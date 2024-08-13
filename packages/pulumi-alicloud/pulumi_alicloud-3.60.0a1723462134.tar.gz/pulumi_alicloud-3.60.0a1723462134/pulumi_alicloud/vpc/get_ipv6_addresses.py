# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetIpv6AddressesResult',
    'AwaitableGetIpv6AddressesResult',
    'get_ipv6_addresses',
    'get_ipv6_addresses_output',
]

@pulumi.output_type
class GetIpv6AddressesResult:
    """
    A collection of values returned by getIpv6Addresses.
    """
    def __init__(__self__, addresses=None, associated_instance_id=None, id=None, ids=None, names=None, output_file=None, status=None, vpc_id=None, vswitch_id=None):
        if addresses and not isinstance(addresses, list):
            raise TypeError("Expected argument 'addresses' to be a list")
        pulumi.set(__self__, "addresses", addresses)
        if associated_instance_id and not isinstance(associated_instance_id, str):
            raise TypeError("Expected argument 'associated_instance_id' to be a str")
        pulumi.set(__self__, "associated_instance_id", associated_instance_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        pulumi.set(__self__, "names", names)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if vpc_id and not isinstance(vpc_id, str):
            raise TypeError("Expected argument 'vpc_id' to be a str")
        pulumi.set(__self__, "vpc_id", vpc_id)
        if vswitch_id and not isinstance(vswitch_id, str):
            raise TypeError("Expected argument 'vswitch_id' to be a str")
        pulumi.set(__self__, "vswitch_id", vswitch_id)

    @property
    @pulumi.getter
    def addresses(self) -> Sequence['outputs.GetIpv6AddressesAddressResult']:
        return pulumi.get(self, "addresses")

    @property
    @pulumi.getter(name="associatedInstanceId")
    def associated_instance_id(self) -> Optional[str]:
        return pulumi.get(self, "associated_instance_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def ids(self) -> Sequence[str]:
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter
    def names(self) -> Sequence[str]:
        return pulumi.get(self, "names")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> Optional[str]:
        return pulumi.get(self, "vpc_id")

    @property
    @pulumi.getter(name="vswitchId")
    def vswitch_id(self) -> Optional[str]:
        return pulumi.get(self, "vswitch_id")


class AwaitableGetIpv6AddressesResult(GetIpv6AddressesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetIpv6AddressesResult(
            addresses=self.addresses,
            associated_instance_id=self.associated_instance_id,
            id=self.id,
            ids=self.ids,
            names=self.names,
            output_file=self.output_file,
            status=self.status,
            vpc_id=self.vpc_id,
            vswitch_id=self.vswitch_id)


def get_ipv6_addresses(associated_instance_id: Optional[str] = None,
                       ids: Optional[Sequence[str]] = None,
                       output_file: Optional[str] = None,
                       status: Optional[str] = None,
                       vpc_id: Optional[str] = None,
                       vswitch_id: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetIpv6AddressesResult:
    """
    This data source provides the Vpc Ipv6 Addresses of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.142.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    associated_instance_id = alicloud.vpc.get_ipv6_addresses(associated_instance_id="example_value")
    pulumi.export("vpcIpv6AddressId1", associated_instance_id.addresses[0].id)
    vswitch_id = alicloud.vpc.get_ipv6_addresses(vswitch_id="example_value")
    pulumi.export("vpcIpv6AddressId2", vswitch_id.addresses[0].id)
    vpc_id = alicloud.vpc.get_ipv6_addresses(vpc_id="example_value")
    pulumi.export("vpcIpv6AddressId3", vpc_id.addresses[0].id)
    status = alicloud.vpc.get_ipv6_addresses(status="Available")
    pulumi.export("vpcIpv6AddressId4", status.addresses[0].id)
    ```


    :param str associated_instance_id: The ID of the instance that is assigned the IPv6 address.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str status: The status of the IPv6 address. Valid values:`Pending` or `Available`. 
           - `Pending`: The IPv6 address is being configured.
           - `Available`: The IPv6 address is available.
    :param str vpc_id: The ID of the VPC to which the IPv6 address belongs.
    :param str vswitch_id: The ID of the vSwitch to which the IPv6 address belongs.
    """
    __args__ = dict()
    __args__['associatedInstanceId'] = associated_instance_id
    __args__['ids'] = ids
    __args__['outputFile'] = output_file
    __args__['status'] = status
    __args__['vpcId'] = vpc_id
    __args__['vswitchId'] = vswitch_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:vpc/getIpv6Addresses:getIpv6Addresses', __args__, opts=opts, typ=GetIpv6AddressesResult).value

    return AwaitableGetIpv6AddressesResult(
        addresses=pulumi.get(__ret__, 'addresses'),
        associated_instance_id=pulumi.get(__ret__, 'associated_instance_id'),
        id=pulumi.get(__ret__, 'id'),
        ids=pulumi.get(__ret__, 'ids'),
        names=pulumi.get(__ret__, 'names'),
        output_file=pulumi.get(__ret__, 'output_file'),
        status=pulumi.get(__ret__, 'status'),
        vpc_id=pulumi.get(__ret__, 'vpc_id'),
        vswitch_id=pulumi.get(__ret__, 'vswitch_id'))


@_utilities.lift_output_func(get_ipv6_addresses)
def get_ipv6_addresses_output(associated_instance_id: Optional[pulumi.Input[Optional[str]]] = None,
                              ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                              output_file: Optional[pulumi.Input[Optional[str]]] = None,
                              status: Optional[pulumi.Input[Optional[str]]] = None,
                              vpc_id: Optional[pulumi.Input[Optional[str]]] = None,
                              vswitch_id: Optional[pulumi.Input[Optional[str]]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetIpv6AddressesResult]:
    """
    This data source provides the Vpc Ipv6 Addresses of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.142.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    associated_instance_id = alicloud.vpc.get_ipv6_addresses(associated_instance_id="example_value")
    pulumi.export("vpcIpv6AddressId1", associated_instance_id.addresses[0].id)
    vswitch_id = alicloud.vpc.get_ipv6_addresses(vswitch_id="example_value")
    pulumi.export("vpcIpv6AddressId2", vswitch_id.addresses[0].id)
    vpc_id = alicloud.vpc.get_ipv6_addresses(vpc_id="example_value")
    pulumi.export("vpcIpv6AddressId3", vpc_id.addresses[0].id)
    status = alicloud.vpc.get_ipv6_addresses(status="Available")
    pulumi.export("vpcIpv6AddressId4", status.addresses[0].id)
    ```


    :param str associated_instance_id: The ID of the instance that is assigned the IPv6 address.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str status: The status of the IPv6 address. Valid values:`Pending` or `Available`. 
           - `Pending`: The IPv6 address is being configured.
           - `Available`: The IPv6 address is available.
    :param str vpc_id: The ID of the VPC to which the IPv6 address belongs.
    :param str vswitch_id: The ID of the vSwitch to which the IPv6 address belongs.
    """
    ...
