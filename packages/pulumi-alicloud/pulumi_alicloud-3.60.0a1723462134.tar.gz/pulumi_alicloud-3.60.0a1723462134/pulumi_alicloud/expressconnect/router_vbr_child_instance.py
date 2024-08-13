# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['RouterVbrChildInstanceArgs', 'RouterVbrChildInstance']

@pulumi.input_type
class RouterVbrChildInstanceArgs:
    def __init__(__self__, *,
                 child_instance_id: pulumi.Input[str],
                 child_instance_region_id: pulumi.Input[str],
                 child_instance_type: pulumi.Input[str],
                 ecr_id: pulumi.Input[str],
                 child_instance_owner_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a RouterVbrChildInstance resource.
        :param pulumi.Input[str] child_instance_id: The ID of the leased line gateway subinstance.
        :param pulumi.Input[str] child_instance_region_id: Region of the leased line gateway sub-instance.
        :param pulumi.Input[str] child_instance_type: The type of leased line gateway sub-instance, Valid values: `VBR`.
        :param pulumi.Input[str] ecr_id: ID of the representative leased line gateway instance.
        :param pulumi.Input[str] child_instance_owner_id: The ID of the subinstance of the leased line gateway.
        """
        pulumi.set(__self__, "child_instance_id", child_instance_id)
        pulumi.set(__self__, "child_instance_region_id", child_instance_region_id)
        pulumi.set(__self__, "child_instance_type", child_instance_type)
        pulumi.set(__self__, "ecr_id", ecr_id)
        if child_instance_owner_id is not None:
            pulumi.set(__self__, "child_instance_owner_id", child_instance_owner_id)

    @property
    @pulumi.getter(name="childInstanceId")
    def child_instance_id(self) -> pulumi.Input[str]:
        """
        The ID of the leased line gateway subinstance.
        """
        return pulumi.get(self, "child_instance_id")

    @child_instance_id.setter
    def child_instance_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "child_instance_id", value)

    @property
    @pulumi.getter(name="childInstanceRegionId")
    def child_instance_region_id(self) -> pulumi.Input[str]:
        """
        Region of the leased line gateway sub-instance.
        """
        return pulumi.get(self, "child_instance_region_id")

    @child_instance_region_id.setter
    def child_instance_region_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "child_instance_region_id", value)

    @property
    @pulumi.getter(name="childInstanceType")
    def child_instance_type(self) -> pulumi.Input[str]:
        """
        The type of leased line gateway sub-instance, Valid values: `VBR`.
        """
        return pulumi.get(self, "child_instance_type")

    @child_instance_type.setter
    def child_instance_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "child_instance_type", value)

    @property
    @pulumi.getter(name="ecrId")
    def ecr_id(self) -> pulumi.Input[str]:
        """
        ID of the representative leased line gateway instance.
        """
        return pulumi.get(self, "ecr_id")

    @ecr_id.setter
    def ecr_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "ecr_id", value)

    @property
    @pulumi.getter(name="childInstanceOwnerId")
    def child_instance_owner_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the subinstance of the leased line gateway.
        """
        return pulumi.get(self, "child_instance_owner_id")

    @child_instance_owner_id.setter
    def child_instance_owner_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "child_instance_owner_id", value)


@pulumi.input_type
class _RouterVbrChildInstanceState:
    def __init__(__self__, *,
                 child_instance_id: Optional[pulumi.Input[str]] = None,
                 child_instance_owner_id: Optional[pulumi.Input[str]] = None,
                 child_instance_region_id: Optional[pulumi.Input[str]] = None,
                 child_instance_type: Optional[pulumi.Input[str]] = None,
                 create_time: Optional[pulumi.Input[str]] = None,
                 ecr_id: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering RouterVbrChildInstance resources.
        :param pulumi.Input[str] child_instance_id: The ID of the leased line gateway subinstance.
        :param pulumi.Input[str] child_instance_owner_id: The ID of the subinstance of the leased line gateway.
        :param pulumi.Input[str] child_instance_region_id: Region of the leased line gateway sub-instance.
        :param pulumi.Input[str] child_instance_type: The type of leased line gateway sub-instance, Valid values: `VBR`.
        :param pulumi.Input[str] create_time: The creation time of the resource.
        :param pulumi.Input[str] ecr_id: ID of the representative leased line gateway instance.
        :param pulumi.Input[str] status: Binding relationship status of leased line gateway subinstances.
        """
        if child_instance_id is not None:
            pulumi.set(__self__, "child_instance_id", child_instance_id)
        if child_instance_owner_id is not None:
            pulumi.set(__self__, "child_instance_owner_id", child_instance_owner_id)
        if child_instance_region_id is not None:
            pulumi.set(__self__, "child_instance_region_id", child_instance_region_id)
        if child_instance_type is not None:
            pulumi.set(__self__, "child_instance_type", child_instance_type)
        if create_time is not None:
            pulumi.set(__self__, "create_time", create_time)
        if ecr_id is not None:
            pulumi.set(__self__, "ecr_id", ecr_id)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="childInstanceId")
    def child_instance_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the leased line gateway subinstance.
        """
        return pulumi.get(self, "child_instance_id")

    @child_instance_id.setter
    def child_instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "child_instance_id", value)

    @property
    @pulumi.getter(name="childInstanceOwnerId")
    def child_instance_owner_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the subinstance of the leased line gateway.
        """
        return pulumi.get(self, "child_instance_owner_id")

    @child_instance_owner_id.setter
    def child_instance_owner_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "child_instance_owner_id", value)

    @property
    @pulumi.getter(name="childInstanceRegionId")
    def child_instance_region_id(self) -> Optional[pulumi.Input[str]]:
        """
        Region of the leased line gateway sub-instance.
        """
        return pulumi.get(self, "child_instance_region_id")

    @child_instance_region_id.setter
    def child_instance_region_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "child_instance_region_id", value)

    @property
    @pulumi.getter(name="childInstanceType")
    def child_instance_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of leased line gateway sub-instance, Valid values: `VBR`.
        """
        return pulumi.get(self, "child_instance_type")

    @child_instance_type.setter
    def child_instance_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "child_instance_type", value)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> Optional[pulumi.Input[str]]:
        """
        The creation time of the resource.
        """
        return pulumi.get(self, "create_time")

    @create_time.setter
    def create_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create_time", value)

    @property
    @pulumi.getter(name="ecrId")
    def ecr_id(self) -> Optional[pulumi.Input[str]]:
        """
        ID of the representative leased line gateway instance.
        """
        return pulumi.get(self, "ecr_id")

    @ecr_id.setter
    def ecr_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ecr_id", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Binding relationship status of leased line gateway subinstances.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


class RouterVbrChildInstance(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 child_instance_id: Optional[pulumi.Input[str]] = None,
                 child_instance_owner_id: Optional[pulumi.Input[str]] = None,
                 child_instance_region_id: Optional[pulumi.Input[str]] = None,
                 child_instance_type: Optional[pulumi.Input[str]] = None,
                 ecr_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Express Connect Router Express Connect Router Vbr Child Instance resource. Leased Line Gateway VBR sub-instance.

        For information about Express Connect Router Express Connect Router Vbr Child Instance and how to use it, see [What is Express Connect Router Vbr Child Instance](https://next.api.alibabacloud.com/api/ExpressConnectRouter/2023-09-01/AttachExpressConnectRouterChildInstance).

        > **NOTE:** Available since v1.224.0.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "terraform-example"
        name_regex = alicloud.expressconnect.get_physical_connections(name_regex="^preserved-NODELETING")
        defaultydbbk3 = alicloud.expressconnect.VirtualBorderRouter("defaultydbbk3",
            physical_connection_id=name_regex.connections[0].id,
            vlan_id=1000,
            peer_gateway_ip="192.168.254.2",
            peering_subnet_mask="255.255.255.0",
            local_gateway_ip="192.168.254.1")
        default_a_alh_uy = alicloud.expressconnect.RouterExpressConnectRouter("defaultAAlhUy", alibaba_side_asn=65532)
        current = alicloud.get_account()
        default = alicloud.expressconnect.RouterVbrChildInstance("default",
            child_instance_id=defaultydbbk3.id,
            child_instance_region_id="cn-hangzhou",
            ecr_id=default_a_alh_uy.id,
            child_instance_type="VBR",
            child_instance_owner_id=current.id)
        ```

        ## Import

        Express Connect Router Express Connect Router Vbr Child Instance can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:expressconnect/routerVbrChildInstance:RouterVbrChildInstance example <ecr_id>:<child_instance_id>:<child_instance_type>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] child_instance_id: The ID of the leased line gateway subinstance.
        :param pulumi.Input[str] child_instance_owner_id: The ID of the subinstance of the leased line gateway.
        :param pulumi.Input[str] child_instance_region_id: Region of the leased line gateway sub-instance.
        :param pulumi.Input[str] child_instance_type: The type of leased line gateway sub-instance, Valid values: `VBR`.
        :param pulumi.Input[str] ecr_id: ID of the representative leased line gateway instance.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RouterVbrChildInstanceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Express Connect Router Express Connect Router Vbr Child Instance resource. Leased Line Gateway VBR sub-instance.

        For information about Express Connect Router Express Connect Router Vbr Child Instance and how to use it, see [What is Express Connect Router Vbr Child Instance](https://next.api.alibabacloud.com/api/ExpressConnectRouter/2023-09-01/AttachExpressConnectRouterChildInstance).

        > **NOTE:** Available since v1.224.0.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "terraform-example"
        name_regex = alicloud.expressconnect.get_physical_connections(name_regex="^preserved-NODELETING")
        defaultydbbk3 = alicloud.expressconnect.VirtualBorderRouter("defaultydbbk3",
            physical_connection_id=name_regex.connections[0].id,
            vlan_id=1000,
            peer_gateway_ip="192.168.254.2",
            peering_subnet_mask="255.255.255.0",
            local_gateway_ip="192.168.254.1")
        default_a_alh_uy = alicloud.expressconnect.RouterExpressConnectRouter("defaultAAlhUy", alibaba_side_asn=65532)
        current = alicloud.get_account()
        default = alicloud.expressconnect.RouterVbrChildInstance("default",
            child_instance_id=defaultydbbk3.id,
            child_instance_region_id="cn-hangzhou",
            ecr_id=default_a_alh_uy.id,
            child_instance_type="VBR",
            child_instance_owner_id=current.id)
        ```

        ## Import

        Express Connect Router Express Connect Router Vbr Child Instance can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:expressconnect/routerVbrChildInstance:RouterVbrChildInstance example <ecr_id>:<child_instance_id>:<child_instance_type>
        ```

        :param str resource_name: The name of the resource.
        :param RouterVbrChildInstanceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RouterVbrChildInstanceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 child_instance_id: Optional[pulumi.Input[str]] = None,
                 child_instance_owner_id: Optional[pulumi.Input[str]] = None,
                 child_instance_region_id: Optional[pulumi.Input[str]] = None,
                 child_instance_type: Optional[pulumi.Input[str]] = None,
                 ecr_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RouterVbrChildInstanceArgs.__new__(RouterVbrChildInstanceArgs)

            if child_instance_id is None and not opts.urn:
                raise TypeError("Missing required property 'child_instance_id'")
            __props__.__dict__["child_instance_id"] = child_instance_id
            __props__.__dict__["child_instance_owner_id"] = child_instance_owner_id
            if child_instance_region_id is None and not opts.urn:
                raise TypeError("Missing required property 'child_instance_region_id'")
            __props__.__dict__["child_instance_region_id"] = child_instance_region_id
            if child_instance_type is None and not opts.urn:
                raise TypeError("Missing required property 'child_instance_type'")
            __props__.__dict__["child_instance_type"] = child_instance_type
            if ecr_id is None and not opts.urn:
                raise TypeError("Missing required property 'ecr_id'")
            __props__.__dict__["ecr_id"] = ecr_id
            __props__.__dict__["create_time"] = None
            __props__.__dict__["status"] = None
        super(RouterVbrChildInstance, __self__).__init__(
            'alicloud:expressconnect/routerVbrChildInstance:RouterVbrChildInstance',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            child_instance_id: Optional[pulumi.Input[str]] = None,
            child_instance_owner_id: Optional[pulumi.Input[str]] = None,
            child_instance_region_id: Optional[pulumi.Input[str]] = None,
            child_instance_type: Optional[pulumi.Input[str]] = None,
            create_time: Optional[pulumi.Input[str]] = None,
            ecr_id: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None) -> 'RouterVbrChildInstance':
        """
        Get an existing RouterVbrChildInstance resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] child_instance_id: The ID of the leased line gateway subinstance.
        :param pulumi.Input[str] child_instance_owner_id: The ID of the subinstance of the leased line gateway.
        :param pulumi.Input[str] child_instance_region_id: Region of the leased line gateway sub-instance.
        :param pulumi.Input[str] child_instance_type: The type of leased line gateway sub-instance, Valid values: `VBR`.
        :param pulumi.Input[str] create_time: The creation time of the resource.
        :param pulumi.Input[str] ecr_id: ID of the representative leased line gateway instance.
        :param pulumi.Input[str] status: Binding relationship status of leased line gateway subinstances.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _RouterVbrChildInstanceState.__new__(_RouterVbrChildInstanceState)

        __props__.__dict__["child_instance_id"] = child_instance_id
        __props__.__dict__["child_instance_owner_id"] = child_instance_owner_id
        __props__.__dict__["child_instance_region_id"] = child_instance_region_id
        __props__.__dict__["child_instance_type"] = child_instance_type
        __props__.__dict__["create_time"] = create_time
        __props__.__dict__["ecr_id"] = ecr_id
        __props__.__dict__["status"] = status
        return RouterVbrChildInstance(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="childInstanceId")
    def child_instance_id(self) -> pulumi.Output[str]:
        """
        The ID of the leased line gateway subinstance.
        """
        return pulumi.get(self, "child_instance_id")

    @property
    @pulumi.getter(name="childInstanceOwnerId")
    def child_instance_owner_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the subinstance of the leased line gateway.
        """
        return pulumi.get(self, "child_instance_owner_id")

    @property
    @pulumi.getter(name="childInstanceRegionId")
    def child_instance_region_id(self) -> pulumi.Output[str]:
        """
        Region of the leased line gateway sub-instance.
        """
        return pulumi.get(self, "child_instance_region_id")

    @property
    @pulumi.getter(name="childInstanceType")
    def child_instance_type(self) -> pulumi.Output[str]:
        """
        The type of leased line gateway sub-instance, Valid values: `VBR`.
        """
        return pulumi.get(self, "child_instance_type")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        The creation time of the resource.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="ecrId")
    def ecr_id(self) -> pulumi.Output[str]:
        """
        ID of the representative leased line gateway instance.
        """
        return pulumi.get(self, "ecr_id")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        Binding relationship status of leased line gateway subinstances.
        """
        return pulumi.get(self, "status")

