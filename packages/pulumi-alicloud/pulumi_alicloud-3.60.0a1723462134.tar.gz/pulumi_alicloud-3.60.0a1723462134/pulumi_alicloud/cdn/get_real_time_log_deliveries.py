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
    'GetRealTimeLogDeliveriesResult',
    'AwaitableGetRealTimeLogDeliveriesResult',
    'get_real_time_log_deliveries',
    'get_real_time_log_deliveries_output',
]

@pulumi.output_type
class GetRealTimeLogDeliveriesResult:
    """
    A collection of values returned by getRealTimeLogDeliveries.
    """
    def __init__(__self__, deliveries=None, domain=None, id=None, output_file=None, status=None):
        if deliveries and not isinstance(deliveries, list):
            raise TypeError("Expected argument 'deliveries' to be a list")
        pulumi.set(__self__, "deliveries", deliveries)
        if domain and not isinstance(domain, str):
            raise TypeError("Expected argument 'domain' to be a str")
        pulumi.set(__self__, "domain", domain)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def deliveries(self) -> Sequence['outputs.GetRealTimeLogDeliveriesDeliveryResult']:
        return pulumi.get(self, "deliveries")

    @property
    @pulumi.getter
    def domain(self) -> str:
        return pulumi.get(self, "domain")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        return pulumi.get(self, "status")


class AwaitableGetRealTimeLogDeliveriesResult(GetRealTimeLogDeliveriesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRealTimeLogDeliveriesResult(
            deliveries=self.deliveries,
            domain=self.domain,
            id=self.id,
            output_file=self.output_file,
            status=self.status)


def get_real_time_log_deliveries(domain: Optional[str] = None,
                                 output_file: Optional[str] = None,
                                 status: Optional[str] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRealTimeLogDeliveriesResult:
    """
    This data source provides the Cdn Real Time Log Deliveries of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.134.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    example = alicloud.cdn.get_real_time_log_deliveries(domain="example_value")
    pulumi.export("cdnRealTimeLogDelivery1", example.deliveries[0].id)
    ```


    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str status: The status of the real-time log delivery feature. Valid Values: `online` and `offline`.
    """
    __args__ = dict()
    __args__['domain'] = domain
    __args__['outputFile'] = output_file
    __args__['status'] = status
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:cdn/getRealTimeLogDeliveries:getRealTimeLogDeliveries', __args__, opts=opts, typ=GetRealTimeLogDeliveriesResult).value

    return AwaitableGetRealTimeLogDeliveriesResult(
        deliveries=pulumi.get(__ret__, 'deliveries'),
        domain=pulumi.get(__ret__, 'domain'),
        id=pulumi.get(__ret__, 'id'),
        output_file=pulumi.get(__ret__, 'output_file'),
        status=pulumi.get(__ret__, 'status'))


@_utilities.lift_output_func(get_real_time_log_deliveries)
def get_real_time_log_deliveries_output(domain: Optional[pulumi.Input[str]] = None,
                                        output_file: Optional[pulumi.Input[Optional[str]]] = None,
                                        status: Optional[pulumi.Input[Optional[str]]] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRealTimeLogDeliveriesResult]:
    """
    This data source provides the Cdn Real Time Log Deliveries of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.134.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    example = alicloud.cdn.get_real_time_log_deliveries(domain="example_value")
    pulumi.export("cdnRealTimeLogDelivery1", example.deliveries[0].id)
    ```


    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str status: The status of the real-time log delivery feature. Valid Values: `online` and `offline`.
    """
    ...
