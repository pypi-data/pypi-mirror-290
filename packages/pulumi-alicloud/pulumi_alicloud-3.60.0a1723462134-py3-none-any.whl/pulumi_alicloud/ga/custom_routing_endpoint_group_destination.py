# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['CustomRoutingEndpointGroupDestinationArgs', 'CustomRoutingEndpointGroupDestination']

@pulumi.input_type
class CustomRoutingEndpointGroupDestinationArgs:
    def __init__(__self__, *,
                 endpoint_group_id: pulumi.Input[str],
                 from_port: pulumi.Input[int],
                 protocols: pulumi.Input[Sequence[pulumi.Input[str]]],
                 to_port: pulumi.Input[int]):
        """
        The set of arguments for constructing a CustomRoutingEndpointGroupDestination resource.
        :param pulumi.Input[str] endpoint_group_id: The ID of the endpoint group.
        :param pulumi.Input[int] from_port: The start port of the backend service port range of the endpoint group. The `from_port` value must be smaller than or equal to the `to_port` value. Valid values: `1` to `65499`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] protocols: The backend service protocol of the endpoint group. Valid values: `TCP`, `UDP`, `TCP, UDP`.
        :param pulumi.Input[int] to_port: The end port of the backend service port range of the endpoint group. The `from_port` value must be smaller than or equal to the `to_port` value. Valid values: `1` to `65499`.
        """
        pulumi.set(__self__, "endpoint_group_id", endpoint_group_id)
        pulumi.set(__self__, "from_port", from_port)
        pulumi.set(__self__, "protocols", protocols)
        pulumi.set(__self__, "to_port", to_port)

    @property
    @pulumi.getter(name="endpointGroupId")
    def endpoint_group_id(self) -> pulumi.Input[str]:
        """
        The ID of the endpoint group.
        """
        return pulumi.get(self, "endpoint_group_id")

    @endpoint_group_id.setter
    def endpoint_group_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "endpoint_group_id", value)

    @property
    @pulumi.getter(name="fromPort")
    def from_port(self) -> pulumi.Input[int]:
        """
        The start port of the backend service port range of the endpoint group. The `from_port` value must be smaller than or equal to the `to_port` value. Valid values: `1` to `65499`.
        """
        return pulumi.get(self, "from_port")

    @from_port.setter
    def from_port(self, value: pulumi.Input[int]):
        pulumi.set(self, "from_port", value)

    @property
    @pulumi.getter
    def protocols(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The backend service protocol of the endpoint group. Valid values: `TCP`, `UDP`, `TCP, UDP`.
        """
        return pulumi.get(self, "protocols")

    @protocols.setter
    def protocols(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "protocols", value)

    @property
    @pulumi.getter(name="toPort")
    def to_port(self) -> pulumi.Input[int]:
        """
        The end port of the backend service port range of the endpoint group. The `from_port` value must be smaller than or equal to the `to_port` value. Valid values: `1` to `65499`.
        """
        return pulumi.get(self, "to_port")

    @to_port.setter
    def to_port(self, value: pulumi.Input[int]):
        pulumi.set(self, "to_port", value)


@pulumi.input_type
class _CustomRoutingEndpointGroupDestinationState:
    def __init__(__self__, *,
                 accelerator_id: Optional[pulumi.Input[str]] = None,
                 custom_routing_endpoint_group_destination_id: Optional[pulumi.Input[str]] = None,
                 endpoint_group_id: Optional[pulumi.Input[str]] = None,
                 from_port: Optional[pulumi.Input[int]] = None,
                 listener_id: Optional[pulumi.Input[str]] = None,
                 protocols: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 to_port: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering CustomRoutingEndpointGroupDestination resources.
        :param pulumi.Input[str] accelerator_id: The ID of the GA instance.
        :param pulumi.Input[str] custom_routing_endpoint_group_destination_id: The ID of the Custom Routing Endpoint Group Destination.
        :param pulumi.Input[str] endpoint_group_id: The ID of the endpoint group.
        :param pulumi.Input[int] from_port: The start port of the backend service port range of the endpoint group. The `from_port` value must be smaller than or equal to the `to_port` value. Valid values: `1` to `65499`.
        :param pulumi.Input[str] listener_id: The ID of the listener.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] protocols: The backend service protocol of the endpoint group. Valid values: `TCP`, `UDP`, `TCP, UDP`.
        :param pulumi.Input[str] status: The status of the Custom Routing Endpoint Group Destination.
        :param pulumi.Input[int] to_port: The end port of the backend service port range of the endpoint group. The `from_port` value must be smaller than or equal to the `to_port` value. Valid values: `1` to `65499`.
        """
        if accelerator_id is not None:
            pulumi.set(__self__, "accelerator_id", accelerator_id)
        if custom_routing_endpoint_group_destination_id is not None:
            pulumi.set(__self__, "custom_routing_endpoint_group_destination_id", custom_routing_endpoint_group_destination_id)
        if endpoint_group_id is not None:
            pulumi.set(__self__, "endpoint_group_id", endpoint_group_id)
        if from_port is not None:
            pulumi.set(__self__, "from_port", from_port)
        if listener_id is not None:
            pulumi.set(__self__, "listener_id", listener_id)
        if protocols is not None:
            pulumi.set(__self__, "protocols", protocols)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if to_port is not None:
            pulumi.set(__self__, "to_port", to_port)

    @property
    @pulumi.getter(name="acceleratorId")
    def accelerator_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the GA instance.
        """
        return pulumi.get(self, "accelerator_id")

    @accelerator_id.setter
    def accelerator_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "accelerator_id", value)

    @property
    @pulumi.getter(name="customRoutingEndpointGroupDestinationId")
    def custom_routing_endpoint_group_destination_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Custom Routing Endpoint Group Destination.
        """
        return pulumi.get(self, "custom_routing_endpoint_group_destination_id")

    @custom_routing_endpoint_group_destination_id.setter
    def custom_routing_endpoint_group_destination_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "custom_routing_endpoint_group_destination_id", value)

    @property
    @pulumi.getter(name="endpointGroupId")
    def endpoint_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the endpoint group.
        """
        return pulumi.get(self, "endpoint_group_id")

    @endpoint_group_id.setter
    def endpoint_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "endpoint_group_id", value)

    @property
    @pulumi.getter(name="fromPort")
    def from_port(self) -> Optional[pulumi.Input[int]]:
        """
        The start port of the backend service port range of the endpoint group. The `from_port` value must be smaller than or equal to the `to_port` value. Valid values: `1` to `65499`.
        """
        return pulumi.get(self, "from_port")

    @from_port.setter
    def from_port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "from_port", value)

    @property
    @pulumi.getter(name="listenerId")
    def listener_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the listener.
        """
        return pulumi.get(self, "listener_id")

    @listener_id.setter
    def listener_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "listener_id", value)

    @property
    @pulumi.getter
    def protocols(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The backend service protocol of the endpoint group. Valid values: `TCP`, `UDP`, `TCP, UDP`.
        """
        return pulumi.get(self, "protocols")

    @protocols.setter
    def protocols(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "protocols", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the Custom Routing Endpoint Group Destination.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter(name="toPort")
    def to_port(self) -> Optional[pulumi.Input[int]]:
        """
        The end port of the backend service port range of the endpoint group. The `from_port` value must be smaller than or equal to the `to_port` value. Valid values: `1` to `65499`.
        """
        return pulumi.get(self, "to_port")

    @to_port.setter
    def to_port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "to_port", value)


class CustomRoutingEndpointGroupDestination(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 endpoint_group_id: Optional[pulumi.Input[str]] = None,
                 from_port: Optional[pulumi.Input[int]] = None,
                 protocols: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 to_port: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        Provides a Global Accelerator (GA) Custom Routing Endpoint Group Destination resource.

        For information about Global Accelerator (GA) Custom Routing Endpoint Group Destination and how to use it, see [What is Custom Routing Endpoint Group Destination](https://www.alibabacloud.com/help/en/global-accelerator/latest/api-ga-2019-11-20-createcustomroutingendpointgroupdestinations).

        > **NOTE:** Available since v1.197.0.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        region = config.get("region")
        if region is None:
            region = "cn-hangzhou"
        default = alicloud.ga.Accelerator("default",
            duration=1,
            auto_use_coupon=True,
            spec="1")
        default_bandwidth_package = alicloud.ga.BandwidthPackage("default",
            bandwidth=100,
            type="Basic",
            bandwidth_type="Basic",
            payment_type="PayAsYouGo",
            billing_type="PayBy95",
            ratio=30)
        default_bandwidth_package_attachment = alicloud.ga.BandwidthPackageAttachment("default",
            accelerator_id=default.id,
            bandwidth_package_id=default_bandwidth_package.id)
        default_listener = alicloud.ga.Listener("default",
            accelerator_id=default_bandwidth_package_attachment.accelerator_id,
            listener_type="CustomRouting",
            port_ranges=[{
                "from_port": 10000,
                "to_port": 16000,
            }])
        default_custom_routing_endpoint_group = alicloud.ga.CustomRoutingEndpointGroup("default",
            accelerator_id=default_listener.accelerator_id,
            listener_id=default_listener.id,
            endpoint_group_region=region,
            custom_routing_endpoint_group_name="terraform-example",
            description="terraform-example")
        default_custom_routing_endpoint_group_destination = alicloud.ga.CustomRoutingEndpointGroupDestination("default",
            endpoint_group_id=default_custom_routing_endpoint_group.id,
            protocols=["TCP"],
            from_port=1,
            to_port=2)
        ```

        ## Import

        Global Accelerator (GA) Custom Routing Endpoint Group Destination can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:ga/customRoutingEndpointGroupDestination:CustomRoutingEndpointGroupDestination example <endpoint_group_id>:<custom_routing_endpoint_group_destination_id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] endpoint_group_id: The ID of the endpoint group.
        :param pulumi.Input[int] from_port: The start port of the backend service port range of the endpoint group. The `from_port` value must be smaller than or equal to the `to_port` value. Valid values: `1` to `65499`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] protocols: The backend service protocol of the endpoint group. Valid values: `TCP`, `UDP`, `TCP, UDP`.
        :param pulumi.Input[int] to_port: The end port of the backend service port range of the endpoint group. The `from_port` value must be smaller than or equal to the `to_port` value. Valid values: `1` to `65499`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: CustomRoutingEndpointGroupDestinationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Global Accelerator (GA) Custom Routing Endpoint Group Destination resource.

        For information about Global Accelerator (GA) Custom Routing Endpoint Group Destination and how to use it, see [What is Custom Routing Endpoint Group Destination](https://www.alibabacloud.com/help/en/global-accelerator/latest/api-ga-2019-11-20-createcustomroutingendpointgroupdestinations).

        > **NOTE:** Available since v1.197.0.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        region = config.get("region")
        if region is None:
            region = "cn-hangzhou"
        default = alicloud.ga.Accelerator("default",
            duration=1,
            auto_use_coupon=True,
            spec="1")
        default_bandwidth_package = alicloud.ga.BandwidthPackage("default",
            bandwidth=100,
            type="Basic",
            bandwidth_type="Basic",
            payment_type="PayAsYouGo",
            billing_type="PayBy95",
            ratio=30)
        default_bandwidth_package_attachment = alicloud.ga.BandwidthPackageAttachment("default",
            accelerator_id=default.id,
            bandwidth_package_id=default_bandwidth_package.id)
        default_listener = alicloud.ga.Listener("default",
            accelerator_id=default_bandwidth_package_attachment.accelerator_id,
            listener_type="CustomRouting",
            port_ranges=[{
                "from_port": 10000,
                "to_port": 16000,
            }])
        default_custom_routing_endpoint_group = alicloud.ga.CustomRoutingEndpointGroup("default",
            accelerator_id=default_listener.accelerator_id,
            listener_id=default_listener.id,
            endpoint_group_region=region,
            custom_routing_endpoint_group_name="terraform-example",
            description="terraform-example")
        default_custom_routing_endpoint_group_destination = alicloud.ga.CustomRoutingEndpointGroupDestination("default",
            endpoint_group_id=default_custom_routing_endpoint_group.id,
            protocols=["TCP"],
            from_port=1,
            to_port=2)
        ```

        ## Import

        Global Accelerator (GA) Custom Routing Endpoint Group Destination can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:ga/customRoutingEndpointGroupDestination:CustomRoutingEndpointGroupDestination example <endpoint_group_id>:<custom_routing_endpoint_group_destination_id>
        ```

        :param str resource_name: The name of the resource.
        :param CustomRoutingEndpointGroupDestinationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CustomRoutingEndpointGroupDestinationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 endpoint_group_id: Optional[pulumi.Input[str]] = None,
                 from_port: Optional[pulumi.Input[int]] = None,
                 protocols: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 to_port: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = CustomRoutingEndpointGroupDestinationArgs.__new__(CustomRoutingEndpointGroupDestinationArgs)

            if endpoint_group_id is None and not opts.urn:
                raise TypeError("Missing required property 'endpoint_group_id'")
            __props__.__dict__["endpoint_group_id"] = endpoint_group_id
            if from_port is None and not opts.urn:
                raise TypeError("Missing required property 'from_port'")
            __props__.__dict__["from_port"] = from_port
            if protocols is None and not opts.urn:
                raise TypeError("Missing required property 'protocols'")
            __props__.__dict__["protocols"] = protocols
            if to_port is None and not opts.urn:
                raise TypeError("Missing required property 'to_port'")
            __props__.__dict__["to_port"] = to_port
            __props__.__dict__["accelerator_id"] = None
            __props__.__dict__["custom_routing_endpoint_group_destination_id"] = None
            __props__.__dict__["listener_id"] = None
            __props__.__dict__["status"] = None
        super(CustomRoutingEndpointGroupDestination, __self__).__init__(
            'alicloud:ga/customRoutingEndpointGroupDestination:CustomRoutingEndpointGroupDestination',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            accelerator_id: Optional[pulumi.Input[str]] = None,
            custom_routing_endpoint_group_destination_id: Optional[pulumi.Input[str]] = None,
            endpoint_group_id: Optional[pulumi.Input[str]] = None,
            from_port: Optional[pulumi.Input[int]] = None,
            listener_id: Optional[pulumi.Input[str]] = None,
            protocols: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            status: Optional[pulumi.Input[str]] = None,
            to_port: Optional[pulumi.Input[int]] = None) -> 'CustomRoutingEndpointGroupDestination':
        """
        Get an existing CustomRoutingEndpointGroupDestination resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] accelerator_id: The ID of the GA instance.
        :param pulumi.Input[str] custom_routing_endpoint_group_destination_id: The ID of the Custom Routing Endpoint Group Destination.
        :param pulumi.Input[str] endpoint_group_id: The ID of the endpoint group.
        :param pulumi.Input[int] from_port: The start port of the backend service port range of the endpoint group. The `from_port` value must be smaller than or equal to the `to_port` value. Valid values: `1` to `65499`.
        :param pulumi.Input[str] listener_id: The ID of the listener.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] protocols: The backend service protocol of the endpoint group. Valid values: `TCP`, `UDP`, `TCP, UDP`.
        :param pulumi.Input[str] status: The status of the Custom Routing Endpoint Group Destination.
        :param pulumi.Input[int] to_port: The end port of the backend service port range of the endpoint group. The `from_port` value must be smaller than or equal to the `to_port` value. Valid values: `1` to `65499`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _CustomRoutingEndpointGroupDestinationState.__new__(_CustomRoutingEndpointGroupDestinationState)

        __props__.__dict__["accelerator_id"] = accelerator_id
        __props__.__dict__["custom_routing_endpoint_group_destination_id"] = custom_routing_endpoint_group_destination_id
        __props__.__dict__["endpoint_group_id"] = endpoint_group_id
        __props__.__dict__["from_port"] = from_port
        __props__.__dict__["listener_id"] = listener_id
        __props__.__dict__["protocols"] = protocols
        __props__.__dict__["status"] = status
        __props__.__dict__["to_port"] = to_port
        return CustomRoutingEndpointGroupDestination(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="acceleratorId")
    def accelerator_id(self) -> pulumi.Output[str]:
        """
        The ID of the GA instance.
        """
        return pulumi.get(self, "accelerator_id")

    @property
    @pulumi.getter(name="customRoutingEndpointGroupDestinationId")
    def custom_routing_endpoint_group_destination_id(self) -> pulumi.Output[str]:
        """
        The ID of the Custom Routing Endpoint Group Destination.
        """
        return pulumi.get(self, "custom_routing_endpoint_group_destination_id")

    @property
    @pulumi.getter(name="endpointGroupId")
    def endpoint_group_id(self) -> pulumi.Output[str]:
        """
        The ID of the endpoint group.
        """
        return pulumi.get(self, "endpoint_group_id")

    @property
    @pulumi.getter(name="fromPort")
    def from_port(self) -> pulumi.Output[int]:
        """
        The start port of the backend service port range of the endpoint group. The `from_port` value must be smaller than or equal to the `to_port` value. Valid values: `1` to `65499`.
        """
        return pulumi.get(self, "from_port")

    @property
    @pulumi.getter(name="listenerId")
    def listener_id(self) -> pulumi.Output[str]:
        """
        The ID of the listener.
        """
        return pulumi.get(self, "listener_id")

    @property
    @pulumi.getter
    def protocols(self) -> pulumi.Output[Sequence[str]]:
        """
        The backend service protocol of the endpoint group. Valid values: `TCP`, `UDP`, `TCP, UDP`.
        """
        return pulumi.get(self, "protocols")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The status of the Custom Routing Endpoint Group Destination.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="toPort")
    def to_port(self) -> pulumi.Output[int]:
        """
        The end port of the backend service port range of the endpoint group. The `from_port` value must be smaller than or equal to the `to_port` value. Valid values: `1` to `65499`.
        """
        return pulumi.get(self, "to_port")

