# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['TransitRouterPrefixListAssociationArgs', 'TransitRouterPrefixListAssociation']

@pulumi.input_type
class TransitRouterPrefixListAssociationArgs:
    def __init__(__self__, *,
                 next_hop: pulumi.Input[str],
                 prefix_list_id: pulumi.Input[str],
                 transit_router_id: pulumi.Input[str],
                 transit_router_table_id: pulumi.Input[str],
                 next_hop_type: Optional[pulumi.Input[str]] = None,
                 owner_uid: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a TransitRouterPrefixListAssociation resource.
        :param pulumi.Input[str] next_hop: The ID of the next hop. **NOTE:** If `next_hop` is set to `BlackHole`, you must set this parameter to `BlackHole`.
        :param pulumi.Input[str] prefix_list_id: The ID of the prefix list.
        :param pulumi.Input[str] transit_router_id: The ID of the transit router.
        :param pulumi.Input[str] transit_router_table_id: The ID of the route table of the transit router.
        :param pulumi.Input[str] next_hop_type: The type of the next hop. Valid values:
               - `BlackHole`: Specifies that all the CIDR blocks in the prefix list are blackhole routes. Packets destined for the CIDR blocks are dropped.
               - `VPC`: Specifies that the next hop of the CIDR blocks in the prefix list is a virtual private cloud (VPC) connection.
               - `VBR`: Specifies that the next hop of the CIDR blocks in the prefix list is a virtual border router (VBR) connection.
               - `TR`: Specifies that the next hop of the CIDR blocks in the prefix list is an inter-region connection.
        :param pulumi.Input[int] owner_uid: The ID of the Alibaba Cloud account to which the prefix list belongs.
        """
        pulumi.set(__self__, "next_hop", next_hop)
        pulumi.set(__self__, "prefix_list_id", prefix_list_id)
        pulumi.set(__self__, "transit_router_id", transit_router_id)
        pulumi.set(__self__, "transit_router_table_id", transit_router_table_id)
        if next_hop_type is not None:
            pulumi.set(__self__, "next_hop_type", next_hop_type)
        if owner_uid is not None:
            pulumi.set(__self__, "owner_uid", owner_uid)

    @property
    @pulumi.getter(name="nextHop")
    def next_hop(self) -> pulumi.Input[str]:
        """
        The ID of the next hop. **NOTE:** If `next_hop` is set to `BlackHole`, you must set this parameter to `BlackHole`.
        """
        return pulumi.get(self, "next_hop")

    @next_hop.setter
    def next_hop(self, value: pulumi.Input[str]):
        pulumi.set(self, "next_hop", value)

    @property
    @pulumi.getter(name="prefixListId")
    def prefix_list_id(self) -> pulumi.Input[str]:
        """
        The ID of the prefix list.
        """
        return pulumi.get(self, "prefix_list_id")

    @prefix_list_id.setter
    def prefix_list_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "prefix_list_id", value)

    @property
    @pulumi.getter(name="transitRouterId")
    def transit_router_id(self) -> pulumi.Input[str]:
        """
        The ID of the transit router.
        """
        return pulumi.get(self, "transit_router_id")

    @transit_router_id.setter
    def transit_router_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "transit_router_id", value)

    @property
    @pulumi.getter(name="transitRouterTableId")
    def transit_router_table_id(self) -> pulumi.Input[str]:
        """
        The ID of the route table of the transit router.
        """
        return pulumi.get(self, "transit_router_table_id")

    @transit_router_table_id.setter
    def transit_router_table_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "transit_router_table_id", value)

    @property
    @pulumi.getter(name="nextHopType")
    def next_hop_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of the next hop. Valid values:
        - `BlackHole`: Specifies that all the CIDR blocks in the prefix list are blackhole routes. Packets destined for the CIDR blocks are dropped.
        - `VPC`: Specifies that the next hop of the CIDR blocks in the prefix list is a virtual private cloud (VPC) connection.
        - `VBR`: Specifies that the next hop of the CIDR blocks in the prefix list is a virtual border router (VBR) connection.
        - `TR`: Specifies that the next hop of the CIDR blocks in the prefix list is an inter-region connection.
        """
        return pulumi.get(self, "next_hop_type")

    @next_hop_type.setter
    def next_hop_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "next_hop_type", value)

    @property
    @pulumi.getter(name="ownerUid")
    def owner_uid(self) -> Optional[pulumi.Input[int]]:
        """
        The ID of the Alibaba Cloud account to which the prefix list belongs.
        """
        return pulumi.get(self, "owner_uid")

    @owner_uid.setter
    def owner_uid(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "owner_uid", value)


@pulumi.input_type
class _TransitRouterPrefixListAssociationState:
    def __init__(__self__, *,
                 next_hop: Optional[pulumi.Input[str]] = None,
                 next_hop_type: Optional[pulumi.Input[str]] = None,
                 owner_uid: Optional[pulumi.Input[int]] = None,
                 prefix_list_id: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 transit_router_id: Optional[pulumi.Input[str]] = None,
                 transit_router_table_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering TransitRouterPrefixListAssociation resources.
        :param pulumi.Input[str] next_hop: The ID of the next hop. **NOTE:** If `next_hop` is set to `BlackHole`, you must set this parameter to `BlackHole`.
        :param pulumi.Input[str] next_hop_type: The type of the next hop. Valid values:
               - `BlackHole`: Specifies that all the CIDR blocks in the prefix list are blackhole routes. Packets destined for the CIDR blocks are dropped.
               - `VPC`: Specifies that the next hop of the CIDR blocks in the prefix list is a virtual private cloud (VPC) connection.
               - `VBR`: Specifies that the next hop of the CIDR blocks in the prefix list is a virtual border router (VBR) connection.
               - `TR`: Specifies that the next hop of the CIDR blocks in the prefix list is an inter-region connection.
        :param pulumi.Input[int] owner_uid: The ID of the Alibaba Cloud account to which the prefix list belongs.
        :param pulumi.Input[str] prefix_list_id: The ID of the prefix list.
        :param pulumi.Input[str] status: The status of the prefix list.
        :param pulumi.Input[str] transit_router_id: The ID of the transit router.
        :param pulumi.Input[str] transit_router_table_id: The ID of the route table of the transit router.
        """
        if next_hop is not None:
            pulumi.set(__self__, "next_hop", next_hop)
        if next_hop_type is not None:
            pulumi.set(__self__, "next_hop_type", next_hop_type)
        if owner_uid is not None:
            pulumi.set(__self__, "owner_uid", owner_uid)
        if prefix_list_id is not None:
            pulumi.set(__self__, "prefix_list_id", prefix_list_id)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if transit_router_id is not None:
            pulumi.set(__self__, "transit_router_id", transit_router_id)
        if transit_router_table_id is not None:
            pulumi.set(__self__, "transit_router_table_id", transit_router_table_id)

    @property
    @pulumi.getter(name="nextHop")
    def next_hop(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the next hop. **NOTE:** If `next_hop` is set to `BlackHole`, you must set this parameter to `BlackHole`.
        """
        return pulumi.get(self, "next_hop")

    @next_hop.setter
    def next_hop(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "next_hop", value)

    @property
    @pulumi.getter(name="nextHopType")
    def next_hop_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of the next hop. Valid values:
        - `BlackHole`: Specifies that all the CIDR blocks in the prefix list are blackhole routes. Packets destined for the CIDR blocks are dropped.
        - `VPC`: Specifies that the next hop of the CIDR blocks in the prefix list is a virtual private cloud (VPC) connection.
        - `VBR`: Specifies that the next hop of the CIDR blocks in the prefix list is a virtual border router (VBR) connection.
        - `TR`: Specifies that the next hop of the CIDR blocks in the prefix list is an inter-region connection.
        """
        return pulumi.get(self, "next_hop_type")

    @next_hop_type.setter
    def next_hop_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "next_hop_type", value)

    @property
    @pulumi.getter(name="ownerUid")
    def owner_uid(self) -> Optional[pulumi.Input[int]]:
        """
        The ID of the Alibaba Cloud account to which the prefix list belongs.
        """
        return pulumi.get(self, "owner_uid")

    @owner_uid.setter
    def owner_uid(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "owner_uid", value)

    @property
    @pulumi.getter(name="prefixListId")
    def prefix_list_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the prefix list.
        """
        return pulumi.get(self, "prefix_list_id")

    @prefix_list_id.setter
    def prefix_list_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "prefix_list_id", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the prefix list.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter(name="transitRouterId")
    def transit_router_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the transit router.
        """
        return pulumi.get(self, "transit_router_id")

    @transit_router_id.setter
    def transit_router_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "transit_router_id", value)

    @property
    @pulumi.getter(name="transitRouterTableId")
    def transit_router_table_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the route table of the transit router.
        """
        return pulumi.get(self, "transit_router_table_id")

    @transit_router_table_id.setter
    def transit_router_table_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "transit_router_table_id", value)


class TransitRouterPrefixListAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 next_hop: Optional[pulumi.Input[str]] = None,
                 next_hop_type: Optional[pulumi.Input[str]] = None,
                 owner_uid: Optional[pulumi.Input[int]] = None,
                 prefix_list_id: Optional[pulumi.Input[str]] = None,
                 transit_router_id: Optional[pulumi.Input[str]] = None,
                 transit_router_table_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Cloud Enterprise Network (CEN) Transit Router Prefix List Association resource.

        For information about Cloud Enterprise Network (CEN) Transit Router Prefix List Association and how to use it, see [What is Transit Router Prefix List Association](https://www.alibabacloud.com/help/en/cloud-enterprise-network/latest/createtransitrouterprefixlistassociation).

        > **NOTE:** Available since v1.188.0.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default = alicloud.get_account()
        example = alicloud.vpc.PrefixList("example", entrys=[{
            "cidr": "192.168.0.0/16",
        }])
        example_instance = alicloud.cen.Instance("example",
            cen_instance_name="tf_example",
            description="an example for cen")
        example_transit_router = alicloud.cen.TransitRouter("example",
            transit_router_name="tf_example",
            cen_id=example_instance.id)
        example_transit_router_route_table = alicloud.cen.TransitRouterRouteTable("example", transit_router_id=example_transit_router.transit_router_id)
        example_transit_router_prefix_list_association = alicloud.cen.TransitRouterPrefixListAssociation("example",
            prefix_list_id=example.id,
            transit_router_id=example_transit_router.transit_router_id,
            transit_router_table_id=example_transit_router_route_table.transit_router_route_table_id,
            next_hop="BlackHole",
            next_hop_type="BlackHole",
            owner_uid=default.id)
        ```

        ## Import

        Cloud Enterprise Network (CEN) Transit Router Prefix List Association can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:cen/transitRouterPrefixListAssociation:TransitRouterPrefixListAssociation default <prefix_list_id>:<transit_router_id>:<transit_router_table_id>:<next_hop>.
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] next_hop: The ID of the next hop. **NOTE:** If `next_hop` is set to `BlackHole`, you must set this parameter to `BlackHole`.
        :param pulumi.Input[str] next_hop_type: The type of the next hop. Valid values:
               - `BlackHole`: Specifies that all the CIDR blocks in the prefix list are blackhole routes. Packets destined for the CIDR blocks are dropped.
               - `VPC`: Specifies that the next hop of the CIDR blocks in the prefix list is a virtual private cloud (VPC) connection.
               - `VBR`: Specifies that the next hop of the CIDR blocks in the prefix list is a virtual border router (VBR) connection.
               - `TR`: Specifies that the next hop of the CIDR blocks in the prefix list is an inter-region connection.
        :param pulumi.Input[int] owner_uid: The ID of the Alibaba Cloud account to which the prefix list belongs.
        :param pulumi.Input[str] prefix_list_id: The ID of the prefix list.
        :param pulumi.Input[str] transit_router_id: The ID of the transit router.
        :param pulumi.Input[str] transit_router_table_id: The ID of the route table of the transit router.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TransitRouterPrefixListAssociationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Cloud Enterprise Network (CEN) Transit Router Prefix List Association resource.

        For information about Cloud Enterprise Network (CEN) Transit Router Prefix List Association and how to use it, see [What is Transit Router Prefix List Association](https://www.alibabacloud.com/help/en/cloud-enterprise-network/latest/createtransitrouterprefixlistassociation).

        > **NOTE:** Available since v1.188.0.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default = alicloud.get_account()
        example = alicloud.vpc.PrefixList("example", entrys=[{
            "cidr": "192.168.0.0/16",
        }])
        example_instance = alicloud.cen.Instance("example",
            cen_instance_name="tf_example",
            description="an example for cen")
        example_transit_router = alicloud.cen.TransitRouter("example",
            transit_router_name="tf_example",
            cen_id=example_instance.id)
        example_transit_router_route_table = alicloud.cen.TransitRouterRouteTable("example", transit_router_id=example_transit_router.transit_router_id)
        example_transit_router_prefix_list_association = alicloud.cen.TransitRouterPrefixListAssociation("example",
            prefix_list_id=example.id,
            transit_router_id=example_transit_router.transit_router_id,
            transit_router_table_id=example_transit_router_route_table.transit_router_route_table_id,
            next_hop="BlackHole",
            next_hop_type="BlackHole",
            owner_uid=default.id)
        ```

        ## Import

        Cloud Enterprise Network (CEN) Transit Router Prefix List Association can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:cen/transitRouterPrefixListAssociation:TransitRouterPrefixListAssociation default <prefix_list_id>:<transit_router_id>:<transit_router_table_id>:<next_hop>.
        ```

        :param str resource_name: The name of the resource.
        :param TransitRouterPrefixListAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TransitRouterPrefixListAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 next_hop: Optional[pulumi.Input[str]] = None,
                 next_hop_type: Optional[pulumi.Input[str]] = None,
                 owner_uid: Optional[pulumi.Input[int]] = None,
                 prefix_list_id: Optional[pulumi.Input[str]] = None,
                 transit_router_id: Optional[pulumi.Input[str]] = None,
                 transit_router_table_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TransitRouterPrefixListAssociationArgs.__new__(TransitRouterPrefixListAssociationArgs)

            if next_hop is None and not opts.urn:
                raise TypeError("Missing required property 'next_hop'")
            __props__.__dict__["next_hop"] = next_hop
            __props__.__dict__["next_hop_type"] = next_hop_type
            __props__.__dict__["owner_uid"] = owner_uid
            if prefix_list_id is None and not opts.urn:
                raise TypeError("Missing required property 'prefix_list_id'")
            __props__.__dict__["prefix_list_id"] = prefix_list_id
            if transit_router_id is None and not opts.urn:
                raise TypeError("Missing required property 'transit_router_id'")
            __props__.__dict__["transit_router_id"] = transit_router_id
            if transit_router_table_id is None and not opts.urn:
                raise TypeError("Missing required property 'transit_router_table_id'")
            __props__.__dict__["transit_router_table_id"] = transit_router_table_id
            __props__.__dict__["status"] = None
        super(TransitRouterPrefixListAssociation, __self__).__init__(
            'alicloud:cen/transitRouterPrefixListAssociation:TransitRouterPrefixListAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            next_hop: Optional[pulumi.Input[str]] = None,
            next_hop_type: Optional[pulumi.Input[str]] = None,
            owner_uid: Optional[pulumi.Input[int]] = None,
            prefix_list_id: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            transit_router_id: Optional[pulumi.Input[str]] = None,
            transit_router_table_id: Optional[pulumi.Input[str]] = None) -> 'TransitRouterPrefixListAssociation':
        """
        Get an existing TransitRouterPrefixListAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] next_hop: The ID of the next hop. **NOTE:** If `next_hop` is set to `BlackHole`, you must set this parameter to `BlackHole`.
        :param pulumi.Input[str] next_hop_type: The type of the next hop. Valid values:
               - `BlackHole`: Specifies that all the CIDR blocks in the prefix list are blackhole routes. Packets destined for the CIDR blocks are dropped.
               - `VPC`: Specifies that the next hop of the CIDR blocks in the prefix list is a virtual private cloud (VPC) connection.
               - `VBR`: Specifies that the next hop of the CIDR blocks in the prefix list is a virtual border router (VBR) connection.
               - `TR`: Specifies that the next hop of the CIDR blocks in the prefix list is an inter-region connection.
        :param pulumi.Input[int] owner_uid: The ID of the Alibaba Cloud account to which the prefix list belongs.
        :param pulumi.Input[str] prefix_list_id: The ID of the prefix list.
        :param pulumi.Input[str] status: The status of the prefix list.
        :param pulumi.Input[str] transit_router_id: The ID of the transit router.
        :param pulumi.Input[str] transit_router_table_id: The ID of the route table of the transit router.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _TransitRouterPrefixListAssociationState.__new__(_TransitRouterPrefixListAssociationState)

        __props__.__dict__["next_hop"] = next_hop
        __props__.__dict__["next_hop_type"] = next_hop_type
        __props__.__dict__["owner_uid"] = owner_uid
        __props__.__dict__["prefix_list_id"] = prefix_list_id
        __props__.__dict__["status"] = status
        __props__.__dict__["transit_router_id"] = transit_router_id
        __props__.__dict__["transit_router_table_id"] = transit_router_table_id
        return TransitRouterPrefixListAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="nextHop")
    def next_hop(self) -> pulumi.Output[str]:
        """
        The ID of the next hop. **NOTE:** If `next_hop` is set to `BlackHole`, you must set this parameter to `BlackHole`.
        """
        return pulumi.get(self, "next_hop")

    @property
    @pulumi.getter(name="nextHopType")
    def next_hop_type(self) -> pulumi.Output[str]:
        """
        The type of the next hop. Valid values:
        - `BlackHole`: Specifies that all the CIDR blocks in the prefix list are blackhole routes. Packets destined for the CIDR blocks are dropped.
        - `VPC`: Specifies that the next hop of the CIDR blocks in the prefix list is a virtual private cloud (VPC) connection.
        - `VBR`: Specifies that the next hop of the CIDR blocks in the prefix list is a virtual border router (VBR) connection.
        - `TR`: Specifies that the next hop of the CIDR blocks in the prefix list is an inter-region connection.
        """
        return pulumi.get(self, "next_hop_type")

    @property
    @pulumi.getter(name="ownerUid")
    def owner_uid(self) -> pulumi.Output[int]:
        """
        The ID of the Alibaba Cloud account to which the prefix list belongs.
        """
        return pulumi.get(self, "owner_uid")

    @property
    @pulumi.getter(name="prefixListId")
    def prefix_list_id(self) -> pulumi.Output[str]:
        """
        The ID of the prefix list.
        """
        return pulumi.get(self, "prefix_list_id")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The status of the prefix list.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="transitRouterId")
    def transit_router_id(self) -> pulumi.Output[str]:
        """
        The ID of the transit router.
        """
        return pulumi.get(self, "transit_router_id")

    @property
    @pulumi.getter(name="transitRouterTableId")
    def transit_router_table_id(self) -> pulumi.Output[str]:
        """
        The ID of the route table of the transit router.
        """
        return pulumi.get(self, "transit_router_table_id")

