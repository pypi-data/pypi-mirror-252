# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: v1/rules/schedule_work_line.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from omni.pro.protos.common import base_pb2 as common_dot_base__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n!v1/rules/schedule_work_line.proto\x12,pro.omni.oms.api.v1.rules.schedule_work_line\x1a\x11\x63ommon/base.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1fgoogle/protobuf/timestamp.proto"\xd9\x01\n\x10ScheduleWorkLine\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0b\n\x03\x64\x61y\x18\x02 \x01(\t\x12\x14\n\x0copening_time\x18\x03 \x01(\t\x12\x14\n\x0c\x63losing_time\x18\x04 \x01(\t\x12*\n\x06\x61\x63tive\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12\x13\n\x0b\x65xternal_id\x18\x06 \x01(\t\x12?\n\x0cobject_audit\x18\x07 \x01(\x0b\x32).pro.omni.oms.api.common.base.ObjectAudit"\xa5\x01\n\x1dScheduleWorkLineCreateRequest\x12\x0b\n\x03\x64\x61y\x18\x01 \x01(\t\x12\x14\n\x0copening_time\x18\x02 \x01(\t\x12\x14\n\x0c\x63losing_time\x18\x03 \x01(\t\x12\x13\n\x0b\x65xternal_id\x18\x04 \x01(\t\x12\x36\n\x07\x63ontext\x18\x05 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xc7\x01\n\x1eScheduleWorkLineCreateResponse\x12Z\n\x12schedule_work_line\x18\x01 \x01(\x0b\x32>.pro.omni.oms.api.v1.rules.schedule_work_line.ScheduleWorkLine\x12I\n\x11response_standard\x18\x02 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard"\xf9\x02\n\x1bScheduleWorkLineReadRequest\x12\x37\n\x08group_by\x18\x01 \x03(\x0b\x32%.pro.omni.oms.api.common.base.GroupBy\x12\x35\n\x07sort_by\x18\x02 \x01(\x0b\x32$.pro.omni.oms.api.common.base.SortBy\x12\x34\n\x06\x66ields\x18\x03 \x01(\x0b\x32$.pro.omni.oms.api.common.base.Fields\x12\x34\n\x06\x66ilter\x18\x04 \x01(\x0b\x32$.pro.omni.oms.api.common.base.Filter\x12:\n\tpaginated\x18\x05 \x01(\x0b\x32\'.pro.omni.oms.api.common.base.Paginated\x12\n\n\x02id\x18\x06 \x01(\t\x12\x36\n\x07\x63ontext\x18\x07 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\x81\x02\n\x1cScheduleWorkLineReadResponse\x12[\n\x13schedule_work_lines\x18\x01 \x03(\x0b\x32>.pro.omni.oms.api.v1.rules.schedule_work_line.ScheduleWorkLine\x12\x39\n\tmeta_data\x18\x02 \x01(\x0b\x32&.pro.omni.oms.api.common.base.MetaData\x12I\n\x11response_standard\x18\x03 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard"\xb3\x01\n\x1dScheduleWorkLineUpdateRequest\x12Z\n\x12schedule_work_line\x18\x01 \x01(\x0b\x32>.pro.omni.oms.api.v1.rules.schedule_work_line.ScheduleWorkLine\x12\x36\n\x07\x63ontext\x18\x02 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xc7\x01\n\x1eScheduleWorkLineUpdateResponse\x12Z\n\x12schedule_work_line\x18\x01 \x01(\x0b\x32>.pro.omni.oms.api.v1.rules.schedule_work_line.ScheduleWorkLine\x12I\n\x11response_standard\x18\x02 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard"c\n\x1dScheduleWorkLineDeleteRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x36\n\x07\x63ontext\x18\x02 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"k\n\x1eScheduleWorkLineDeleteResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard2\xf3\x05\n\x17ScheduleWorkLineService\x12\xb5\x01\n\x16ScheduleWorkLineCreate\x12K.pro.omni.oms.api.v1.rules.schedule_work_line.ScheduleWorkLineCreateRequest\x1aL.pro.omni.oms.api.v1.rules.schedule_work_line.ScheduleWorkLineCreateResponse"\x00\x12\xaf\x01\n\x14ScheduleWorkLineRead\x12I.pro.omni.oms.api.v1.rules.schedule_work_line.ScheduleWorkLineReadRequest\x1aJ.pro.omni.oms.api.v1.rules.schedule_work_line.ScheduleWorkLineReadResponse"\x00\x12\xb5\x01\n\x16ScheduleWorkLineUpdate\x12K.pro.omni.oms.api.v1.rules.schedule_work_line.ScheduleWorkLineUpdateRequest\x1aL.pro.omni.oms.api.v1.rules.schedule_work_line.ScheduleWorkLineUpdateResponse"\x00\x12\xb5\x01\n\x16ScheduleWorkLineDelete\x12K.pro.omni.oms.api.v1.rules.schedule_work_line.ScheduleWorkLineDeleteRequest\x1aL.pro.omni.oms.api.v1.rules.schedule_work_line.ScheduleWorkLineDeleteResponse"\x00\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "v1.rules.schedule_work_line_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals["_SCHEDULEWORKLINE"]._serialized_start = 168
    _globals["_SCHEDULEWORKLINE"]._serialized_end = 385
    _globals["_SCHEDULEWORKLINECREATEREQUEST"]._serialized_start = 388
    _globals["_SCHEDULEWORKLINECREATEREQUEST"]._serialized_end = 553
    _globals["_SCHEDULEWORKLINECREATERESPONSE"]._serialized_start = 556
    _globals["_SCHEDULEWORKLINECREATERESPONSE"]._serialized_end = 755
    _globals["_SCHEDULEWORKLINEREADREQUEST"]._serialized_start = 758
    _globals["_SCHEDULEWORKLINEREADREQUEST"]._serialized_end = 1135
    _globals["_SCHEDULEWORKLINEREADRESPONSE"]._serialized_start = 1138
    _globals["_SCHEDULEWORKLINEREADRESPONSE"]._serialized_end = 1395
    _globals["_SCHEDULEWORKLINEUPDATEREQUEST"]._serialized_start = 1398
    _globals["_SCHEDULEWORKLINEUPDATEREQUEST"]._serialized_end = 1577
    _globals["_SCHEDULEWORKLINEUPDATERESPONSE"]._serialized_start = 1580
    _globals["_SCHEDULEWORKLINEUPDATERESPONSE"]._serialized_end = 1779
    _globals["_SCHEDULEWORKLINEDELETEREQUEST"]._serialized_start = 1781
    _globals["_SCHEDULEWORKLINEDELETEREQUEST"]._serialized_end = 1880
    _globals["_SCHEDULEWORKLINEDELETERESPONSE"]._serialized_start = 1882
    _globals["_SCHEDULEWORKLINEDELETERESPONSE"]._serialized_end = 1989
    _globals["_SCHEDULEWORKLINESERVICE"]._serialized_start = 1992
    _globals["_SCHEDULEWORKLINESERVICE"]._serialized_end = 2747
# @@protoc_insertion_point(module_scope)
