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
    'GetBasicAccelerateIpsResult',
    'AwaitableGetBasicAccelerateIpsResult',
    'get_basic_accelerate_ips',
    'get_basic_accelerate_ips_output',
]

@pulumi.output_type
class GetBasicAccelerateIpsResult:
    """
    A collection of values returned by getBasicAccelerateIps.
    """
    def __init__(__self__, accelerate_ip_address=None, accelerate_ip_id=None, id=None, ids=None, ip_set_id=None, ips=None, output_file=None, status=None):
        if accelerate_ip_address and not isinstance(accelerate_ip_address, str):
            raise TypeError("Expected argument 'accelerate_ip_address' to be a str")
        pulumi.set(__self__, "accelerate_ip_address", accelerate_ip_address)
        if accelerate_ip_id and not isinstance(accelerate_ip_id, str):
            raise TypeError("Expected argument 'accelerate_ip_id' to be a str")
        pulumi.set(__self__, "accelerate_ip_id", accelerate_ip_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if ip_set_id and not isinstance(ip_set_id, str):
            raise TypeError("Expected argument 'ip_set_id' to be a str")
        pulumi.set(__self__, "ip_set_id", ip_set_id)
        if ips and not isinstance(ips, list):
            raise TypeError("Expected argument 'ips' to be a list")
        pulumi.set(__self__, "ips", ips)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="accelerateIpAddress")
    def accelerate_ip_address(self) -> Optional[str]:
        """
        The address of the Basic Accelerate IP.
        """
        return pulumi.get(self, "accelerate_ip_address")

    @property
    @pulumi.getter(name="accelerateIpId")
    def accelerate_ip_id(self) -> Optional[str]:
        """
        The id of the Basic Accelerate IP.
        """
        return pulumi.get(self, "accelerate_ip_id")

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
    @pulumi.getter(name="ipSetId")
    def ip_set_id(self) -> str:
        """
        The ID of the Basic Ip Set.
        """
        return pulumi.get(self, "ip_set_id")

    @property
    @pulumi.getter
    def ips(self) -> Sequence['outputs.GetBasicAccelerateIpsIpResult']:
        """
        A list of Global Accelerator Basic Accelerate IPs. Each element contains the following attributes:
        """
        return pulumi.get(self, "ips")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        The status of the Basic Accelerate IP instance.
        """
        return pulumi.get(self, "status")


class AwaitableGetBasicAccelerateIpsResult(GetBasicAccelerateIpsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetBasicAccelerateIpsResult(
            accelerate_ip_address=self.accelerate_ip_address,
            accelerate_ip_id=self.accelerate_ip_id,
            id=self.id,
            ids=self.ids,
            ip_set_id=self.ip_set_id,
            ips=self.ips,
            output_file=self.output_file,
            status=self.status)


def get_basic_accelerate_ips(accelerate_ip_address: Optional[str] = None,
                             accelerate_ip_id: Optional[str] = None,
                             ids: Optional[Sequence[str]] = None,
                             ip_set_id: Optional[str] = None,
                             output_file: Optional[str] = None,
                             status: Optional[str] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetBasicAccelerateIpsResult:
    """
    This data source provides the Global Accelerator (GA) Basic Accelerate IPs of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.194.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    ids = alicloud.ga.get_basic_accelerate_ips(ids=["example_id"],
        ip_set_id="example_ip_set_id")
    pulumi.export("gaBasicAccelerateIpId1", ids.ips[0].id)
    ```


    :param str accelerate_ip_address: The address of the Basic Accelerate IP.
    :param str accelerate_ip_id: The id of the Basic Accelerate IP.
    :param Sequence[str] ids: A list of Global Accelerator Basic Accelerate IP IDs.
    :param str ip_set_id: The ID of the Basic Ip Set.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str status: The status of the Global Accelerator Basic Accelerate IP instance. Valid Value: `active`, `binding`, `bound`, `unbinding`, `deleting`.
    """
    __args__ = dict()
    __args__['accelerateIpAddress'] = accelerate_ip_address
    __args__['accelerateIpId'] = accelerate_ip_id
    __args__['ids'] = ids
    __args__['ipSetId'] = ip_set_id
    __args__['outputFile'] = output_file
    __args__['status'] = status
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:ga/getBasicAccelerateIps:getBasicAccelerateIps', __args__, opts=opts, typ=GetBasicAccelerateIpsResult).value

    return AwaitableGetBasicAccelerateIpsResult(
        accelerate_ip_address=pulumi.get(__ret__, 'accelerate_ip_address'),
        accelerate_ip_id=pulumi.get(__ret__, 'accelerate_ip_id'),
        id=pulumi.get(__ret__, 'id'),
        ids=pulumi.get(__ret__, 'ids'),
        ip_set_id=pulumi.get(__ret__, 'ip_set_id'),
        ips=pulumi.get(__ret__, 'ips'),
        output_file=pulumi.get(__ret__, 'output_file'),
        status=pulumi.get(__ret__, 'status'))


@_utilities.lift_output_func(get_basic_accelerate_ips)
def get_basic_accelerate_ips_output(accelerate_ip_address: Optional[pulumi.Input[Optional[str]]] = None,
                                    accelerate_ip_id: Optional[pulumi.Input[Optional[str]]] = None,
                                    ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                                    ip_set_id: Optional[pulumi.Input[str]] = None,
                                    output_file: Optional[pulumi.Input[Optional[str]]] = None,
                                    status: Optional[pulumi.Input[Optional[str]]] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetBasicAccelerateIpsResult]:
    """
    This data source provides the Global Accelerator (GA) Basic Accelerate IPs of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.194.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    ids = alicloud.ga.get_basic_accelerate_ips(ids=["example_id"],
        ip_set_id="example_ip_set_id")
    pulumi.export("gaBasicAccelerateIpId1", ids.ips[0].id)
    ```


    :param str accelerate_ip_address: The address of the Basic Accelerate IP.
    :param str accelerate_ip_id: The id of the Basic Accelerate IP.
    :param Sequence[str] ids: A list of Global Accelerator Basic Accelerate IP IDs.
    :param str ip_set_id: The ID of the Basic Ip Set.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str status: The status of the Global Accelerator Basic Accelerate IP instance. Valid Value: `active`, `binding`, `bound`, `unbinding`, `deleting`.
    """
    ...
