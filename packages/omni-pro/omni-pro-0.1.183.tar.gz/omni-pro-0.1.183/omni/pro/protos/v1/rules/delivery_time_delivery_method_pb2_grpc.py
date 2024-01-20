# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from omni.pro.protos.v1.rules import (
    delivery_time_delivery_method_pb2 as v1_dot_rules_dot_delivery__time__delivery__method__pb2,
)


class DeliveryTimeDeliveryMethodServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.DeliveryTimeDeliveryMethodCreate = channel.unary_unary(
            "/pro.omni.oms.api.v1.rules.delivery_time_delivery_method.DeliveryTimeDeliveryMethodService/DeliveryTimeDeliveryMethodCreate",
            request_serializer=v1_dot_rules_dot_delivery__time__delivery__method__pb2.DeliveryTimeDeliveryMethodCreateRequest.SerializeToString,
            response_deserializer=v1_dot_rules_dot_delivery__time__delivery__method__pb2.DeliveryTimeDeliveryMethodCreateResponse.FromString,
        )
        self.DeliveryTimeDeliveryMethodRead = channel.unary_unary(
            "/pro.omni.oms.api.v1.rules.delivery_time_delivery_method.DeliveryTimeDeliveryMethodService/DeliveryTimeDeliveryMethodRead",
            request_serializer=v1_dot_rules_dot_delivery__time__delivery__method__pb2.DeliveryTimeDeliveryMethodReadRequest.SerializeToString,
            response_deserializer=v1_dot_rules_dot_delivery__time__delivery__method__pb2.DeliveryTimeDeliveryMethodReadResponse.FromString,
        )
        self.DeliveryTimeDeliveryMethodUpdate = channel.unary_unary(
            "/pro.omni.oms.api.v1.rules.delivery_time_delivery_method.DeliveryTimeDeliveryMethodService/DeliveryTimeDeliveryMethodUpdate",
            request_serializer=v1_dot_rules_dot_delivery__time__delivery__method__pb2.DeliveryTimeDeliveryMethodUpdateRequest.SerializeToString,
            response_deserializer=v1_dot_rules_dot_delivery__time__delivery__method__pb2.DeliveryTimeDeliveryMethodUpdateResponse.FromString,
        )
        self.DeliveryTimeDeliveryMethodDelete = channel.unary_unary(
            "/pro.omni.oms.api.v1.rules.delivery_time_delivery_method.DeliveryTimeDeliveryMethodService/DeliveryTimeDeliveryMethodDelete",
            request_serializer=v1_dot_rules_dot_delivery__time__delivery__method__pb2.DeliveryTimeDeliveryMethodDeleteRequest.SerializeToString,
            response_deserializer=v1_dot_rules_dot_delivery__time__delivery__method__pb2.DeliveryTimeDeliveryMethodDeleteResponse.FromString,
        )


class DeliveryTimeDeliveryMethodServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def DeliveryTimeDeliveryMethodCreate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def DeliveryTimeDeliveryMethodRead(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def DeliveryTimeDeliveryMethodUpdate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def DeliveryTimeDeliveryMethodDelete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_DeliveryTimeDeliveryMethodServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "DeliveryTimeDeliveryMethodCreate": grpc.unary_unary_rpc_method_handler(
            servicer.DeliveryTimeDeliveryMethodCreate,
            request_deserializer=v1_dot_rules_dot_delivery__time__delivery__method__pb2.DeliveryTimeDeliveryMethodCreateRequest.FromString,
            response_serializer=v1_dot_rules_dot_delivery__time__delivery__method__pb2.DeliveryTimeDeliveryMethodCreateResponse.SerializeToString,
        ),
        "DeliveryTimeDeliveryMethodRead": grpc.unary_unary_rpc_method_handler(
            servicer.DeliveryTimeDeliveryMethodRead,
            request_deserializer=v1_dot_rules_dot_delivery__time__delivery__method__pb2.DeliveryTimeDeliveryMethodReadRequest.FromString,
            response_serializer=v1_dot_rules_dot_delivery__time__delivery__method__pb2.DeliveryTimeDeliveryMethodReadResponse.SerializeToString,
        ),
        "DeliveryTimeDeliveryMethodUpdate": grpc.unary_unary_rpc_method_handler(
            servicer.DeliveryTimeDeliveryMethodUpdate,
            request_deserializer=v1_dot_rules_dot_delivery__time__delivery__method__pb2.DeliveryTimeDeliveryMethodUpdateRequest.FromString,
            response_serializer=v1_dot_rules_dot_delivery__time__delivery__method__pb2.DeliveryTimeDeliveryMethodUpdateResponse.SerializeToString,
        ),
        "DeliveryTimeDeliveryMethodDelete": grpc.unary_unary_rpc_method_handler(
            servicer.DeliveryTimeDeliveryMethodDelete,
            request_deserializer=v1_dot_rules_dot_delivery__time__delivery__method__pb2.DeliveryTimeDeliveryMethodDeleteRequest.FromString,
            response_serializer=v1_dot_rules_dot_delivery__time__delivery__method__pb2.DeliveryTimeDeliveryMethodDeleteResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "pro.omni.oms.api.v1.rules.delivery_time_delivery_method.DeliveryTimeDeliveryMethodService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class DeliveryTimeDeliveryMethodService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def DeliveryTimeDeliveryMethodCreate(
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
            "/pro.omni.oms.api.v1.rules.delivery_time_delivery_method.DeliveryTimeDeliveryMethodService/DeliveryTimeDeliveryMethodCreate",
            v1_dot_rules_dot_delivery__time__delivery__method__pb2.DeliveryTimeDeliveryMethodCreateRequest.SerializeToString,
            v1_dot_rules_dot_delivery__time__delivery__method__pb2.DeliveryTimeDeliveryMethodCreateResponse.FromString,
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
    def DeliveryTimeDeliveryMethodRead(
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
            "/pro.omni.oms.api.v1.rules.delivery_time_delivery_method.DeliveryTimeDeliveryMethodService/DeliveryTimeDeliveryMethodRead",
            v1_dot_rules_dot_delivery__time__delivery__method__pb2.DeliveryTimeDeliveryMethodReadRequest.SerializeToString,
            v1_dot_rules_dot_delivery__time__delivery__method__pb2.DeliveryTimeDeliveryMethodReadResponse.FromString,
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
    def DeliveryTimeDeliveryMethodUpdate(
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
            "/pro.omni.oms.api.v1.rules.delivery_time_delivery_method.DeliveryTimeDeliveryMethodService/DeliveryTimeDeliveryMethodUpdate",
            v1_dot_rules_dot_delivery__time__delivery__method__pb2.DeliveryTimeDeliveryMethodUpdateRequest.SerializeToString,
            v1_dot_rules_dot_delivery__time__delivery__method__pb2.DeliveryTimeDeliveryMethodUpdateResponse.FromString,
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
    def DeliveryTimeDeliveryMethodDelete(
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
            "/pro.omni.oms.api.v1.rules.delivery_time_delivery_method.DeliveryTimeDeliveryMethodService/DeliveryTimeDeliveryMethodDelete",
            v1_dot_rules_dot_delivery__time__delivery__method__pb2.DeliveryTimeDeliveryMethodDeleteRequest.SerializeToString,
            v1_dot_rules_dot_delivery__time__delivery__method__pb2.DeliveryTimeDeliveryMethodDeleteResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
