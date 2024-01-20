# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from omni.pro.protos.v1.utilities import territory_matrix_pb2 as v1_dot_utilities_dot_territory__matrix__pb2


class TerritoryMatrixServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.TerritoryMatrixAdd = channel.unary_unary(
            "/pro.omni.oms.api.v1.utilities.territory_matrix.TerritoryMatrixService/TerritoryMatrixAdd",
            request_serializer=v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixAddRequest.SerializeToString,
            response_deserializer=v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixAddResponse.FromString,
        )
        self.TerritoryMatrixRead = channel.unary_unary(
            "/pro.omni.oms.api.v1.utilities.territory_matrix.TerritoryMatrixService/TerritoryMatrixRead",
            request_serializer=v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixReadRequest.SerializeToString,
            response_deserializer=v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixReadResponse.FromString,
        )
        self.TerritoryMatrixUpdate = channel.unary_unary(
            "/pro.omni.oms.api.v1.utilities.territory_matrix.TerritoryMatrixService/TerritoryMatrixUpdate",
            request_serializer=v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixUpdateRequest.SerializeToString,
            response_deserializer=v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixUpdateResponse.FromString,
        )
        self.TerritoryMatrixDelete = channel.unary_unary(
            "/pro.omni.oms.api.v1.utilities.territory_matrix.TerritoryMatrixService/TerritoryMatrixDelete",
            request_serializer=v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixDeleteRequest.SerializeToString,
            response_deserializer=v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixDeleteResponse.FromString,
        )
        self.TerritoryMatrixLoad = channel.unary_unary(
            "/pro.omni.oms.api.v1.utilities.territory_matrix.TerritoryMatrixService/TerritoryMatrixLoad",
            request_serializer=v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixLoadRequest.SerializeToString,
            response_deserializer=v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixLoadResponse.FromString,
        )
        self.TerritoryMatrixStructure = channel.unary_unary(
            "/pro.omni.oms.api.v1.utilities.territory_matrix.TerritoryMatrixService/TerritoryMatrixStructure",
            request_serializer=v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixStructureRequest.SerializeToString,
            response_deserializer=v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixStructureResponse.FromString,
        )


class TerritoryMatrixServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def TerritoryMatrixAdd(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def TerritoryMatrixRead(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def TerritoryMatrixUpdate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def TerritoryMatrixDelete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def TerritoryMatrixLoad(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def TerritoryMatrixStructure(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_TerritoryMatrixServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "TerritoryMatrixAdd": grpc.unary_unary_rpc_method_handler(
            servicer.TerritoryMatrixAdd,
            request_deserializer=v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixAddRequest.FromString,
            response_serializer=v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixAddResponse.SerializeToString,
        ),
        "TerritoryMatrixRead": grpc.unary_unary_rpc_method_handler(
            servicer.TerritoryMatrixRead,
            request_deserializer=v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixReadRequest.FromString,
            response_serializer=v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixReadResponse.SerializeToString,
        ),
        "TerritoryMatrixUpdate": grpc.unary_unary_rpc_method_handler(
            servicer.TerritoryMatrixUpdate,
            request_deserializer=v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixUpdateRequest.FromString,
            response_serializer=v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixUpdateResponse.SerializeToString,
        ),
        "TerritoryMatrixDelete": grpc.unary_unary_rpc_method_handler(
            servicer.TerritoryMatrixDelete,
            request_deserializer=v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixDeleteRequest.FromString,
            response_serializer=v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixDeleteResponse.SerializeToString,
        ),
        "TerritoryMatrixLoad": grpc.unary_unary_rpc_method_handler(
            servicer.TerritoryMatrixLoad,
            request_deserializer=v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixLoadRequest.FromString,
            response_serializer=v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixLoadResponse.SerializeToString,
        ),
        "TerritoryMatrixStructure": grpc.unary_unary_rpc_method_handler(
            servicer.TerritoryMatrixStructure,
            request_deserializer=v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixStructureRequest.FromString,
            response_serializer=v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixStructureResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "pro.omni.oms.api.v1.utilities.territory_matrix.TerritoryMatrixService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class TerritoryMatrixService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def TerritoryMatrixAdd(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/pro.omni.oms.api.v1.utilities.territory_matrix.TerritoryMatrixService/TerritoryMatrixAdd",
            v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixAddRequest.SerializeToString,
            v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixAddResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def TerritoryMatrixRead(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/pro.omni.oms.api.v1.utilities.territory_matrix.TerritoryMatrixService/TerritoryMatrixRead",
            v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixReadRequest.SerializeToString,
            v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixReadResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def TerritoryMatrixUpdate(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/pro.omni.oms.api.v1.utilities.territory_matrix.TerritoryMatrixService/TerritoryMatrixUpdate",
            v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixUpdateRequest.SerializeToString,
            v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixUpdateResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def TerritoryMatrixDelete(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/pro.omni.oms.api.v1.utilities.territory_matrix.TerritoryMatrixService/TerritoryMatrixDelete",
            v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixDeleteRequest.SerializeToString,
            v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixDeleteResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def TerritoryMatrixLoad(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/pro.omni.oms.api.v1.utilities.territory_matrix.TerritoryMatrixService/TerritoryMatrixLoad",
            v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixLoadRequest.SerializeToString,
            v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixLoadResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def TerritoryMatrixStructure(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/pro.omni.oms.api.v1.utilities.territory_matrix.TerritoryMatrixService/TerritoryMatrixStructure",
            v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixStructureRequest.SerializeToString,
            v1_dot_utilities_dot_territory__matrix__pb2.TerritoryMatrixStructureResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
