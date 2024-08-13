# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['CustomRoutingEndpointGroupArgs', 'CustomRoutingEndpointGroup']

@pulumi.input_type
class CustomRoutingEndpointGroupArgs:
    def __init__(__self__, *,
                 accelerator_id: pulumi.Input[str],
                 endpoint_group_region: pulumi.Input[str],
                 listener_id: pulumi.Input[str],
                 custom_routing_endpoint_group_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a CustomRoutingEndpointGroup resource.
        :param pulumi.Input[str] accelerator_id: The ID of the GA instance.
        :param pulumi.Input[str] endpoint_group_region: The ID of the region in which to create the endpoint group.
        :param pulumi.Input[str] listener_id: The ID of the custom routing listener.
        :param pulumi.Input[str] custom_routing_endpoint_group_name: The name of the endpoint group.
        :param pulumi.Input[str] description: The description of the endpoint group.
        """
        pulumi.set(__self__, "accelerator_id", accelerator_id)
        pulumi.set(__self__, "endpoint_group_region", endpoint_group_region)
        pulumi.set(__self__, "listener_id", listener_id)
        if custom_routing_endpoint_group_name is not None:
            pulumi.set(__self__, "custom_routing_endpoint_group_name", custom_routing_endpoint_group_name)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter(name="acceleratorId")
    def accelerator_id(self) -> pulumi.Input[str]:
        """
        The ID of the GA instance.
        """
        return pulumi.get(self, "accelerator_id")

    @accelerator_id.setter
    def accelerator_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "accelerator_id", value)

    @property
    @pulumi.getter(name="endpointGroupRegion")
    def endpoint_group_region(self) -> pulumi.Input[str]:
        """
        The ID of the region in which to create the endpoint group.
        """
        return pulumi.get(self, "endpoint_group_region")

    @endpoint_group_region.setter
    def endpoint_group_region(self, value: pulumi.Input[str]):
        pulumi.set(self, "endpoint_group_region", value)

    @property
    @pulumi.getter(name="listenerId")
    def listener_id(self) -> pulumi.Input[str]:
        """
        The ID of the custom routing listener.
        """
        return pulumi.get(self, "listener_id")

    @listener_id.setter
    def listener_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "listener_id", value)

    @property
    @pulumi.getter(name="customRoutingEndpointGroupName")
    def custom_routing_endpoint_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the endpoint group.
        """
        return pulumi.get(self, "custom_routing_endpoint_group_name")

    @custom_routing_endpoint_group_name.setter
    def custom_routing_endpoint_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "custom_routing_endpoint_group_name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the endpoint group.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


@pulumi.input_type
class _CustomRoutingEndpointGroupState:
    def __init__(__self__, *,
                 accelerator_id: Optional[pulumi.Input[str]] = None,
                 custom_routing_endpoint_group_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 endpoint_group_region: Optional[pulumi.Input[str]] = None,
                 listener_id: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering CustomRoutingEndpointGroup resources.
        :param pulumi.Input[str] accelerator_id: The ID of the GA instance.
        :param pulumi.Input[str] custom_routing_endpoint_group_name: The name of the endpoint group.
        :param pulumi.Input[str] description: The description of the endpoint group.
        :param pulumi.Input[str] endpoint_group_region: The ID of the region in which to create the endpoint group.
        :param pulumi.Input[str] listener_id: The ID of the custom routing listener.
        :param pulumi.Input[str] status: The status of the Custom Routing Endpoint Group.
        """
        if accelerator_id is not None:
            pulumi.set(__self__, "accelerator_id", accelerator_id)
        if custom_routing_endpoint_group_name is not None:
            pulumi.set(__self__, "custom_routing_endpoint_group_name", custom_routing_endpoint_group_name)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if endpoint_group_region is not None:
            pulumi.set(__self__, "endpoint_group_region", endpoint_group_region)
        if listener_id is not None:
            pulumi.set(__self__, "listener_id", listener_id)
        if status is not None:
            pulumi.set(__self__, "status", status)

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
    @pulumi.getter(name="customRoutingEndpointGroupName")
    def custom_routing_endpoint_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the endpoint group.
        """
        return pulumi.get(self, "custom_routing_endpoint_group_name")

    @custom_routing_endpoint_group_name.setter
    def custom_routing_endpoint_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "custom_routing_endpoint_group_name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the endpoint group.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="endpointGroupRegion")
    def endpoint_group_region(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the region in which to create the endpoint group.
        """
        return pulumi.get(self, "endpoint_group_region")

    @endpoint_group_region.setter
    def endpoint_group_region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "endpoint_group_region", value)

    @property
    @pulumi.getter(name="listenerId")
    def listener_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the custom routing listener.
        """
        return pulumi.get(self, "listener_id")

    @listener_id.setter
    def listener_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "listener_id", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the Custom Routing Endpoint Group.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


class CustomRoutingEndpointGroup(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 accelerator_id: Optional[pulumi.Input[str]] = None,
                 custom_routing_endpoint_group_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 endpoint_group_region: Optional[pulumi.Input[str]] = None,
                 listener_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Global Accelerator (GA) Custom Routing Endpoint Group resource.

        For information about Global Accelerator (GA) Custom Routing Endpoint Group and how to use it, see [What is Custom Routing Endpoint Group](https://www.alibabacloud.com/help/en/global-accelerator/latest/api-ga-2019-11-20-createcustomroutingendpointgroups).

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
        ```

        ## Import

        Global Accelerator (GA) Custom Routing Endpoint Group can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:ga/customRoutingEndpointGroup:CustomRoutingEndpointGroup example <id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] accelerator_id: The ID of the GA instance.
        :param pulumi.Input[str] custom_routing_endpoint_group_name: The name of the endpoint group.
        :param pulumi.Input[str] description: The description of the endpoint group.
        :param pulumi.Input[str] endpoint_group_region: The ID of the region in which to create the endpoint group.
        :param pulumi.Input[str] listener_id: The ID of the custom routing listener.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: CustomRoutingEndpointGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Global Accelerator (GA) Custom Routing Endpoint Group resource.

        For information about Global Accelerator (GA) Custom Routing Endpoint Group and how to use it, see [What is Custom Routing Endpoint Group](https://www.alibabacloud.com/help/en/global-accelerator/latest/api-ga-2019-11-20-createcustomroutingendpointgroups).

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
        ```

        ## Import

        Global Accelerator (GA) Custom Routing Endpoint Group can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:ga/customRoutingEndpointGroup:CustomRoutingEndpointGroup example <id>
        ```

        :param str resource_name: The name of the resource.
        :param CustomRoutingEndpointGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CustomRoutingEndpointGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 accelerator_id: Optional[pulumi.Input[str]] = None,
                 custom_routing_endpoint_group_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 endpoint_group_region: Optional[pulumi.Input[str]] = None,
                 listener_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = CustomRoutingEndpointGroupArgs.__new__(CustomRoutingEndpointGroupArgs)

            if accelerator_id is None and not opts.urn:
                raise TypeError("Missing required property 'accelerator_id'")
            __props__.__dict__["accelerator_id"] = accelerator_id
            __props__.__dict__["custom_routing_endpoint_group_name"] = custom_routing_endpoint_group_name
            __props__.__dict__["description"] = description
            if endpoint_group_region is None and not opts.urn:
                raise TypeError("Missing required property 'endpoint_group_region'")
            __props__.__dict__["endpoint_group_region"] = endpoint_group_region
            if listener_id is None and not opts.urn:
                raise TypeError("Missing required property 'listener_id'")
            __props__.__dict__["listener_id"] = listener_id
            __props__.__dict__["status"] = None
        super(CustomRoutingEndpointGroup, __self__).__init__(
            'alicloud:ga/customRoutingEndpointGroup:CustomRoutingEndpointGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            accelerator_id: Optional[pulumi.Input[str]] = None,
            custom_routing_endpoint_group_name: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            endpoint_group_region: Optional[pulumi.Input[str]] = None,
            listener_id: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None) -> 'CustomRoutingEndpointGroup':
        """
        Get an existing CustomRoutingEndpointGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] accelerator_id: The ID of the GA instance.
        :param pulumi.Input[str] custom_routing_endpoint_group_name: The name of the endpoint group.
        :param pulumi.Input[str] description: The description of the endpoint group.
        :param pulumi.Input[str] endpoint_group_region: The ID of the region in which to create the endpoint group.
        :param pulumi.Input[str] listener_id: The ID of the custom routing listener.
        :param pulumi.Input[str] status: The status of the Custom Routing Endpoint Group.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _CustomRoutingEndpointGroupState.__new__(_CustomRoutingEndpointGroupState)

        __props__.__dict__["accelerator_id"] = accelerator_id
        __props__.__dict__["custom_routing_endpoint_group_name"] = custom_routing_endpoint_group_name
        __props__.__dict__["description"] = description
        __props__.__dict__["endpoint_group_region"] = endpoint_group_region
        __props__.__dict__["listener_id"] = listener_id
        __props__.__dict__["status"] = status
        return CustomRoutingEndpointGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="acceleratorId")
    def accelerator_id(self) -> pulumi.Output[str]:
        """
        The ID of the GA instance.
        """
        return pulumi.get(self, "accelerator_id")

    @property
    @pulumi.getter(name="customRoutingEndpointGroupName")
    def custom_routing_endpoint_group_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the endpoint group.
        """
        return pulumi.get(self, "custom_routing_endpoint_group_name")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the endpoint group.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="endpointGroupRegion")
    def endpoint_group_region(self) -> pulumi.Output[str]:
        """
        The ID of the region in which to create the endpoint group.
        """
        return pulumi.get(self, "endpoint_group_region")

    @property
    @pulumi.getter(name="listenerId")
    def listener_id(self) -> pulumi.Output[str]:
        """
        The ID of the custom routing listener.
        """
        return pulumi.get(self, "listener_id")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The status of the Custom Routing Endpoint Group.
        """
        return pulumi.get(self, "status")

