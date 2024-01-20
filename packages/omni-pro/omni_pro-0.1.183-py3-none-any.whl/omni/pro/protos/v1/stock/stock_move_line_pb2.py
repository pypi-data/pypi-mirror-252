# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: v1/stock/stock_move_line.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from omni.pro.protos.common import base_pb2 as common_dot_base__pb2
from omni.pro.protos.v1.stock import location_pb2 as v1_dot_stock_dot_location__pb2
from omni.pro.protos.v1.stock import picking_pb2 as v1_dot_stock_dot_picking__pb2
from omni.pro.protos.v1.stock import product_pb2 as v1_dot_stock_dot_product__pb2
from omni.pro.protos.v1.stock import stock_move_pb2 as v1_dot_stock_dot_stock__move__pb2
from omni.pro.protos.v1.stock import uom_pb2 as v1_dot_stock_dot_uom__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x1ev1/stock/stock_move_line.proto\x12)pro.omni.oms.api.v1.stock.stock_move_line\x1a\x11\x63ommon/base.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x12v1/stock/uom.proto\x1a\x17v1/stock/location.proto\x1a\x16v1/stock/picking.proto\x1a\x19v1/stock/stock_move.proto\x1a\x16v1/stock/product.proto"\xb7\x05\n\rStockMoveLine\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x43\n\nstock_move\x18\x02 \x01(\x0b\x32/.pro.omni.oms.api.v1.stock.stock_move.StockMove\x12;\n\x07picking\x18\x03 \x01(\x0b\x32*.pro.omni.oms.api.v1.stock.picking.Picking\x12\r\n\x05state\x18\x04 \x01(\t\x12\x11\n\treference\x18\x05 \x01(\t\x12(\n\x04\x64\x61te\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0e\n\x06origin\x18\x07 \x01(\t\x12;\n\x07product\x18\x08 \x01(\x0b\x32*.pro.omni.oms.api.v1.stock.product.Product\x12>\n\x08location\x18\t \x01(\x0b\x32,.pro.omni.oms.api.v1.stock.location.Location\x12\x43\n\rlocation_dest\x18\n \x01(\x0b\x32,.pro.omni.oms.api.v1.stock.location.Location\x12\x10\n\x08qty_done\x18\x0b \x01(\x02\x12\x17\n\x0fproduct_uom_qty\x18\x0c \x01(\x02\x12\x37\n\x0bproduct_uom\x18\r \x01(\x0b\x32".pro.omni.oms.api.v1.stock.uom.Uom\x12\x14\n\x0cqty_reserved\x18\x0e \x01(\x02\x12*\n\x06\x61\x63tive\x18\x0f \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12\x13\n\x0b\x65xternal_id\x18\x10 \x01(\t\x12?\n\x0cobject_audit\x18\x11 \x01(\x0b\x32).pro.omni.oms.api.common.base.ObjectAudit"\x8c\x03\n\x1aStockMoveLineCreateRequest\x12\x15\n\rstock_move_id\x18\x01 \x01(\x05\x12\x12\n\npicking_id\x18\x02 \x01(\x05\x12\r\n\x05state\x18\x03 \x01(\t\x12\x11\n\treference\x18\x04 \x01(\t\x12(\n\x04\x64\x61te\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0e\n\x06origin\x18\x06 \x01(\t\x12\x12\n\nproduct_id\x18\x07 \x01(\t\x12\x13\n\x0blocation_id\x18\x08 \x01(\x05\x12\x18\n\x10location_dest_id\x18\t \x01(\x05\x12\x10\n\x08qty_done\x18\n \x01(\x02\x12\x17\n\x0fproduct_uom_qty\x18\x0b \x01(\x02\x12\x16\n\x0eproduct_uom_id\x18\x0c \x01(\t\x12\x14\n\x0cqty_reserved\x18\r \x01(\x02\x12\x13\n\x0b\x65xternal_id\x18\x0e \x01(\t\x12\x36\n\x07\x63ontext\x18\x0f \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xbb\x01\n\x1bStockMoveLineCreateResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard\x12Q\n\x0fstock_move_line\x18\x02 \x01(\x0b\x32\x38.pro.omni.oms.api.v1.stock.stock_move_line.StockMoveLine"\xf6\x02\n\x18StockMoveLineReadRequest\x12\x37\n\x08group_by\x18\x01 \x03(\x0b\x32%.pro.omni.oms.api.common.base.GroupBy\x12\x35\n\x07sort_by\x18\x02 \x01(\x0b\x32$.pro.omni.oms.api.common.base.SortBy\x12\x34\n\x06\x66ields\x18\x03 \x01(\x0b\x32$.pro.omni.oms.api.common.base.Fields\x12\x34\n\x06\x66ilter\x18\x04 \x01(\x0b\x32$.pro.omni.oms.api.common.base.Filter\x12:\n\tpaginated\x18\x05 \x01(\x0b\x32\'.pro.omni.oms.api.common.base.Paginated\x12\n\n\x02id\x18\x06 \x01(\x05\x12\x36\n\x07\x63ontext\x18\x07 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xf5\x01\n\x19StockMoveLineReadResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard\x12\x39\n\tmeta_data\x18\x02 \x01(\x0b\x32&.pro.omni.oms.api.common.base.MetaData\x12R\n\x10stock_move_lines\x18\x03 \x03(\x0b\x32\x38.pro.omni.oms.api.v1.stock.stock_move_line.StockMoveLine"\xa7\x01\n\x1aStockMoveLineUpdateRequest\x12Q\n\x0fstock_move_line\x18\x01 \x01(\x0b\x32\x38.pro.omni.oms.api.v1.stock.stock_move_line.StockMoveLine\x12\x36\n\x07\x63ontext\x18\x02 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\xbb\x01\n\x1bStockMoveLineUpdateResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard\x12Q\n\x0fstock_move_line\x18\x02 \x01(\x0b\x32\x38.pro.omni.oms.api.v1.stock.stock_move_line.StockMoveLine"`\n\x1aStockMoveLineDeleteRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x36\n\x07\x63ontext\x18\x02 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"h\n\x1bStockMoveLineDeleteResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard"\x97\x01\n\x15MoveLineAddQtyRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x10\n\x08quantity\x18\x02 \x01(\x05\x12(\n\x07payload\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x36\n\x07\x63ontext\x18\x04 \x01(\x0b\x32%.pro.omni.oms.api.common.base.Context"\x8a\x01\n\x16MoveLineAddQtyResponse\x12I\n\x11response_standard\x18\x01 \x01(\x0b\x32..pro.omni.oms.api.common.base.ResponseStandard\x12%\n\x04\x64\x61ta\x18\x02 \x01(\x0b\x32\x17.google.protobuf.Struct2\xc6\x06\n\x14StockMoveLineService\x12\xa4\x01\n\x13StockMoveLineCreate\x12\x45.pro.omni.oms.api.v1.stock.stock_move_line.StockMoveLineCreateRequest\x1a\x46.pro.omni.oms.api.v1.stock.stock_move_line.StockMoveLineCreateResponse\x12\x9e\x01\n\x11StockMoveLineRead\x12\x43.pro.omni.oms.api.v1.stock.stock_move_line.StockMoveLineReadRequest\x1a\x44.pro.omni.oms.api.v1.stock.stock_move_line.StockMoveLineReadResponse\x12\xa4\x01\n\x13StockMoveLineUpdate\x12\x45.pro.omni.oms.api.v1.stock.stock_move_line.StockMoveLineUpdateRequest\x1a\x46.pro.omni.oms.api.v1.stock.stock_move_line.StockMoveLineUpdateResponse\x12\xa4\x01\n\x13StockMoveLineDelete\x12\x45.pro.omni.oms.api.v1.stock.stock_move_line.StockMoveLineDeleteRequest\x1a\x46.pro.omni.oms.api.v1.stock.stock_move_line.StockMoveLineDeleteResponse\x12\x97\x01\n\x0eMoveLineAddQty\x12@.pro.omni.oms.api.v1.stock.stock_move_line.MoveLineAddQtyRequest\x1a\x41.pro.omni.oms.api.v1.stock.stock_move_line.MoveLineAddQtyResponse"\x00\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "v1.stock.stock_move_line_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals["_STOCKMOVELINE"]._serialized_start = 312
    _globals["_STOCKMOVELINE"]._serialized_end = 1007
    _globals["_STOCKMOVELINECREATEREQUEST"]._serialized_start = 1010
    _globals["_STOCKMOVELINECREATEREQUEST"]._serialized_end = 1406
    _globals["_STOCKMOVELINECREATERESPONSE"]._serialized_start = 1409
    _globals["_STOCKMOVELINECREATERESPONSE"]._serialized_end = 1596
    _globals["_STOCKMOVELINEREADREQUEST"]._serialized_start = 1599
    _globals["_STOCKMOVELINEREADREQUEST"]._serialized_end = 1973
    _globals["_STOCKMOVELINEREADRESPONSE"]._serialized_start = 1976
    _globals["_STOCKMOVELINEREADRESPONSE"]._serialized_end = 2221
    _globals["_STOCKMOVELINEUPDATEREQUEST"]._serialized_start = 2224
    _globals["_STOCKMOVELINEUPDATEREQUEST"]._serialized_end = 2391
    _globals["_STOCKMOVELINEUPDATERESPONSE"]._serialized_start = 2394
    _globals["_STOCKMOVELINEUPDATERESPONSE"]._serialized_end = 2581
    _globals["_STOCKMOVELINEDELETEREQUEST"]._serialized_start = 2583
    _globals["_STOCKMOVELINEDELETEREQUEST"]._serialized_end = 2679
    _globals["_STOCKMOVELINEDELETERESPONSE"]._serialized_start = 2681
    _globals["_STOCKMOVELINEDELETERESPONSE"]._serialized_end = 2785
    _globals["_MOVELINEADDQTYREQUEST"]._serialized_start = 2788
    _globals["_MOVELINEADDQTYREQUEST"]._serialized_end = 2939
    _globals["_MOVELINEADDQTYRESPONSE"]._serialized_start = 2942
    _globals["_MOVELINEADDQTYRESPONSE"]._serialized_end = 3080
    _globals["_STOCKMOVELINESERVICE"]._serialized_start = 3083
    _globals["_STOCKMOVELINESERVICE"]._serialized_end = 3921
# @@protoc_insertion_point(module_scope)
