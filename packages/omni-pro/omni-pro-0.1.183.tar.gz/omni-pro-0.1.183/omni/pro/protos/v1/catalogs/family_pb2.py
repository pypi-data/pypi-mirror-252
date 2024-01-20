# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: v1/catalogs/family.proto
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
    b'\n\x18v1/catalogs/family.proto\x12#pro.omni.oms.api.v1.catalogs.family\x1a\x1cgoogle/protobuf/struct.proto\x1a\x11\x63ommon/base.proto\x1a\x1egoogle/protobuf/wrappers.proto"\x9e\x03\n\x06\x46\x61mily\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0c\n\x04\x63ode\x18\x03 \x01(\t\x12J\n\x12\x61ttribute_as_label\x18\x04 \x01(\x0b\x32..pro.omni.oms.api.v1.catalogs.family.Attribute\x12J\n\x12\x61ttribute_as_image\x18\x05 \x01(\x0b\x32..pro.omni.oms.api.v1.catalogs.family.Attribute\x12)\n\x08variants\x18\x06 \x03(\x0b\x32\x17.google.protobuf.Struct\x12\'\n\x06groups\x18\x07 \x03(\x0b\x32\x17.google.protobuf.Struct\x12\x13\n\x0b\x65xternal_id\x18\x08 \x01(\t\x12*\n\x06\x61\x63tive\x18\t \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12?\n\x0cobject_audit\x18\n \x01(\x0b\x32).pro.omni.oms.api.common.base.ObjectAudit"\xb6\x01\n\x13\x46\x61milyCreateRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t\x12\x1a\n\x12\x61ttribute_as_label\x18\x03 \x01(\t\x12\x1a\n\x12\x61ttribute_as_image\x18\x04 \x01(\t\x12\x13\n\x0b\x65xternal_id\x18\x05 \x01(\t\x12\x36\n\x07\x63ontext\x18\x06 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\x9e\x01\n\x14\x46\x61milyCreateResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard\x12;\n\x06\x66\x61mily\x18\x02 \x01(\x0b\x32+.pro.omni.oms.api.v1.catalogs.family.Family"\xef\x02\n\x11\x46\x61milyReadRequest\x12\x37\n\x08group_by\x18\x01 \x03(\x0b\x32%.pro.omni.oms.api.common.base.GroupBy\x12\x35\n\x07sort_by\x18\x02 \x01(\x0b\x32$.pro.omni.oms.api.common.base.SortBy\x12\x34\n\x06\x66ields\x18\x03 \x01(\x0b\x32$.pro.omni.oms.api.common.base.Fields\x12\x34\n\x06\x66ilter\x18\x04 \x01(\x0b\x32$.pro.omni.oms.api.common.base.Filter\x12:\n\tpaginated\x18\x05 \x01(\x0b\x32\'.pro.omni.oms.api.common.base.Paginated\x12\n\n\x02id\x18\x06 \x01(\t\x12\x36\n\x07\x63ontext\x18\x07 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\x91\x02\n\x12\x46\x61milyReadResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard\x12\x39\n\tmeta_data\x18\x02 \x01(\x0b\x32&.pro.omni.oms.api.common.base.MetaData\x12=\n\x08\x66\x61milies\x18\x03 \x03(\x0b\x32+.pro.omni.oms.api.v1.catalogs.family.Family\x12\x36\n\x07\x63ontext\x18\x04 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\x8a\x01\n\x13\x46\x61milyUpdateRequest\x12;\n\x06\x66\x61mily\x18\x01 \x01(\x0b\x32+.pro.omni.oms.api.v1.catalogs.family.Family\x12\x36\n\x07\x63ontext\x18\x02 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\x9e\x01\n\x14\x46\x61milyUpdateResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard\x12;\n\x06\x66\x61mily\x18\x02 \x01(\x0b\x32+.pro.omni.oms.api.v1.catalogs.family.Family"Y\n\x13\x46\x61milyDeleteRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x36\n\x07\x63ontext\x18\x02 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"a\n\x14\x46\x61milyDeleteResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard"\x96\x02\n\tAttribute\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x16\n\x0e\x61ttribute_type\x18\x03 \x01(\t\x12\x11\n\tis_common\x18\x04 \x01(\x08\x12\'\n\x06\x66\x61mily\x18\x05 \x01(\x0b\x32\x17.google.protobuf.Struct\x12&\n\x05group\x18\x06 \x01(\x0b\x32\x17.google.protobuf.Struct\x12*\n\x06\x61\x63tive\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12\x13\n\x0b\x65xternal_id\x18\x08 \x01(\t\x12\x30\n\x0f\x65xtra_attribute\x18\t \x01(\x0b\x32\x17.google.protobuf.Struct"\x85\x02\n\x16\x41ttributeCreateRequest\x12\x11\n\tfamily_id\x18\x01 \x01(\t\x12\x12\n\ngroup_code\x18\x02 \x01(\t\x12\x0c\n\x04\x63ode\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x16\n\x0e\x61ttribute_type\x18\x05 \x01(\t\x12\x11\n\tis_common\x18\x06 \x01(\x08\x12\x30\n\x0f\x65xtra_attribute\x18\x07 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x13\n\x0b\x65xternal_id\x18\x08 \x01(\t\x12\x36\n\x07\x63ontext\x18\t \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xa7\x01\n\x17\x41ttributeCreateResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard\x12\x41\n\tattribute\x18\x02 \x01(\x0b\x32..pro.omni.oms.api.v1.catalogs.family.Attribute"\x9b\x03\n\x14\x41ttributeReadRequest\x12\x11\n\tfamily_id\x18\x01 \x01(\t\x12\x12\n\ngroup_code\x18\x02 \x01(\t\x12\x0c\n\x04\x63ode\x18\x03 \x01(\t\x12\x37\n\x08group_by\x18\x04 \x03(\x0b\x32%.pro.omni.oms.api.common.base.GroupBy\x12\x35\n\x07sort_by\x18\x05 \x01(\x0b\x32$.pro.omni.oms.api.common.base.SortBy\x12\x34\n\x06\x66ields\x18\x06 \x01(\x0b\x32$.pro.omni.oms.api.common.base.Fields\x12\x34\n\x06\x66ilter\x18\x07 \x01(\x0b\x32$.pro.omni.oms.api.common.base.Filter\x12:\n\tpaginated\x18\x08 \x01(\x0b\x32\'.pro.omni.oms.api.common.base.Paginated\x12\x36\n\x07\x63ontext\x18\t \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xe1\x01\n\x15\x41ttributeReadResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard\x12\x39\n\tmeta_data\x18\x02 \x01(\x0b\x32&.pro.omni.oms.api.common.base.MetaData\x12\x42\n\nattributes\x18\x03 \x03(\x0b\x32..pro.omni.oms.api.v1.catalogs.family.Attribute"\x93\x01\n\x16\x41ttributeUpdateRequest\x12\x41\n\tattribute\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.v1.catalogs.family.Attribute\x12\x36\n\x07\x63ontext\x18\x02 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xa7\x01\n\x17\x41ttributeUpdateResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard\x12\x41\n\tattribute\x18\x02 \x01(\x0b\x32..pro.omni.oms.api.v1.catalogs.family.Attribute"\x85\x01\n\x16\x41ttributeDeleteRequest\x12\x11\n\tfamily_id\x18\x01 \x01(\t\x12\x12\n\ngroup_code\x18\x02 \x01(\t\x12\x0c\n\x04\x63ode\x18\x03 \x01(\t\x12\x36\n\x07\x63ontext\x18\x04 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"d\n\x17\x41ttributeDeleteResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard"\xd1\x01\n\x05Group\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12*\n\x06\x61\x63tive\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12\'\n\x06\x66\x61mily\x18\x04 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x13\n\x0b\x65xternal_id\x18\x05 \x01(\t\x12\x42\n\nattributes\x18\x06 \x03(\x0b\x32..pro.omni.oms.api.v1.catalogs.family.Attribute"\x90\x01\n\x12GroupCreateRequest\x12\x11\n\tfamily_id\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x13\n\x0b\x65xternal_id\x18\x04 \x01(\t\x12\x36\n\x07\x63ontext\x18\x05 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\x9b\x01\n\x13GroupCreateResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard\x12\x39\n\x05group\x18\x02 \x01(\x0b\x32*.pro.omni.oms.api.v1.catalogs.family.Group"\x83\x03\n\x10GroupReadRequest\x12\x11\n\tfamily_id\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t\x12\x37\n\x08group_by\x18\x03 \x03(\x0b\x32%.pro.omni.oms.api.common.base.GroupBy\x12\x35\n\x07sort_by\x18\x04 \x01(\x0b\x32$.pro.omni.oms.api.common.base.SortBy\x12\x34\n\x06\x66ields\x18\x05 \x01(\x0b\x32$.pro.omni.oms.api.common.base.Fields\x12\x34\n\x06\x66ilter\x18\x06 \x01(\x0b\x32$.pro.omni.oms.api.common.base.Filter\x12:\n\tpaginated\x18\x07 \x01(\x0b\x32\'.pro.omni.oms.api.common.base.Paginated\x12\x36\n\x07\x63ontext\x18\x08 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xd5\x01\n\x11GroupReadResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard\x12\x39\n\tmeta_data\x18\x02 \x01(\x0b\x32&.pro.omni.oms.api.common.base.MetaData\x12:\n\x06groups\x18\x03 \x03(\x0b\x32*.pro.omni.oms.api.v1.catalogs.family.Group"\x9a\x01\n\x12GroupUpdateRequest\x12\x11\n\tfamily_id\x18\x01 \x01(\t\x12\x39\n\x05group\x18\x02 \x01(\x0b\x32*.pro.omni.oms.api.v1.catalogs.family.Group\x12\x36\n\x07\x63ontext\x18\x03 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\x9b\x01\n\x13GroupUpdateResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard\x12\x39\n\x05group\x18\x02 \x01(\x0b\x32*.pro.omni.oms.api.v1.catalogs.family.Group"m\n\x12GroupDeleteRequest\x12\x11\n\tfamily_id\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t\x12\x36\n\x07\x63ontext\x18\x03 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"`\n\x13GroupDeleteResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard"\xa4\x01\n\x10\x41ttributeVariant\x12*\n\tattribute\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x10\n\x08sequence\x18\x02 \x01(\x05\x12\x11\n\tfamily_id\x18\x03 \x01(\t\x12\x13\n\x0b\x65xternal_id\x18\x04 \x01(\t\x12*\n\x06\x61\x63tive\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.BoolValue"\xa9\x01\n\x1d\x41ttributeVariantCreateRequest\x12\x11\n\tfamily_id\x18\x01 \x01(\t\x12\x16\n\x0e\x61ttribute_code\x18\x02 \x01(\t\x12\x10\n\x08sequence\x18\x03 \x01(\x05\x12\x13\n\x0b\x65xternal_id\x18\x04 \x01(\t\x12\x36\n\x07\x63ontext\x18\x05 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xbd\x01\n\x1e\x41ttributeVariantCreateResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard\x12P\n\x11\x61ttribute_variant\x18\x02 \x01(\x0b\x32\x35.pro.omni.oms.api.v1.catalogs.family.AttributeVariant"\x98\x03\n\x1b\x41ttributeVariantReadRequest\x12\x11\n\tfamily_id\x18\x01 \x01(\t\x12\x16\n\x0e\x61ttribute_code\x18\x02 \x01(\t\x12\x37\n\x08group_by\x18\x03 \x03(\x0b\x32%.pro.omni.oms.api.common.base.GroupBy\x12\x35\n\x07sort_by\x18\x04 \x01(\x0b\x32$.pro.omni.oms.api.common.base.SortBy\x12\x34\n\x06\x66ields\x18\x05 \x01(\x0b\x32$.pro.omni.oms.api.common.base.Fields\x12\x34\n\x06\x66ilter\x18\x06 \x01(\x0b\x32$.pro.omni.oms.api.common.base.Filter\x12:\n\tpaginated\x18\x07 \x01(\x0b\x32\'.pro.omni.oms.api.common.base.Paginated\x12\x36\n\x07\x63ontext\x18\x08 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xf7\x01\n\x1c\x41ttributeVariantReadResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard\x12\x39\n\tmeta_data\x18\x02 \x01(\x0b\x32&.pro.omni.oms.api.common.base.MetaData\x12Q\n\x12\x61ttribute_variants\x18\x03 \x03(\x0b\x32\x35.pro.omni.oms.api.v1.catalogs.family.AttributeVariant"\xb7\x01\n\x1d\x41ttributeVariantUpdateRequest\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\x12P\n\x11\x61ttribute_variant\x18\x02 \x01(\x0b\x32\x35.pro.omni.oms.api.v1.catalogs.family.AttributeVariant\x12\x36\n\x07\x63ontext\x18\x03 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xbd\x01\n\x1e\x41ttributeVariantUpdateResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard\x12P\n\x11\x61ttribute_variant\x18\x02 \x01(\x0b\x32\x35.pro.omni.oms.api.v1.catalogs.family.AttributeVariant"\x82\x01\n\x1d\x41ttributeVariantDeleteRequest\x12\x11\n\tfamily_id\x18\x01 \x01(\t\x12\x16\n\x0e\x61ttribute_code\x18\x02 \x01(\t\x12\x36\n\x07\x63ontext\x18\x03 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"k\n\x1e\x41ttributeVariantDeleteResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard"\xaf\x01\n\x08\x43\x61tegory\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x16\n\x0e\x61ttribute_type\x18\x03 \x01(\t\x12\x11\n\tis_common\x18\x04 \x01(\x08\x12*\n\x06\x61\x63tive\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12\x30\n\x0f\x65xtra_attribute\x18\x06 \x01(\x0b\x32\x17.google.protobuf.Struct"\xe5\x02\n\x13\x43\x61tegoryReadRequest\x12\x37\n\x08group_by\x18\x02 \x03(\x0b\x32%.pro.omni.oms.api.common.base.GroupBy\x12\x35\n\x07sort_by\x18\x03 \x01(\x0b\x32$.pro.omni.oms.api.common.base.SortBy\x12\x34\n\x06\x66ields\x18\x04 \x01(\x0b\x32$.pro.omni.oms.api.common.base.Fields\x12\x34\n\x06\x66ilter\x18\x05 \x01(\x0b\x32$.pro.omni.oms.api.common.base.Filter\x12:\n\tpaginated\x18\x06 \x01(\x0b\x32\'.pro.omni.oms.api.common.base.Paginated\x12\x36\n\x07\x63ontext\x18\x07 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xdf\x01\n\x14\x43\x61tegoryReadResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard\x12\x39\n\tmeta_data\x18\x02 \x01(\x0b\x32&.pro.omni.oms.api.common.base.MetaData\x12\x41\n\ncategories\x18\x03 \x03(\x0b\x32-.pro.omni.oms.api.v1.catalogs.family.Category2\x8d\x13\n\rFamilyService\x12\x85\x01\n\x0c\x46\x61milyCreate\x12\x38.pro.omni.oms.api.v1.catalogs.family.FamilyCreateRequest\x1a\x39.pro.omni.oms.api.v1.catalogs.family.FamilyCreateResponse"\x00\x12\x7f\n\nFamilyRead\x12\x36.pro.omni.oms.api.v1.catalogs.family.FamilyReadRequest\x1a\x37.pro.omni.oms.api.v1.catalogs.family.FamilyReadResponse"\x00\x12\x85\x01\n\x0c\x46\x61milyUpdate\x12\x38.pro.omni.oms.api.v1.catalogs.family.FamilyUpdateRequest\x1a\x39.pro.omni.oms.api.v1.catalogs.family.FamilyUpdateResponse"\x00\x12\x85\x01\n\x0c\x46\x61milyDelete\x12\x38.pro.omni.oms.api.v1.catalogs.family.FamilyDeleteRequest\x1a\x39.pro.omni.oms.api.v1.catalogs.family.FamilyDeleteResponse"\x00\x12\x82\x01\n\x0bGroupCreate\x12\x37.pro.omni.oms.api.v1.catalogs.family.GroupCreateRequest\x1a\x38.pro.omni.oms.api.v1.catalogs.family.GroupCreateResponse"\x00\x12|\n\tGroupRead\x12\x35.pro.omni.oms.api.v1.catalogs.family.GroupReadRequest\x1a\x36.pro.omni.oms.api.v1.catalogs.family.GroupReadResponse"\x00\x12\x82\x01\n\x0bGroupUpdate\x12\x37.pro.omni.oms.api.v1.catalogs.family.GroupUpdateRequest\x1a\x38.pro.omni.oms.api.v1.catalogs.family.GroupUpdateResponse"\x00\x12\x82\x01\n\x0bGroupDelete\x12\x37.pro.omni.oms.api.v1.catalogs.family.GroupDeleteRequest\x1a\x38.pro.omni.oms.api.v1.catalogs.family.GroupDeleteResponse"\x00\x12\x8e\x01\n\x0f\x41ttributeCreate\x12;.pro.omni.oms.api.v1.catalogs.family.AttributeCreateRequest\x1a<.pro.omni.oms.api.v1.catalogs.family.AttributeCreateResponse"\x00\x12\x88\x01\n\rAttributeRead\x12\x39.pro.omni.oms.api.v1.catalogs.family.AttributeReadRequest\x1a:.pro.omni.oms.api.v1.catalogs.family.AttributeReadResponse"\x00\x12\x8e\x01\n\x0f\x41ttributeUpdate\x12;.pro.omni.oms.api.v1.catalogs.family.AttributeUpdateRequest\x1a<.pro.omni.oms.api.v1.catalogs.family.AttributeUpdateResponse"\x00\x12\x8e\x01\n\x0f\x41ttributeDelete\x12;.pro.omni.oms.api.v1.catalogs.family.AttributeDeleteRequest\x1a<.pro.omni.oms.api.v1.catalogs.family.AttributeDeleteResponse"\x00\x12\xa3\x01\n\x16\x41ttributeVariantCreate\x12\x42.pro.omni.oms.api.v1.catalogs.family.AttributeVariantCreateRequest\x1a\x43.pro.omni.oms.api.v1.catalogs.family.AttributeVariantCreateResponse"\x00\x12\x9d\x01\n\x14\x41ttributeVariantRead\x12@.pro.omni.oms.api.v1.catalogs.family.AttributeVariantReadRequest\x1a\x41.pro.omni.oms.api.v1.catalogs.family.AttributeVariantReadResponse"\x00\x12\xa3\x01\n\x16\x41ttributeVariantUpdate\x12\x42.pro.omni.oms.api.v1.catalogs.family.AttributeVariantUpdateRequest\x1a\x43.pro.omni.oms.api.v1.catalogs.family.AttributeVariantUpdateResponse"\x00\x12\xa3\x01\n\x16\x41ttributeVariantDelete\x12\x42.pro.omni.oms.api.v1.catalogs.family.AttributeVariantDeleteRequest\x1a\x43.pro.omni.oms.api.v1.catalogs.family.AttributeVariantDeleteResponse"\x00\x12\x85\x01\n\x0c\x43\x61tegoryRead\x12\x38.pro.omni.oms.api.v1.catalogs.family.CategoryReadRequest\x1a\x39.pro.omni.oms.api.v1.catalogs.family.CategoryReadResponse"\x00\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "v1.catalogs.family_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals["_FAMILY"]._serialized_start = 147
    _globals["_FAMILY"]._serialized_end = 561
    _globals["_FAMILYCREATEREQUEST"]._serialized_start = 564
    _globals["_FAMILYCREATEREQUEST"]._serialized_end = 746
    _globals["_FAMILYCREATERESPONSE"]._serialized_start = 749
    _globals["_FAMILYCREATERESPONSE"]._serialized_end = 907
    _globals["_FAMILYREADREQUEST"]._serialized_start = 910
    _globals["_FAMILYREADREQUEST"]._serialized_end = 1277
    _globals["_FAMILYREADRESPONSE"]._serialized_start = 1280
    _globals["_FAMILYREADRESPONSE"]._serialized_end = 1553
    _globals["_FAMILYUPDATEREQUEST"]._serialized_start = 1556
    _globals["_FAMILYUPDATEREQUEST"]._serialized_end = 1694
    _globals["_FAMILYUPDATERESPONSE"]._serialized_start = 1697
    _globals["_FAMILYUPDATERESPONSE"]._serialized_end = 1855
    _globals["_FAMILYDELETEREQUEST"]._serialized_start = 1857
    _globals["_FAMILYDELETEREQUEST"]._serialized_end = 1946
    _globals["_FAMILYDELETERESPONSE"]._serialized_start = 1948
    _globals["_FAMILYDELETERESPONSE"]._serialized_end = 2045
    _globals["_ATTRIBUTE"]._serialized_start = 2048
    _globals["_ATTRIBUTE"]._serialized_end = 2326
    _globals["_ATTRIBUTECREATEREQUEST"]._serialized_start = 2329
    _globals["_ATTRIBUTECREATEREQUEST"]._serialized_end = 2590
    _globals["_ATTRIBUTECREATERESPONSE"]._serialized_start = 2593
    _globals["_ATTRIBUTECREATERESPONSE"]._serialized_end = 2760
    _globals["_ATTRIBUTEREADREQUEST"]._serialized_start = 2763
    _globals["_ATTRIBUTEREADREQUEST"]._serialized_end = 3174
    _globals["_ATTRIBUTEREADRESPONSE"]._serialized_start = 3177
    _globals["_ATTRIBUTEREADRESPONSE"]._serialized_end = 3402
    _globals["_ATTRIBUTEUPDATEREQUEST"]._serialized_start = 3405
    _globals["_ATTRIBUTEUPDATEREQUEST"]._serialized_end = 3552
    _globals["_ATTRIBUTEUPDATERESPONSE"]._serialized_start = 3555
    _globals["_ATTRIBUTEUPDATERESPONSE"]._serialized_end = 3722
    _globals["_ATTRIBUTEDELETEREQUEST"]._serialized_start = 3725
    _globals["_ATTRIBUTEDELETEREQUEST"]._serialized_end = 3858
    _globals["_ATTRIBUTEDELETERESPONSE"]._serialized_start = 3860
    _globals["_ATTRIBUTEDELETERESPONSE"]._serialized_end = 3960
    _globals["_GROUP"]._serialized_start = 3963
    _globals["_GROUP"]._serialized_end = 4172
    _globals["_GROUPCREATEREQUEST"]._serialized_start = 4175
    _globals["_GROUPCREATEREQUEST"]._serialized_end = 4319
    _globals["_GROUPCREATERESPONSE"]._serialized_start = 4322
    _globals["_GROUPCREATERESPONSE"]._serialized_end = 4477
    _globals["_GROUPREADREQUEST"]._serialized_start = 4480
    _globals["_GROUPREADREQUEST"]._serialized_end = 4867
    _globals["_GROUPREADRESPONSE"]._serialized_start = 4870
    _globals["_GROUPREADRESPONSE"]._serialized_end = 5083
    _globals["_GROUPUPDATEREQUEST"]._serialized_start = 5086
    _globals["_GROUPUPDATEREQUEST"]._serialized_end = 5240
    _globals["_GROUPUPDATERESPONSE"]._serialized_start = 5243
    _globals["_GROUPUPDATERESPONSE"]._serialized_end = 5398
    _globals["_GROUPDELETEREQUEST"]._serialized_start = 5400
    _globals["_GROUPDELETEREQUEST"]._serialized_end = 5509
    _globals["_GROUPDELETERESPONSE"]._serialized_start = 5511
    _globals["_GROUPDELETERESPONSE"]._serialized_end = 5607
    _globals["_ATTRIBUTEVARIANT"]._serialized_start = 5610
    _globals["_ATTRIBUTEVARIANT"]._serialized_end = 5774
    _globals["_ATTRIBUTEVARIANTCREATEREQUEST"]._serialized_start = 5777
    _globals["_ATTRIBUTEVARIANTCREATEREQUEST"]._serialized_end = 5946
    _globals["_ATTRIBUTEVARIANTCREATERESPONSE"]._serialized_start = 5949
    _globals["_ATTRIBUTEVARIANTCREATERESPONSE"]._serialized_end = 6138
    _globals["_ATTRIBUTEVARIANTREADREQUEST"]._serialized_start = 6141
    _globals["_ATTRIBUTEVARIANTREADREQUEST"]._serialized_end = 6549
    _globals["_ATTRIBUTEVARIANTREADRESPONSE"]._serialized_start = 6552
    _globals["_ATTRIBUTEVARIANTREADRESPONSE"]._serialized_end = 6799
    _globals["_ATTRIBUTEVARIANTUPDATEREQUEST"]._serialized_start = 6802
    _globals["_ATTRIBUTEVARIANTUPDATEREQUEST"]._serialized_end = 6985
    _globals["_ATTRIBUTEVARIANTUPDATERESPONSE"]._serialized_start = 6988
    _globals["_ATTRIBUTEVARIANTUPDATERESPONSE"]._serialized_end = 7177
    _globals["_ATTRIBUTEVARIANTDELETEREQUEST"]._serialized_start = 7180
    _globals["_ATTRIBUTEVARIANTDELETEREQUEST"]._serialized_end = 7310
    _globals["_ATTRIBUTEVARIANTDELETERESPONSE"]._serialized_start = 7312
    _globals["_ATTRIBUTEVARIANTDELETERESPONSE"]._serialized_end = 7419
    _globals["_CATEGORY"]._serialized_start = 7422
    _globals["_CATEGORY"]._serialized_end = 7597
    _globals["_CATEGORYREADREQUEST"]._serialized_start = 7600
    _globals["_CATEGORYREADREQUEST"]._serialized_end = 7957
    _globals["_CATEGORYREADRESPONSE"]._serialized_start = 7960
    _globals["_CATEGORYREADRESPONSE"]._serialized_end = 8183
    _globals["_FAMILYSERVICE"]._serialized_start = 8186
    _globals["_FAMILYSERVICE"]._serialized_end = 10631
# @@protoc_insertion_point(module_scope)
