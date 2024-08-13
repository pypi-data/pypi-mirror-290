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
    'GetSlotsResult',
    'AwaitableGetSlotsResult',
    'get_slots',
    'get_slots_output',
]

@pulumi.output_type
class GetSlotsResult:
    """
    A collection of values returned by getSlots.
    """
    def __init__(__self__, db_instance_id=None, id=None, output_file=None, resource_group_id=None, slots=None):
        if db_instance_id and not isinstance(db_instance_id, str):
            raise TypeError("Expected argument 'db_instance_id' to be a str")
        pulumi.set(__self__, "db_instance_id", db_instance_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if resource_group_id and not isinstance(resource_group_id, str):
            raise TypeError("Expected argument 'resource_group_id' to be a str")
        pulumi.set(__self__, "resource_group_id", resource_group_id)
        if slots and not isinstance(slots, list):
            raise TypeError("Expected argument 'slots' to be a list")
        pulumi.set(__self__, "slots", slots)

    @property
    @pulumi.getter(name="dbInstanceId")
    def db_instance_id(self) -> str:
        return pulumi.get(self, "db_instance_id")

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
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> Optional[str]:
        return pulumi.get(self, "resource_group_id")

    @property
    @pulumi.getter
    def slots(self) -> Sequence['outputs.GetSlotsSlotResult']:
        """
        A list of Rds Replication Slots. Each element contains the following attributes:
        """
        return pulumi.get(self, "slots")


class AwaitableGetSlotsResult(GetSlotsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSlotsResult(
            db_instance_id=self.db_instance_id,
            id=self.id,
            output_file=self.output_file,
            resource_group_id=self.resource_group_id,
            slots=self.slots)


def get_slots(db_instance_id: Optional[str] = None,
              output_file: Optional[str] = None,
              resource_group_id: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSlotsResult:
    """
    This data source provides the Rds Replication Slots of the current Alibaba Cloud user.

    > **NOTE:** Available since v1.204.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    example = alicloud.rds.get_slots(db_instance_id="example_value")
    pulumi.export("firstRdsSlotsName", example.slots[0].slot_name)
    ```


    :param str db_instance_id: The db instance id.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str resource_group_id: The resource group id.
    """
    __args__ = dict()
    __args__['dbInstanceId'] = db_instance_id
    __args__['outputFile'] = output_file
    __args__['resourceGroupId'] = resource_group_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:rds/getSlots:getSlots', __args__, opts=opts, typ=GetSlotsResult).value

    return AwaitableGetSlotsResult(
        db_instance_id=pulumi.get(__ret__, 'db_instance_id'),
        id=pulumi.get(__ret__, 'id'),
        output_file=pulumi.get(__ret__, 'output_file'),
        resource_group_id=pulumi.get(__ret__, 'resource_group_id'),
        slots=pulumi.get(__ret__, 'slots'))


@_utilities.lift_output_func(get_slots)
def get_slots_output(db_instance_id: Optional[pulumi.Input[str]] = None,
                     output_file: Optional[pulumi.Input[Optional[str]]] = None,
                     resource_group_id: Optional[pulumi.Input[Optional[str]]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSlotsResult]:
    """
    This data source provides the Rds Replication Slots of the current Alibaba Cloud user.

    > **NOTE:** Available since v1.204.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    example = alicloud.rds.get_slots(db_instance_id="example_value")
    pulumi.export("firstRdsSlotsName", example.slots[0].slot_name)
    ```


    :param str db_instance_id: The db instance id.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str resource_group_id: The resource group id.
    """
    ...
