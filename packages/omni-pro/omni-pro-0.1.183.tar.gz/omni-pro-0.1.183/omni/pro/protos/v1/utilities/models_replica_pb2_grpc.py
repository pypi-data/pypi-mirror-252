# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from omni.pro.protos.v1.utilities import models_replica_pb2 as v1_dot_utilities_dot_models__replica__pb2


class ModelsReplicaServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ModelsReplica = channel.unary_unary(
            "/pro.omni.oms.api.v1.utilities.models_replica.ModelsReplicaService/ModelsReplica",
            request_serializer=v1_dot_utilities_dot_models__replica__pb2.ModelsReplicaRequest.SerializeToString,
            response_deserializer=v1_dot_utilities_dot_models__replica__pb2.ModelsReplicaResponse.FromString,
        )


class ModelsReplicaServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ModelsReplica(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_ModelsReplicaServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "ModelsReplica": grpc.unary_unary_rpc_method_handler(
            servicer.ModelsReplica,
            request_deserializer=v1_dot_utilities_dot_models__replica__pb2.ModelsReplicaRequest.FromString,
            response_serializer=v1_dot_utilities_dot_models__replica__pb2.ModelsReplicaResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "pro.omni.oms.api.v1.utilities.models_replica.ModelsReplicaService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class ModelsReplicaService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ModelsReplica(
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
            "/pro.omni.oms.api.v1.utilities.models_replica.ModelsReplicaService/ModelsReplica",
            v1_dot_utilities_dot_models__replica__pb2.ModelsReplicaRequest.SerializeToString,
            v1_dot_utilities_dot_models__replica__pb2.ModelsReplicaResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
