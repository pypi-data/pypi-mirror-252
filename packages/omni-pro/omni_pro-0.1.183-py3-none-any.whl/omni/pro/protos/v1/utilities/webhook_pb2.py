# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: v1/utilities/webhook.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from omni.pro.protos.common import base_pb2 as common_dot_base__pb2
from omni.pro.protos.v1.utilities import event_pb2 as v1_dot_utilities_dot_event__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x1av1/utilities/webhook.proto\x12%pro.omni.oms.api.v1.utilities.webhook\x1a\x11\x63ommon/base.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x18v1/utilities/event.proto"\x93\x02\n\x07Webhook\x12\n\n\x02id\x18\x01 \x01(\t\x12\x39\n\x05\x65vent\x18\x02 \x01(\x0b\x32*.pro.omni.oms.api.v1.utilities.event.Event\x12\x0b\n\x03url\x18\x03 \x01(\t\x12\x0e\n\x06method\x18\x04 \x01(\t\x12\x0e\n\x06\x66ormat\x18\x05 \x01(\t\x12\'\n\x03log\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12*\n\x06\x61\x63tive\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12?\n\x0cobject_audit\x18\x08 \x01(\x0b\x32).pro.omni.oms.api.common.base.ObjectAudit"\xb6\x01\n\x14WebhookCreateRequest\x12\x10\n\x08\x65vent_id\x18\x01 \x01(\t\x12\x0b\n\x03url\x18\x02 \x01(\t\x12\x0e\n\x06method\x18\x03 \x01(\t\x12\x0e\n\x06\x66ormat\x18\x04 \x01(\t\x12\'\n\x03log\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12\x36\n\x07\x63ontext\x18\x06 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xa3\x01\n\x15WebhookCreateResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard\x12?\n\x07webhook\x18\x02 \x01(\x0b\x32..pro.omni.oms.api.v1.utilities.webhook.Webhook"\xf0\x02\n\x12WebhookReadRequest\x12\x37\n\x08group_by\x18\x01 \x03(\x0b\x32%.pro.omni.oms.api.common.base.GroupBy\x12\x35\n\x07sort_by\x18\x02 \x01(\x0b\x32$.pro.omni.oms.api.common.base.SortBy\x12\x34\n\x06\x66ields\x18\x03 \x01(\x0b\x32$.pro.omni.oms.api.common.base.Fields\x12\x34\n\x06\x66ilter\x18\x04 \x01(\x0b\x32$.pro.omni.oms.api.common.base.Filter\x12:\n\tpaginated\x18\x05 \x01(\x0b\x32\'.pro.omni.oms.api.common.base.Paginated\x12\n\n\x02id\x18\x06 \x01(\t\x12\x36\n\x07\x63ontext\x18\x07 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xdd\x01\n\x13WebhookReadResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard\x12\x39\n\tmeta_data\x18\x02 \x01(\x0b\x32&.pro.omni.oms.api.common.base.MetaData\x12@\n\x08webhooks\x18\x03 \x03(\x0b\x32..pro.omni.oms.api.v1.utilities.webhook.Webhook"\x8f\x01\n\x14WebhookUpdateRequest\x12?\n\x07webhook\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.v1.utilities.webhook.Webhook\x12\x36\n\x07\x63ontext\x18\x02 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xa3\x01\n\x15WebhookUpdateResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard\x12?\n\x07webhook\x18\x02 \x01(\x0b\x32..pro.omni.oms.api.v1.utilities.webhook.Webhook"Z\n\x14WebhookDeleteRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x36\n\x07\x63ontext\x18\x02 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"b\n\x15WebhookDeleteResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard2\xc6\x04\n\x0eWebhookService\x12\x8c\x01\n\rWebhookCreate\x12;.pro.omni.oms.api.v1.utilities.webhook.WebhookCreateRequest\x1a<.pro.omni.oms.api.v1.utilities.webhook.WebhookCreateResponse"\x00\x12\x86\x01\n\x0bWebhookRead\x12\x39.pro.omni.oms.api.v1.utilities.webhook.WebhookReadRequest\x1a:.pro.omni.oms.api.v1.utilities.webhook.WebhookReadResponse"\x00\x12\x8c\x01\n\rWebhookUpdate\x12;.pro.omni.oms.api.v1.utilities.webhook.WebhookUpdateRequest\x1a<.pro.omni.oms.api.v1.utilities.webhook.WebhookUpdateResponse"\x00\x12\x8c\x01\n\rWebhookDelete\x12;.pro.omni.oms.api.v1.utilities.webhook.WebhookDeleteRequest\x1a<.pro.omni.oms.api.v1.utilities.webhook.WebhookDeleteResponse"\x00\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "v1.utilities.webhook_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals["_WEBHOOK"]._serialized_start = 147
    _globals["_WEBHOOK"]._serialized_end = 422
    _globals["_WEBHOOKCREATEREQUEST"]._serialized_start = 425
    _globals["_WEBHOOKCREATEREQUEST"]._serialized_end = 607
    _globals["_WEBHOOKCREATERESPONSE"]._serialized_start = 610
    _globals["_WEBHOOKCREATERESPONSE"]._serialized_end = 773
    _globals["_WEBHOOKREADREQUEST"]._serialized_start = 776
    _globals["_WEBHOOKREADREQUEST"]._serialized_end = 1144
    _globals["_WEBHOOKREADRESPONSE"]._serialized_start = 1147
    _globals["_WEBHOOKREADRESPONSE"]._serialized_end = 1368
    _globals["_WEBHOOKUPDATEREQUEST"]._serialized_start = 1371
    _globals["_WEBHOOKUPDATEREQUEST"]._serialized_end = 1514
    _globals["_WEBHOOKUPDATERESPONSE"]._serialized_start = 1517
    _globals["_WEBHOOKUPDATERESPONSE"]._serialized_end = 1680
    _globals["_WEBHOOKDELETEREQUEST"]._serialized_start = 1682
    _globals["_WEBHOOKDELETEREQUEST"]._serialized_end = 1772
    _globals["_WEBHOOKDELETERESPONSE"]._serialized_start = 1774
    _globals["_WEBHOOKDELETERESPONSE"]._serialized_end = 1872
    _globals["_WEBHOOKSERVICE"]._serialized_start = 1875
    _globals["_WEBHOOKSERVICE"]._serialized_end = 2457
# @@protoc_insertion_point(module_scope)
