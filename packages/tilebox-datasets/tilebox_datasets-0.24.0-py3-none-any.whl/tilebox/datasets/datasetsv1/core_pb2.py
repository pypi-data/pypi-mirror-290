# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: datasets/v1/core.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import type_pb2 as google_dot_protobuf_dot_type__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16\x64\x61tasets/v1/core.proto\x12\x0b\x64\x61tasets.v1\x1a google/protobuf/descriptor.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1agoogle/protobuf/type.proto\"\x18\n\x02ID\x12\x12\n\x04uuid\x18\x01 \x01(\x0cR\x04uuid\"\xce\x01\n\x0cTimeInterval\x12\x39\n\nstart_time\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tstartTime\x12\x35\n\x08\x65nd_time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x07\x65ndTime\x12\'\n\x0fstart_exclusive\x18\x03 \x01(\x08R\x0estartExclusive\x12#\n\rend_inclusive\x18\x04 \x01(\x08R\x0c\x65ndInclusive\"\x93\x01\n\x11\x44\x61tapointInterval\x12\x19\n\x08start_id\x18\x01 \x01(\tR\x07startId\x12\x15\n\x06\x65nd_id\x18\x02 \x01(\tR\x05\x65ndId\x12\'\n\x0fstart_exclusive\x18\x03 \x01(\x08R\x0estartExclusive\x12#\n\rend_inclusive\x18\x04 \x01(\x08R\x0c\x65ndInclusive\"p\n\nPagination\x12\x19\n\x05limit\x18\x01 \x01(\x03H\x00R\x05limit\x88\x01\x01\x12*\n\x0estarting_after\x18\x02 \x01(\tH\x01R\rstartingAfter\x88\x01\x01\x42\x08\n\x06_limitB\x11\n\x0f_starting_after\"\xad\x01\n\x11\x44\x61tapointMetadata\x12\x39\n\nevent_time\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\teventTime\x12\x41\n\x0eingestion_time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\ringestionTime\x12\x13\n\x02id\x18\x03 \x01(\tH\x00R\x02id\x88\x01\x01\x42\x05\n\x03_id\"0\n\nCollection\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x12\n\x04name\x18\x02 \x01(\tR\x04name\"\xc3\x01\n\x0e\x43ollectionInfo\x12\x37\n\ncollection\x18\x01 \x01(\x0b\x32\x17.datasets.v1.CollectionR\ncollection\x12\x42\n\x0c\x61vailability\x18\x02 \x01(\x0b\x32\x19.datasets.v1.TimeIntervalH\x00R\x0c\x61vailability\x88\x01\x01\x12\x19\n\x05\x63ount\x18\x03 \x01(\x04H\x01R\x05\x63ount\x88\x01\x01\x42\x0f\n\r_availabilityB\x08\n\x06_count\">\n\x0b\x43ollections\x12/\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\x1b.datasets.v1.CollectionInfoR\x04\x64\x61ta\"X\n\x0f\x46ieldAnnotation\x12 \n\x0b\x64\x65scription\x18\x01 \x01(\tR\x0b\x64\x65scription\x12#\n\rexample_value\x18\x02 \x01(\tR\x0c\x65xampleValue\"\xe2\x01\n\rAnnotatedType\x12I\n\x0e\x64\x65scriptor_set\x18\x01 \x01(\x0b\x32\".google.protobuf.FileDescriptorSetR\rdescriptorSet\x12\x19\n\x08type_url\x18\x02 \x01(\tR\x07typeUrl\x12 \n\x0b\x64\x65scription\x18\x03 \x01(\tR\x0b\x64\x65scription\x12I\n\x11\x66ield_annotations\x18\x04 \x03(\x0b\x32\x1c.datasets.v1.FieldAnnotationR\x10\x66ieldAnnotations\"\xd5\x01\n\rLegacyDataset\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x1d\n\nserver_key\x18\x02 \x01(\tR\tserverKey\x12\x1d\n\nclient_key\x18\x03 \x01(\tR\tclientKey\x12\x12\n\x04name\x18\x04 \x01(\tR\x04name\x12\x18\n\x07summary\x18\x05 \x01(\tR\x07summary\x12\x18\n\x07service\x18\x06 \x01(\tR\x07service\x12.\n\x04type\x18\x07 \x01(\x0b\x32\x1a.datasets.v1.AnnotatedTypeR\x04type\"\x87\x02\n\x07\x44\x61taset\x12\x1f\n\x02id\x18\x01 \x01(\x0b\x32\x0f.datasets.v1.IDR\x02id\x12*\n\x08group_id\x18\x02 \x01(\x0b\x32\x0f.datasets.v1.IDR\x07groupId\x12.\n\x04type\x18\x03 \x01(\x0b\x32\x1a.datasets.v1.AnnotatedTypeR\x04type\x12\x1b\n\tcode_name\x18\x04 \x01(\tR\x08\x63odeName\x12\x12\n\x04name\x18\x05 \x01(\tR\x04name\x12\x18\n\x07summary\x18\x06 \x01(\tR\x07summary\x12\x12\n\x04icon\x18\x07 \x01(\tR\x04icon\x12 \n\x0b\x64\x65scription\x18\x08 \x01(\tR\x0b\x64\x65scription\"\x99\x01\n\x12LegacyDatasetGroup\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\x12\x37\n\x06groups\x18\x02 \x03(\x0b\x32\x1f.datasets.v1.LegacyDatasetGroupR\x06groups\x12\x36\n\x08\x64\x61tasets\x18\x03 \x03(\x0b\x32\x1a.datasets.v1.LegacyDatasetR\x08\x64\x61tasets\"\xa2\x01\n\x0c\x44\x61tasetGroup\x12\x1f\n\x02id\x18\x01 \x01(\x0b\x32\x0f.datasets.v1.IDR\x02id\x12,\n\tparent_id\x18\x02 \x01(\x0b\x32\x0f.datasets.v1.IDR\x08parentId\x12\x1b\n\tcode_name\x18\x03 \x01(\tR\x08\x63odeName\x12\x12\n\x04name\x18\x04 \x01(\tR\x04name\x12\x12\n\x04icon\x18\x05 \x01(\tR\x04icon\"\x93\x01\n\x15GetCollectionsRequest\x12.\n\ndataset_id\x18\x01 \x01(\x0b\x32\x0f.datasets.v1.IDR\tdatasetId\x12+\n\x11with_availability\x18\x02 \x01(\x08R\x10withAvailability\x12\x1d\n\nwith_count\x18\x03 \x01(\x08R\twithCount\"\xc1\x01\n\x1aGetCollectionByNameRequest\x12\'\n\x0f\x63ollection_name\x18\x01 \x01(\tR\x0e\x63ollectionName\x12+\n\x11with_availability\x18\x02 \x01(\x08R\x10withAvailability\x12\x1d\n\nwith_count\x18\x03 \x01(\x08R\twithCount\x12.\n\ndataset_id\x18\x04 \x01(\x0b\x32\x0f.datasets.v1.IDR\tdatasetId\"\xc7\x02\n\x1cGetDatasetForIntervalRequest\x12#\n\rcollection_id\x18\x01 \x01(\tR\x0c\x63ollectionId\x12>\n\rtime_interval\x18\x02 \x01(\x0b\x32\x19.datasets.v1.TimeIntervalR\x0ctimeInterval\x12M\n\x12\x64\x61tapoint_interval\x18\x06 \x01(\x0b\x32\x1e.datasets.v1.DatapointIntervalR\x11\x64\x61tapointInterval\x12\x30\n\x04page\x18\x03 \x01(\x0b\x32\x17.datasets.v1.PaginationH\x00R\x04page\x88\x01\x01\x12\x1b\n\tskip_data\x18\x04 \x01(\x08R\x08skipData\x12\x1b\n\tskip_meta\x18\x05 \x01(\x08R\x08skipMetaB\x07\n\x05_page\"k\n\x17GetDatapointByIdRequest\x12#\n\rcollection_id\x18\x01 \x01(\tR\x0c\x63ollectionId\x12\x0e\n\x02id\x18\x02 \x01(\tR\x02id\x12\x1b\n\tskip_data\x18\x03 \x01(\x08R\x08skipData\"6\n\x03\x41ny\x12\x19\n\x08type_url\x18\x01 \x01(\tR\x07typeUrl\x12\x14\n\x05value\x18\x02 \x01(\x0cR\x05value\">\n\x0bRepeatedAny\x12\x19\n\x08type_url\x18\x01 \x01(\tR\x07typeUrl\x12\x14\n\x05value\x18\x02 \x03(\x0cR\x05valueB\xb6\x01\n\x0f\x63om.datasets.v1B\tCoreProtoP\x01ZKgithub.com/tilebox/core/datasets-service/protogen/go/datasets/v1;datasetsv1\xa2\x02\x03\x44XX\xaa\x02\x0b\x44\x61tasets.V1\xca\x02\x0b\x44\x61tasets\\V1\xe2\x02\x17\x44\x61tasets\\V1\\GPBMetadata\xea\x02\x0c\x44\x61tasets::V1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'datasets.v1.core_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\017com.datasets.v1B\tCoreProtoP\001ZKgithub.com/tilebox/core/datasets-service/protogen/go/datasets/v1;datasetsv1\242\002\003DXX\252\002\013Datasets.V1\312\002\013Datasets\\V1\342\002\027Datasets\\V1\\GPBMetadata\352\002\014Datasets::V1'
  _globals['_ID']._serialized_start=134
  _globals['_ID']._serialized_end=158
  _globals['_TIMEINTERVAL']._serialized_start=161
  _globals['_TIMEINTERVAL']._serialized_end=367
  _globals['_DATAPOINTINTERVAL']._serialized_start=370
  _globals['_DATAPOINTINTERVAL']._serialized_end=517
  _globals['_PAGINATION']._serialized_start=519
  _globals['_PAGINATION']._serialized_end=631
  _globals['_DATAPOINTMETADATA']._serialized_start=634
  _globals['_DATAPOINTMETADATA']._serialized_end=807
  _globals['_COLLECTION']._serialized_start=809
  _globals['_COLLECTION']._serialized_end=857
  _globals['_COLLECTIONINFO']._serialized_start=860
  _globals['_COLLECTIONINFO']._serialized_end=1055
  _globals['_COLLECTIONS']._serialized_start=1057
  _globals['_COLLECTIONS']._serialized_end=1119
  _globals['_FIELDANNOTATION']._serialized_start=1121
  _globals['_FIELDANNOTATION']._serialized_end=1209
  _globals['_ANNOTATEDTYPE']._serialized_start=1212
  _globals['_ANNOTATEDTYPE']._serialized_end=1438
  _globals['_LEGACYDATASET']._serialized_start=1441
  _globals['_LEGACYDATASET']._serialized_end=1654
  _globals['_DATASET']._serialized_start=1657
  _globals['_DATASET']._serialized_end=1920
  _globals['_LEGACYDATASETGROUP']._serialized_start=1923
  _globals['_LEGACYDATASETGROUP']._serialized_end=2076
  _globals['_DATASETGROUP']._serialized_start=2079
  _globals['_DATASETGROUP']._serialized_end=2241
  _globals['_GETCOLLECTIONSREQUEST']._serialized_start=2244
  _globals['_GETCOLLECTIONSREQUEST']._serialized_end=2391
  _globals['_GETCOLLECTIONBYNAMEREQUEST']._serialized_start=2394
  _globals['_GETCOLLECTIONBYNAMEREQUEST']._serialized_end=2587
  _globals['_GETDATASETFORINTERVALREQUEST']._serialized_start=2590
  _globals['_GETDATASETFORINTERVALREQUEST']._serialized_end=2917
  _globals['_GETDATAPOINTBYIDREQUEST']._serialized_start=2919
  _globals['_GETDATAPOINTBYIDREQUEST']._serialized_end=3026
  _globals['_ANY']._serialized_start=3028
  _globals['_ANY']._serialized_end=3082
  _globals['_REPEATEDANY']._serialized_start=3084
  _globals['_REPEATEDANY']._serialized_end=3146
# @@protoc_insertion_point(module_scope)
