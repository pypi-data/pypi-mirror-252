# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: common/base.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x11\x63ommon/base.proto\x12\x1cpro.omni.oms.api.common.base\x1a\x1fgoogle/protobuf/timestamp.proto")\n\x06Object\x12\x11\n\tcode_name\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t"\x1d\n\x07GroupBy\x12\x12\n\nname_field\x18\x01 \x01(\t"x\n\x06SortBy\x12\x12\n\nname_field\x18\x01 \x01(\t\x12;\n\x04type\x18\x02 \x01(\x0e\x32-.pro.omni.oms.api.common.base.SortBy.SortType"\x1d\n\x08SortType\x12\x07\n\x03\x41SC\x10\x00\x12\x08\n\x04\x44\x45SC\x10\x01"\x1c\n\x06\x46ields\x12\x12\n\nname_field\x18\x01 \x03(\t"\x18\n\x06\x46ilter\x12\x0e\n\x06\x66ilter\x18\x01 \x01(\t"*\n\tPaginated\x12\x0e\n\x06offset\x18\x01 \x01(\x05\x12\r\n\x05limit\x18\x02 \x01(\x05"\x8c\x01\n\x08LinkPage\x12=\n\x04type\x18\x01 \x01(\x0e\x32/.pro.omni.oms.api.common.base.LinkPage.LinkType\x12\x0c\n\x04link\x18\x02 \x01(\t"3\n\x08LinkType\x12\x08\n\x04NEXT\x10\x00\x12\x08\n\x04PREV\x10\x01\x12\x08\n\x04LAST\x10\x02\x12\t\n\x05\x46IRST\x10\x03"\x82\x01\n\x08MetaData\x12\r\n\x05total\x18\x01 \x01(\x05\x12\x0e\n\x06offset\x18\x02 \x01(\x05\x12\r\n\x05limit\x18\x03 \x01(\x05\x12\r\n\x05\x63ount\x18\x04 \x01(\x05\x12\x39\n\tlink_page\x18\x05 \x03(\x0b\x32&.pro.omni.oms.api.common.base.LinkPage"_\n\x10ResponseStandard\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x13\n\x0bstatus_code\x18\x03 \x01(\x05\x12\x14\n\x0cmessage_code\x18\x04 \x01(\t"\xd9\x01\n\x0bObjectAudit\x12\x12\n\ncreated_by\x18\x01 \x01(\t\x12\x12\n\nupdated_by\x18\x02 \x01(\t\x12\x12\n\ndeleted_by\x18\x03 \x01(\t\x12.\n\ncreated_at\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\nupdated_at\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\ndeleted_at\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp"\'\n\x07\x43ontext\x12\x0e\n\x06tenant\x18\x01 \x01(\t\x12\x0c\n\x04user\x18\x02 \x01(\t"*\n\x0eObjectResponse\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\tb\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "common.base_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals["_OBJECT"]._serialized_start = 84
    _globals["_OBJECT"]._serialized_end = 125
    _globals["_GROUPBY"]._serialized_start = 127
    _globals["_GROUPBY"]._serialized_end = 156
    _globals["_SORTBY"]._serialized_start = 158
    _globals["_SORTBY"]._serialized_end = 278
    _globals["_SORTBY_SORTTYPE"]._serialized_start = 249
    _globals["_SORTBY_SORTTYPE"]._serialized_end = 278
    _globals["_FIELDS"]._serialized_start = 280
    _globals["_FIELDS"]._serialized_end = 308
    _globals["_FILTER"]._serialized_start = 310
    _globals["_FILTER"]._serialized_end = 334
    _globals["_PAGINATED"]._serialized_start = 336
    _globals["_PAGINATED"]._serialized_end = 378
    _globals["_LINKPAGE"]._serialized_start = 381
    _globals["_LINKPAGE"]._serialized_end = 521
    _globals["_LINKPAGE_LINKTYPE"]._serialized_start = 470
    _globals["_LINKPAGE_LINKTYPE"]._serialized_end = 521
    _globals["_METADATA"]._serialized_start = 524
    _globals["_METADATA"]._serialized_end = 654
    _globals["_RESPONSESTANDARD"]._serialized_start = 656
    _globals["_RESPONSESTANDARD"]._serialized_end = 751
    _globals["_OBJECTAUDIT"]._serialized_start = 754
    _globals["_OBJECTAUDIT"]._serialized_end = 971
    _globals["_CONTEXT"]._serialized_start = 973
    _globals["_CONTEXT"]._serialized_end = 1012
    _globals["_OBJECTRESPONSE"]._serialized_start = 1014
    _globals["_OBJECTRESPONSE"]._serialized_end = 1056
# @@protoc_insertion_point(module_scope)
