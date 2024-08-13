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
    'GetAcceleratorsResult',
    'AwaitableGetAcceleratorsResult',
    'get_accelerators',
    'get_accelerators_output',
]

@pulumi.output_type
class GetAcceleratorsResult:
    """
    A collection of values returned by getAccelerators.
    """
    def __init__(__self__, accelerators=None, bandwidth_billing_type=None, id=None, ids=None, name_regex=None, names=None, output_file=None, status=None):
        if accelerators and not isinstance(accelerators, list):
            raise TypeError("Expected argument 'accelerators' to be a list")
        pulumi.set(__self__, "accelerators", accelerators)
        if bandwidth_billing_type and not isinstance(bandwidth_billing_type, str):
            raise TypeError("Expected argument 'bandwidth_billing_type' to be a str")
        pulumi.set(__self__, "bandwidth_billing_type", bandwidth_billing_type)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if name_regex and not isinstance(name_regex, str):
            raise TypeError("Expected argument 'name_regex' to be a str")
        pulumi.set(__self__, "name_regex", name_regex)
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        pulumi.set(__self__, "names", names)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def accelerators(self) -> Sequence['outputs.GetAcceleratorsAcceleratorResult']:
        """
        A list of Ga Accelerators. Each element contains the following attributes:
        """
        return pulumi.get(self, "accelerators")

    @property
    @pulumi.getter(name="bandwidthBillingType")
    def bandwidth_billing_type(self) -> Optional[str]:
        return pulumi.get(self, "bandwidth_billing_type")

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
    @pulumi.getter(name="nameRegex")
    def name_regex(self) -> Optional[str]:
        return pulumi.get(self, "name_regex")

    @property
    @pulumi.getter
    def names(self) -> Sequence[str]:
        """
        A list of Accelerator names.
        """
        return pulumi.get(self, "names")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        The status of the GA instance.
        """
        return pulumi.get(self, "status")


class AwaitableGetAcceleratorsResult(GetAcceleratorsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAcceleratorsResult(
            accelerators=self.accelerators,
            bandwidth_billing_type=self.bandwidth_billing_type,
            id=self.id,
            ids=self.ids,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file,
            status=self.status)


def get_accelerators(bandwidth_billing_type: Optional[str] = None,
                     ids: Optional[Sequence[str]] = None,
                     name_regex: Optional[str] = None,
                     output_file: Optional[str] = None,
                     status: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAcceleratorsResult:
    """
    This data source provides the Global Accelerator (GA) Accelerators of the current Alibaba Cloud user.

    > **NOTE:** Available since v1.111.0.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    example = alicloud.ga.get_accelerators(name_regex="tf")
    pulumi.export("firstGaAcceleratorId", example.accelerators[0].id)
    ```


    :param str bandwidth_billing_type: The bandwidth billing method. Default value: `BandwidthPackage`. Valid values:
           - `BandwidthPackage`: billed based on bandwidth plans.
           - `CDT`: billed based on data transfer.
    :param Sequence[str] ids: A list of Accelerator IDs.
    :param str name_regex: A regex string to filter results by Accelerator name.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str status: The status of the GA instance. Valid values: `active`, `binding`, `configuring`, `deleting`, `finacialLocked`, `init`, `unbinding`.
    """
    __args__ = dict()
    __args__['bandwidthBillingType'] = bandwidth_billing_type
    __args__['ids'] = ids
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    __args__['status'] = status
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:ga/getAccelerators:getAccelerators', __args__, opts=opts, typ=GetAcceleratorsResult).value

    return AwaitableGetAcceleratorsResult(
        accelerators=pulumi.get(__ret__, 'accelerators'),
        bandwidth_billing_type=pulumi.get(__ret__, 'bandwidth_billing_type'),
        id=pulumi.get(__ret__, 'id'),
        ids=pulumi.get(__ret__, 'ids'),
        name_regex=pulumi.get(__ret__, 'name_regex'),
        names=pulumi.get(__ret__, 'names'),
        output_file=pulumi.get(__ret__, 'output_file'),
        status=pulumi.get(__ret__, 'status'))


@_utilities.lift_output_func(get_accelerators)
def get_accelerators_output(bandwidth_billing_type: Optional[pulumi.Input[Optional[str]]] = None,
                            ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                            name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                            output_file: Optional[pulumi.Input[Optional[str]]] = None,
                            status: Optional[pulumi.Input[Optional[str]]] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAcceleratorsResult]:
    """
    This data source provides the Global Accelerator (GA) Accelerators of the current Alibaba Cloud user.

    > **NOTE:** Available since v1.111.0.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    example = alicloud.ga.get_accelerators(name_regex="tf")
    pulumi.export("firstGaAcceleratorId", example.accelerators[0].id)
    ```


    :param str bandwidth_billing_type: The bandwidth billing method. Default value: `BandwidthPackage`. Valid values:
           - `BandwidthPackage`: billed based on bandwidth plans.
           - `CDT`: billed based on data transfer.
    :param Sequence[str] ids: A list of Accelerator IDs.
    :param str name_regex: A regex string to filter results by Accelerator name.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str status: The status of the GA instance. Valid values: `active`, `binding`, `configuring`, `deleting`, `finacialLocked`, `init`, `unbinding`.
    """
    ...
