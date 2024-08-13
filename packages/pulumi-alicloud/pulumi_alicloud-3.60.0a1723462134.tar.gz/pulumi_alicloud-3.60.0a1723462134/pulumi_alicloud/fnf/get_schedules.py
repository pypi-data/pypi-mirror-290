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
    'GetSchedulesResult',
    'AwaitableGetSchedulesResult',
    'get_schedules',
    'get_schedules_output',
]

@pulumi.output_type
class GetSchedulesResult:
    """
    A collection of values returned by getSchedules.
    """
    def __init__(__self__, flow_name=None, id=None, ids=None, limit=None, name_regex=None, names=None, output_file=None, schedules=None):
        if flow_name and not isinstance(flow_name, str):
            raise TypeError("Expected argument 'flow_name' to be a str")
        pulumi.set(__self__, "flow_name", flow_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if limit and not isinstance(limit, int):
            raise TypeError("Expected argument 'limit' to be a int")
        pulumi.set(__self__, "limit", limit)
        if name_regex and not isinstance(name_regex, str):
            raise TypeError("Expected argument 'name_regex' to be a str")
        pulumi.set(__self__, "name_regex", name_regex)
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        pulumi.set(__self__, "names", names)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if schedules and not isinstance(schedules, list):
            raise TypeError("Expected argument 'schedules' to be a list")
        pulumi.set(__self__, "schedules", schedules)

    @property
    @pulumi.getter(name="flowName")
    def flow_name(self) -> str:
        return pulumi.get(self, "flow_name")

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
    def limit(self) -> Optional[int]:
        return pulumi.get(self, "limit")

    @property
    @pulumi.getter(name="nameRegex")
    def name_regex(self) -> Optional[str]:
        return pulumi.get(self, "name_regex")

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
    def schedules(self) -> Sequence['outputs.GetSchedulesScheduleResult']:
        return pulumi.get(self, "schedules")


class AwaitableGetSchedulesResult(GetSchedulesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSchedulesResult(
            flow_name=self.flow_name,
            id=self.id,
            ids=self.ids,
            limit=self.limit,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file,
            schedules=self.schedules)


def get_schedules(flow_name: Optional[str] = None,
                  ids: Optional[Sequence[str]] = None,
                  limit: Optional[int] = None,
                  name_regex: Optional[str] = None,
                  output_file: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSchedulesResult:
    """
    This data source provides the Fnf Schedules of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.105.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    example = alicloud.fnf.get_schedules(flow_name="example_value",
        ids=["example_value"],
        name_regex="the_resource_name")
    pulumi.export("firstFnfScheduleId", example.schedules[0].id)
    ```


    :param str flow_name: The name of the flow bound to the time-based schedule you want to create.
    :param Sequence[str] ids: A list of Schedule IDs.
    :param int limit: The number of resource queries.
    :param str name_regex: A regex string to filter results by Schedule name.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    """
    __args__ = dict()
    __args__['flowName'] = flow_name
    __args__['ids'] = ids
    __args__['limit'] = limit
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:fnf/getSchedules:getSchedules', __args__, opts=opts, typ=GetSchedulesResult).value

    return AwaitableGetSchedulesResult(
        flow_name=pulumi.get(__ret__, 'flow_name'),
        id=pulumi.get(__ret__, 'id'),
        ids=pulumi.get(__ret__, 'ids'),
        limit=pulumi.get(__ret__, 'limit'),
        name_regex=pulumi.get(__ret__, 'name_regex'),
        names=pulumi.get(__ret__, 'names'),
        output_file=pulumi.get(__ret__, 'output_file'),
        schedules=pulumi.get(__ret__, 'schedules'))


@_utilities.lift_output_func(get_schedules)
def get_schedules_output(flow_name: Optional[pulumi.Input[str]] = None,
                         ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                         limit: Optional[pulumi.Input[Optional[int]]] = None,
                         name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                         output_file: Optional[pulumi.Input[Optional[str]]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSchedulesResult]:
    """
    This data source provides the Fnf Schedules of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.105.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    example = alicloud.fnf.get_schedules(flow_name="example_value",
        ids=["example_value"],
        name_regex="the_resource_name")
    pulumi.export("firstFnfScheduleId", example.schedules[0].id)
    ```


    :param str flow_name: The name of the flow bound to the time-based schedule you want to create.
    :param Sequence[str] ids: A list of Schedule IDs.
    :param int limit: The number of resource queries.
    :param str name_regex: A regex string to filter results by Schedule name.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    """
    ...
