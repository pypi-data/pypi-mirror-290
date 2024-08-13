# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['AnycastEipAddressArgs', 'AnycastEipAddress']

@pulumi.input_type
class AnycastEipAddressArgs:
    def __init__(__self__, *,
                 service_location: pulumi.Input[str],
                 anycast_eip_address_name: Optional[pulumi.Input[str]] = None,
                 bandwidth: Optional[pulumi.Input[int]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 internet_charge_type: Optional[pulumi.Input[str]] = None,
                 payment_type: Optional[pulumi.Input[str]] = None,
                 resource_group_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None):
        """
        The set of arguments for constructing a AnycastEipAddress resource.
        :param pulumi.Input[str] service_location: Anycast EIP instance access area. "international": Refers to areas outside of Mainland China.
        :param pulumi.Input[str] anycast_eip_address_name: Anycast EIP instance name.
        :param pulumi.Input[int] bandwidth: The peak bandwidth of the Anycast EIP instance, in Mbps.
        :param pulumi.Input[str] description: Anycast EIP instance description.
        :param pulumi.Input[str] internet_charge_type: The billing method of Anycast EIP instance. "PayByBandwidth": refers to the method of billing based on traffic.
        :param pulumi.Input[str] payment_type: The payment model of Anycast EIP instance. "PayAsYouGo": Refers to the post-paid mode.
        :param pulumi.Input[str] resource_group_id: The ID of the resource group to which the instance belongs.
        :param pulumi.Input[Mapping[str, Any]] tags: List of resource-bound tags.
        """
        pulumi.set(__self__, "service_location", service_location)
        if anycast_eip_address_name is not None:
            pulumi.set(__self__, "anycast_eip_address_name", anycast_eip_address_name)
        if bandwidth is not None:
            pulumi.set(__self__, "bandwidth", bandwidth)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if internet_charge_type is not None:
            pulumi.set(__self__, "internet_charge_type", internet_charge_type)
        if payment_type is not None:
            pulumi.set(__self__, "payment_type", payment_type)
        if resource_group_id is not None:
            pulumi.set(__self__, "resource_group_id", resource_group_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="serviceLocation")
    def service_location(self) -> pulumi.Input[str]:
        """
        Anycast EIP instance access area. "international": Refers to areas outside of Mainland China.
        """
        return pulumi.get(self, "service_location")

    @service_location.setter
    def service_location(self, value: pulumi.Input[str]):
        pulumi.set(self, "service_location", value)

    @property
    @pulumi.getter(name="anycastEipAddressName")
    def anycast_eip_address_name(self) -> Optional[pulumi.Input[str]]:
        """
        Anycast EIP instance name.
        """
        return pulumi.get(self, "anycast_eip_address_name")

    @anycast_eip_address_name.setter
    def anycast_eip_address_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "anycast_eip_address_name", value)

    @property
    @pulumi.getter
    def bandwidth(self) -> Optional[pulumi.Input[int]]:
        """
        The peak bandwidth of the Anycast EIP instance, in Mbps.
        """
        return pulumi.get(self, "bandwidth")

    @bandwidth.setter
    def bandwidth(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "bandwidth", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Anycast EIP instance description.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="internetChargeType")
    def internet_charge_type(self) -> Optional[pulumi.Input[str]]:
        """
        The billing method of Anycast EIP instance. "PayByBandwidth": refers to the method of billing based on traffic.
        """
        return pulumi.get(self, "internet_charge_type")

    @internet_charge_type.setter
    def internet_charge_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "internet_charge_type", value)

    @property
    @pulumi.getter(name="paymentType")
    def payment_type(self) -> Optional[pulumi.Input[str]]:
        """
        The payment model of Anycast EIP instance. "PayAsYouGo": Refers to the post-paid mode.
        """
        return pulumi.get(self, "payment_type")

    @payment_type.setter
    def payment_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "payment_type", value)

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the resource group to which the instance belongs.
        """
        return pulumi.get(self, "resource_group_id")

    @resource_group_id.setter
    def resource_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        List of resource-bound tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _AnycastEipAddressState:
    def __init__(__self__, *,
                 anycast_eip_address_name: Optional[pulumi.Input[str]] = None,
                 bandwidth: Optional[pulumi.Input[int]] = None,
                 create_time: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 internet_charge_type: Optional[pulumi.Input[str]] = None,
                 payment_type: Optional[pulumi.Input[str]] = None,
                 resource_group_id: Optional[pulumi.Input[str]] = None,
                 service_location: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None):
        """
        Input properties used for looking up and filtering AnycastEipAddress resources.
        :param pulumi.Input[str] anycast_eip_address_name: Anycast EIP instance name.
        :param pulumi.Input[int] bandwidth: The peak bandwidth of the Anycast EIP instance, in Mbps.
        :param pulumi.Input[str] create_time: Anycast EIP instance creation time.
        :param pulumi.Input[str] description: Anycast EIP instance description.
        :param pulumi.Input[str] internet_charge_type: The billing method of Anycast EIP instance. "PayByBandwidth": refers to the method of billing based on traffic.
        :param pulumi.Input[str] payment_type: The payment model of Anycast EIP instance. "PayAsYouGo": Refers to the post-paid mode.
        :param pulumi.Input[str] resource_group_id: The ID of the resource group to which the instance belongs.
        :param pulumi.Input[str] service_location: Anycast EIP instance access area. "international": Refers to areas outside of Mainland China.
        :param pulumi.Input[str] status: The status of the resource.
        :param pulumi.Input[Mapping[str, Any]] tags: List of resource-bound tags.
        """
        if anycast_eip_address_name is not None:
            pulumi.set(__self__, "anycast_eip_address_name", anycast_eip_address_name)
        if bandwidth is not None:
            pulumi.set(__self__, "bandwidth", bandwidth)
        if create_time is not None:
            pulumi.set(__self__, "create_time", create_time)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if internet_charge_type is not None:
            pulumi.set(__self__, "internet_charge_type", internet_charge_type)
        if payment_type is not None:
            pulumi.set(__self__, "payment_type", payment_type)
        if resource_group_id is not None:
            pulumi.set(__self__, "resource_group_id", resource_group_id)
        if service_location is not None:
            pulumi.set(__self__, "service_location", service_location)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="anycastEipAddressName")
    def anycast_eip_address_name(self) -> Optional[pulumi.Input[str]]:
        """
        Anycast EIP instance name.
        """
        return pulumi.get(self, "anycast_eip_address_name")

    @anycast_eip_address_name.setter
    def anycast_eip_address_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "anycast_eip_address_name", value)

    @property
    @pulumi.getter
    def bandwidth(self) -> Optional[pulumi.Input[int]]:
        """
        The peak bandwidth of the Anycast EIP instance, in Mbps.
        """
        return pulumi.get(self, "bandwidth")

    @bandwidth.setter
    def bandwidth(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "bandwidth", value)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> Optional[pulumi.Input[str]]:
        """
        Anycast EIP instance creation time.
        """
        return pulumi.get(self, "create_time")

    @create_time.setter
    def create_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create_time", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Anycast EIP instance description.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="internetChargeType")
    def internet_charge_type(self) -> Optional[pulumi.Input[str]]:
        """
        The billing method of Anycast EIP instance. "PayByBandwidth": refers to the method of billing based on traffic.
        """
        return pulumi.get(self, "internet_charge_type")

    @internet_charge_type.setter
    def internet_charge_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "internet_charge_type", value)

    @property
    @pulumi.getter(name="paymentType")
    def payment_type(self) -> Optional[pulumi.Input[str]]:
        """
        The payment model of Anycast EIP instance. "PayAsYouGo": Refers to the post-paid mode.
        """
        return pulumi.get(self, "payment_type")

    @payment_type.setter
    def payment_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "payment_type", value)

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the resource group to which the instance belongs.
        """
        return pulumi.get(self, "resource_group_id")

    @resource_group_id.setter
    def resource_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_id", value)

    @property
    @pulumi.getter(name="serviceLocation")
    def service_location(self) -> Optional[pulumi.Input[str]]:
        """
        Anycast EIP instance access area. "international": Refers to areas outside of Mainland China.
        """
        return pulumi.get(self, "service_location")

    @service_location.setter
    def service_location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_location", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the resource.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        List of resource-bound tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "tags", value)


class AnycastEipAddress(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 anycast_eip_address_name: Optional[pulumi.Input[str]] = None,
                 bandwidth: Optional[pulumi.Input[int]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 internet_charge_type: Optional[pulumi.Input[str]] = None,
                 payment_type: Optional[pulumi.Input[str]] = None,
                 resource_group_id: Optional[pulumi.Input[str]] = None,
                 service_location: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 __props__=None):
        """
        Provides a Eipanycast Anycast Eip Address resource. Anycast Elastic IP Address.

        For information about Eipanycast Anycast Eip Address and how to use it, see [What is Anycast Eip Address](https://www.alibabacloud.com/help/en/anycast-eip/latest/api-eipanycast-2020-03-09-allocateanycasteipaddress).

        > **NOTE:** Available since v1.113.0.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "tf-example"
        default = alicloud.eipanycast.AnycastEipAddress("default",
            anycast_eip_address_name=name,
            description=name,
            bandwidth=200,
            service_location="international",
            internet_charge_type="PayByTraffic",
            payment_type="PayAsYouGo")
        ```

        ## Import

        Eipanycast Anycast Eip Address can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:eipanycast/anycastEipAddress:AnycastEipAddress example <id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] anycast_eip_address_name: Anycast EIP instance name.
        :param pulumi.Input[int] bandwidth: The peak bandwidth of the Anycast EIP instance, in Mbps.
        :param pulumi.Input[str] description: Anycast EIP instance description.
        :param pulumi.Input[str] internet_charge_type: The billing method of Anycast EIP instance. "PayByBandwidth": refers to the method of billing based on traffic.
        :param pulumi.Input[str] payment_type: The payment model of Anycast EIP instance. "PayAsYouGo": Refers to the post-paid mode.
        :param pulumi.Input[str] resource_group_id: The ID of the resource group to which the instance belongs.
        :param pulumi.Input[str] service_location: Anycast EIP instance access area. "international": Refers to areas outside of Mainland China.
        :param pulumi.Input[Mapping[str, Any]] tags: List of resource-bound tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AnycastEipAddressArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Eipanycast Anycast Eip Address resource. Anycast Elastic IP Address.

        For information about Eipanycast Anycast Eip Address and how to use it, see [What is Anycast Eip Address](https://www.alibabacloud.com/help/en/anycast-eip/latest/api-eipanycast-2020-03-09-allocateanycasteipaddress).

        > **NOTE:** Available since v1.113.0.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "tf-example"
        default = alicloud.eipanycast.AnycastEipAddress("default",
            anycast_eip_address_name=name,
            description=name,
            bandwidth=200,
            service_location="international",
            internet_charge_type="PayByTraffic",
            payment_type="PayAsYouGo")
        ```

        ## Import

        Eipanycast Anycast Eip Address can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:eipanycast/anycastEipAddress:AnycastEipAddress example <id>
        ```

        :param str resource_name: The name of the resource.
        :param AnycastEipAddressArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AnycastEipAddressArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 anycast_eip_address_name: Optional[pulumi.Input[str]] = None,
                 bandwidth: Optional[pulumi.Input[int]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 internet_charge_type: Optional[pulumi.Input[str]] = None,
                 payment_type: Optional[pulumi.Input[str]] = None,
                 resource_group_id: Optional[pulumi.Input[str]] = None,
                 service_location: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AnycastEipAddressArgs.__new__(AnycastEipAddressArgs)

            __props__.__dict__["anycast_eip_address_name"] = anycast_eip_address_name
            __props__.__dict__["bandwidth"] = bandwidth
            __props__.__dict__["description"] = description
            __props__.__dict__["internet_charge_type"] = internet_charge_type
            __props__.__dict__["payment_type"] = payment_type
            __props__.__dict__["resource_group_id"] = resource_group_id
            if service_location is None and not opts.urn:
                raise TypeError("Missing required property 'service_location'")
            __props__.__dict__["service_location"] = service_location
            __props__.__dict__["tags"] = tags
            __props__.__dict__["create_time"] = None
            __props__.__dict__["status"] = None
        super(AnycastEipAddress, __self__).__init__(
            'alicloud:eipanycast/anycastEipAddress:AnycastEipAddress',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            anycast_eip_address_name: Optional[pulumi.Input[str]] = None,
            bandwidth: Optional[pulumi.Input[int]] = None,
            create_time: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            internet_charge_type: Optional[pulumi.Input[str]] = None,
            payment_type: Optional[pulumi.Input[str]] = None,
            resource_group_id: Optional[pulumi.Input[str]] = None,
            service_location: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, Any]]] = None) -> 'AnycastEipAddress':
        """
        Get an existing AnycastEipAddress resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] anycast_eip_address_name: Anycast EIP instance name.
        :param pulumi.Input[int] bandwidth: The peak bandwidth of the Anycast EIP instance, in Mbps.
        :param pulumi.Input[str] create_time: Anycast EIP instance creation time.
        :param pulumi.Input[str] description: Anycast EIP instance description.
        :param pulumi.Input[str] internet_charge_type: The billing method of Anycast EIP instance. "PayByBandwidth": refers to the method of billing based on traffic.
        :param pulumi.Input[str] payment_type: The payment model of Anycast EIP instance. "PayAsYouGo": Refers to the post-paid mode.
        :param pulumi.Input[str] resource_group_id: The ID of the resource group to which the instance belongs.
        :param pulumi.Input[str] service_location: Anycast EIP instance access area. "international": Refers to areas outside of Mainland China.
        :param pulumi.Input[str] status: The status of the resource.
        :param pulumi.Input[Mapping[str, Any]] tags: List of resource-bound tags.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AnycastEipAddressState.__new__(_AnycastEipAddressState)

        __props__.__dict__["anycast_eip_address_name"] = anycast_eip_address_name
        __props__.__dict__["bandwidth"] = bandwidth
        __props__.__dict__["create_time"] = create_time
        __props__.__dict__["description"] = description
        __props__.__dict__["internet_charge_type"] = internet_charge_type
        __props__.__dict__["payment_type"] = payment_type
        __props__.__dict__["resource_group_id"] = resource_group_id
        __props__.__dict__["service_location"] = service_location
        __props__.__dict__["status"] = status
        __props__.__dict__["tags"] = tags
        return AnycastEipAddress(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="anycastEipAddressName")
    def anycast_eip_address_name(self) -> pulumi.Output[Optional[str]]:
        """
        Anycast EIP instance name.
        """
        return pulumi.get(self, "anycast_eip_address_name")

    @property
    @pulumi.getter
    def bandwidth(self) -> pulumi.Output[int]:
        """
        The peak bandwidth of the Anycast EIP instance, in Mbps.
        """
        return pulumi.get(self, "bandwidth")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        Anycast EIP instance creation time.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Anycast EIP instance description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="internetChargeType")
    def internet_charge_type(self) -> pulumi.Output[Optional[str]]:
        """
        The billing method of Anycast EIP instance. "PayByBandwidth": refers to the method of billing based on traffic.
        """
        return pulumi.get(self, "internet_charge_type")

    @property
    @pulumi.getter(name="paymentType")
    def payment_type(self) -> pulumi.Output[Optional[str]]:
        """
        The payment model of Anycast EIP instance. "PayAsYouGo": Refers to the post-paid mode.
        """
        return pulumi.get(self, "payment_type")

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> pulumi.Output[str]:
        """
        The ID of the resource group to which the instance belongs.
        """
        return pulumi.get(self, "resource_group_id")

    @property
    @pulumi.getter(name="serviceLocation")
    def service_location(self) -> pulumi.Output[str]:
        """
        Anycast EIP instance access area. "international": Refers to areas outside of Mainland China.
        """
        return pulumi.get(self, "service_location")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The status of the resource.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, Any]]]:
        """
        List of resource-bound tags.
        """
        return pulumi.get(self, "tags")

