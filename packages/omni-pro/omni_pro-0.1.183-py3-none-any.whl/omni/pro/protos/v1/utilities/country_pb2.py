# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: v1/utilities/country.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from omni.pro.protos.common import base_pb2 as common_dot_base__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x1av1/utilities/country.proto\x12%pro.omni.oms.api.v1.utilities.country\x1a\x11\x63ommon/base.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1egoogle/protobuf/wrappers.proto"\xe0\x04\n\x07\x43ountry\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x19\n\x11phone_number_size\x18\x04 \x01(\x05\x12\x14\n\x0cphone_prefix\x18\x05 \x01(\t\x12\x33\n\x0frequire_zipcode\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12.\n\ncurrencies\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12\x32\n\x0e\x64ocument_types\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12\x36\n\x12territory_matrixes\x18\t \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12*\n\tmeta_data\x18\n \x01(\x0b\x32\x17.google.protobuf.Struct\x12-\n\ttimezones\x18\x0b \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12-\n\tlanguages\x18\x0c \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12\x11\n\tlow_level\x18\r \x01(\t\x12\x0c\n\x04icon\x18\x0e \x01(\x0c\x12*\n\x06\x61\x63tive\x18\x0f \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12\x13\n\x0b\x65xternal_id\x18\x10 \x01(\t\x12?\n\x0cobject_audit\x18\x11 \x01(\x0b\x32).pro.omni.oms.api.common.base.ObjectAudit"\xc0\x04\n\x14\x43ountryCreateRequest\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x19\n\x11phone_number_size\x18\x03 \x01(\x05\x12\x14\n\x0cphone_prefix\x18\x04 \x01(\t\x12\x33\n\x0frequire_zipcode\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12\x32\n\x0e\x63urrencies_ids\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12\x36\n\x12\x64ocument_types_ids\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12:\n\x16territory_matrixes_ids\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12*\n\tmeta_data\x18\t \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x31\n\rtimezones_ids\x18\n \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12\x31\n\rlanguages_ids\x18\x0b \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12\x11\n\tlow_level\x18\x0c \x01(\t\x12\x0c\n\x04icon\x18\r \x01(\x0c\x12\x13\n\x0b\x65xternal_id\x18\x0e \x01(\t\x12\x36\n\x07\x63ontext\x18\x0f \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xa3\x01\n\x15\x43ountryCreateResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard\x12?\n\x07\x63ountry\x18\x02 \x01(\x0b\x32..pro.omni.oms.api.v1.utilities.country.Country"\xf0\x02\n\x12\x43ountryReadRequest\x12\x37\n\x08group_by\x18\x01 \x03(\x0b\x32%.pro.omni.oms.api.common.base.GroupBy\x12\x35\n\x07sort_by\x18\x02 \x01(\x0b\x32$.pro.omni.oms.api.common.base.SortBy\x12\x34\n\x06\x66ields\x18\x03 \x01(\x0b\x32$.pro.omni.oms.api.common.base.Fields\x12\x34\n\x06\x66ilter\x18\x04 \x01(\x0b\x32$.pro.omni.oms.api.common.base.Filter\x12:\n\tpaginated\x18\x05 \x01(\x0b\x32\'.pro.omni.oms.api.common.base.Paginated\x12\n\n\x02id\x18\x06 \x01(\t\x12\x36\n\x07\x63ontext\x18\x07 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xde\x01\n\x13\x43ountryReadResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard\x12\x39\n\tmeta_data\x18\x02 \x01(\x0b\x32&.pro.omni.oms.api.common.base.MetaData\x12\x41\n\tcountries\x18\x03 \x03(\x0b\x32..pro.omni.oms.api.v1.utilities.country.Country"\x8f\x01\n\x14\x43ountryUpdateRequest\x12?\n\x07\x63ountry\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.v1.utilities.country.Country\x12\x36\n\x07\x63ontext\x18\x02 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xa3\x01\n\x15\x43ountryUpdateResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard\x12?\n\x07\x63ountry\x18\x02 \x01(\x0b\x32..pro.omni.oms.api.v1.utilities.country.Country"Z\n\x14\x43ountryDeleteRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x36\n\x07\x63ontext\x18\x02 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"b\n\x15\x43ountryDeleteResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard2\xc6\x04\n\x0e\x43ountryService\x12\x8c\x01\n\rCountryCreate\x12;.pro.omni.oms.api.v1.utilities.country.CountryCreateRequest\x1a<.pro.omni.oms.api.v1.utilities.country.CountryCreateResponse"\x00\x12\x86\x01\n\x0b\x43ountryRead\x12\x39.pro.omni.oms.api.v1.utilities.country.CountryReadRequest\x1a:.pro.omni.oms.api.v1.utilities.country.CountryReadResponse"\x00\x12\x8c\x01\n\rCountryUpdate\x12;.pro.omni.oms.api.v1.utilities.country.CountryUpdateRequest\x1a<.pro.omni.oms.api.v1.utilities.country.CountryUpdateResponse"\x00\x12\x8c\x01\n\rCountryDelete\x12;.pro.omni.oms.api.v1.utilities.country.CountryDeleteRequest\x1a<.pro.omni.oms.api.v1.utilities.country.CountryDeleteResponse"\x00\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "v1.utilities.country_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals["_COUNTRY"]._serialized_start = 151
    _globals["_COUNTRY"]._serialized_end = 759
    _globals["_COUNTRYCREATEREQUEST"]._serialized_start = 762
    _globals["_COUNTRYCREATEREQUEST"]._serialized_end = 1338
    _globals["_COUNTRYCREATERESPONSE"]._serialized_start = 1341
    _globals["_COUNTRYCREATERESPONSE"]._serialized_end = 1504
    _globals["_COUNTRYREADREQUEST"]._serialized_start = 1507
    _globals["_COUNTRYREADREQUEST"]._serialized_end = 1875
    _globals["_COUNTRYREADRESPONSE"]._serialized_start = 1878
    _globals["_COUNTRYREADRESPONSE"]._serialized_end = 2100
    _globals["_COUNTRYUPDATEREQUEST"]._serialized_start = 2103
    _globals["_COUNTRYUPDATEREQUEST"]._serialized_end = 2246
    _globals["_COUNTRYUPDATERESPONSE"]._serialized_start = 2249
    _globals["_COUNTRYUPDATERESPONSE"]._serialized_end = 2412
    _globals["_COUNTRYDELETEREQUEST"]._serialized_start = 2414
    _globals["_COUNTRYDELETEREQUEST"]._serialized_end = 2504
    _globals["_COUNTRYDELETERESPONSE"]._serialized_start = 2506
    _globals["_COUNTRYDELETERESPONSE"]._serialized_end = 2604
    _globals["_COUNTRYSERVICE"]._serialized_start = 2607
    _globals["_COUNTRYSERVICE"]._serialized_end = 3189
# @@protoc_insertion_point(module_scope)
