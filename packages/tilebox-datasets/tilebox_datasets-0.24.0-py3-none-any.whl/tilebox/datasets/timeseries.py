from collections.abc import AsyncIterator
from functools import partial

import xarray as xr

from _tilebox.grpc.aio.producer_consumer import async_producer_consumer
from _tilebox.grpc.aio.syncify import Syncifiable
from _tilebox.grpc.error import ArgumentError, NotFoundError
from tilebox.datasets.data.collection import Collection, CollectionInfo
from tilebox.datasets.data.datapoint import DatapointInterval, DatapointPage
from tilebox.datasets.data.datasets import Dataset
from tilebox.datasets.data.pagination import Pagination
from tilebox.datasets.data.time_interval import TimeInterval, TimeIntervalLike
from tilebox.datasets.pagination import (
    paginated_request,
    with_progressbar,
    with_time_progressbar,
)
from tilebox.datasets.protobuf_xarray import TimeseriesToXarrayConverter
from tilebox.datasets.service import TileboxDatasetService

# allow private member access: we allow it here because we want to make as much private as possible so that we can
# minimize the publicly facing API (which allows us to change internals later, and also limits to auto-completion)
# ruff: noqa: SLF001


class RemoteTimeseriesDataset(Syncifiable):
    """A client for a timeseries dataset."""

    def __init__(
        self,
        service: TileboxDatasetService,
        dataset: Dataset,
    ) -> None:
        self._service = service
        self.name = dataset.name
        self._dataset = dataset

    async def collections(
        self, availability: bool = True, count: bool = False
    ) -> dict[str, "RemoteTimeseriesDatasetCollection"]:
        """
        List the available collections in this dataset.

        Args:
            availability: Whether to include the availability interval (timestamp of the first and the
                last available data point) of each collection
            count: Whether to include the number of datapoints in each collection

        Returns:
            A mapping from collection names to collections.
        """
        collections = await self._service.get_collections(self._dataset.id, availability, count)

        dataset_collections = {}
        for collection in collections:
            remote_collection = self._collection_client(collection.collection.name)
            remote_collection._info_cache[(availability, count)] = collection
            dataset_collections[collection.collection.name] = remote_collection

        return dataset_collections

    def collection(self, collection: str) -> "RemoteTimeseriesDatasetCollection":
        """Create a client for queriying data in a specific collection in this dataset."""
        return self._collection_client(collection)

    def _collection_client(self, name: str) -> "RemoteTimeseriesDatasetCollection":
        """Create a client for queriying data in a specific collection in this dataset."""
        # this is its own method so that we can patch it when syncifying the dataset to also syncify the collection
        return RemoteTimeseriesDatasetCollection(self, name)

    def _syncify(self) -> None:
        """Syncify this dataset and all collections created via its functions."""
        super()._syncify()

        # patch the _collection_client method to also syncify the collection
        original = self._collection_client

        def _syncified_collection_client(name: str) -> RemoteTimeseriesDatasetCollection:
            collection = original(name)
            collection._syncify()
            return collection

        self._collection_client = _syncified_collection_client

    def __repr__(self) -> str:
        return f"{self.name} [Timeseries Dataset]: {self._dataset.summary}"


class RemoteTimeseriesDatasetCollection(Syncifiable):
    """A client for a datapoint collection in a specific timeseries dataset."""

    def __init__(
        self,
        dataset: RemoteTimeseriesDataset,
        collection_name: str,
    ) -> None:
        self._dataset = dataset
        self.name = collection_name
        # avoid unnecessary info requests by caching the info responses
        self._info_cache: dict[tuple[bool, bool], CollectionInfo] = {}

    def __repr__(self) -> str:
        """Human readable representation of the collection."""
        # find the cached info with the most information
        for key in [(True, True), (True, False), (False, True), (False, False)]:
            if key in self._info_cache:
                return repr(self._info_cache[key])
        return f"Collection {self.name}: <data info not loaded yet>"

    async def info(self, availability: bool = True, count: bool = False) -> CollectionInfo:
        """
        Fetch additional metadata about the datapoints in this collection.

        Args:
            availability: Whether to include the availability interval (timestamp of the first and the
                last available data point) of each collection
            count: Whether to include the number of datapoints in each collection

        Returns:
            collection info for the current collection
        """
        return await self._info(availability, count)

    async def _info(self, availability: bool = True, count: bool = False) -> CollectionInfo:
        """
        Actual implementation of the info method.

        Will always be an async function and can be awaited, even for the syncified version of the dataset.
        """
        if (availability, count) in self._info_cache:
            return self._info_cache[(availability, count)]

        try:
            info = await self._dataset._service.get_collection_by_name(
                self._dataset._dataset.id, self.name, availability, count
            )
        except NotFoundError:
            raise NotFoundError(f"No such collection {self.name}") from None

        self._info_cache[(availability, count)] = info
        return info

    async def find(self, datapoint_id: str, skip_data: bool = False) -> xr.Dataset:
        """
        Find a specific datapoint in this collection by its id.

        Args:
            datapoint_id: The id of the datapoint to find
            skip_data: Whether to skip the actual data of the datapoint. If True, only datapoint metadata is returned.

        Returns:
            The datapoint as an xarray dataset
        """
        collection = await self._collection()
        try:
            datapoint = await self._dataset._service.get_datapoint_by_id(collection.id, datapoint_id, skip_data)
        except ArgumentError:
            raise ValueError(f"Invalid datapoint id: {datapoint_id} is not a valid UUID") from None
        except NotFoundError:
            raise NotFoundError(f"No such datapoint {datapoint_id}") from None

        converter = TimeseriesToXarrayConverter(initial_capacity=1)
        converter.convert(datapoint)
        return converter.finalize().isel(time=0)

    async def _find_interval(
        self,
        datapoint_id_interval: tuple[str, str],
        end_inclusive: bool = True,
        *,
        skip_data: bool = False,
        show_progress: bool = False,
    ) -> xr.Dataset:
        """
        Find a range of datapoints in this collection in an interval specified as datapoint ids.

        Args:
            datapoint_id_interval: tuple of two datapoint ids specifying the interval: [start_id, end_id]
            end_inclusive: Flag indicating whether the datapoint with the given end_id should be included in the
                result or not.
            skip_data: Whether to skip the actual data of the datapoint. If True, only datapoint metadata is returned.
            show_progress: Whether to show a progress bar while loading the data.

        Returns:
            The datapoints in the given interval as an xarray dataset
        """
        start_id, end_id = datapoint_id_interval

        collection = await self._collection()
        datapoint_interval = DatapointInterval(
            start_id=start_id,
            end_id=end_id,
            start_exclusive=False,
            end_inclusive=end_inclusive,
        )
        request = partial(
            self._dataset._service.get_dataset_for_datapoint_interval,
            collection.id,
            datapoint_interval,
            skip_data,
            False,
        )

        initial_page = Pagination()
        pages = paginated_request(request, initial_page)
        if show_progress:
            pages = with_progressbar(pages, f"Fetching {self._dataset.name}")

        return await _convert_to_dataset(pages)

    async def load(
        self,
        time_or_interval: TimeIntervalLike,
        *,
        skip_data: bool = False,
        show_progress: bool = False,
    ) -> xr.Dataset:
        """
        Load a range of datapoints in this collection in a specified interval.

        The interval can be specified in a number of ways:
        - TimeInterval: interval -> Use the time interval as its given
        - DatetimeScalar: [time, time] -> Construct a TimeInterval with start and end time set to the given value and
            the end time inclusive
        - tuple of two DatetimeScalar: [start, end) -> Construct a TimeInterval with the given start and end time
        - xr.DataArray: [arr[0], arr[-1]] -> Construct a TimeInterval with start and end time set to the first and last
            value in the array and the end time inclusive
        - xr.Dataset: [ds.time[0], ds.time[-1]] -> Construct a TimeInterval with start and end time set to the first
            and last value in the time coordinate of the dataset and the end time inclusive

        Args:
            time_or_interval: The interval argument as described above
            skip_data: Whether to skip the actual data of the datapoint. If True, only datapoint metadata is returned.
            show_progress: Whether to show a progress bar while loading the data

        Returns:
            The datapoints in the given interval as an xarray dataset
        """
        pages = self._iter_pages(time_or_interval, skip_data, show_progress=show_progress)
        return await _convert_to_dataset(pages)

    async def _iter_pages(
        self,
        time_or_interval: TimeIntervalLike,
        skip_data: bool = False,
        skip_meta: bool = False,
        show_progress: bool = False,
        page_size: int | None = None,
    ) -> AsyncIterator[DatapointPage]:
        time_interval = TimeInterval.parse(time_or_interval)
        collection = await self._collection()

        request = partial(
            self._dataset._service.get_dataset_for_time_interval, collection.id, time_interval, skip_data, skip_meta
        )

        initial_page = Pagination(limit=page_size)
        pages = paginated_request(request, initial_page)

        if show_progress:
            message = f"Fetching {self._dataset.name}"
            if skip_meta:  # without metadata we can't estimate progress based on event time (since it is not returned)
                pages = with_progressbar(pages, message)
            else:
                pages = with_time_progressbar(pages, time_interval, message)

        async for page in pages:
            yield page

    async def _collection(self) -> Collection:
        """
        Return the collection object (containing name and id). If this information is already cached, it is returned.

        Otherwise a info request is made to the server to retrieve the collection information.
        """
        if len(self._info_cache) >= 1:
            return next(iter(self._info_cache.values())).collection
        return (await self._info(availability=False, count=False)).collection


async def _convert_to_dataset(pages: AsyncIterator[DatapointPage]) -> xr.Dataset:
    """
    Convert an async iterator of DatasetIntervals (pages) into a single xarray Dataset

    Parses each incoming page while in parallel already requesting and waiting for the next page from the server.

    Args:
        pages: Async iterator of DatasetIntervals (pages) to convert

    Returns:
        The datapoints from the individual pages converted and combined into a single xarray dataset
    """

    converter = TimeseriesToXarrayConverter()
    # lets parse the incoming pages already while we wait for the next page from the server
    # we solve this using a classic producer/consumer with a queue of pages for communication
    # this would also account for the case where the server sends pages faster than we are converting
    # them to xarray
    await async_producer_consumer(pages, lambda page: converter.convert_all(page))
    return converter.finalize()
