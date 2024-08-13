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
    'GetAccessPointsResult',
    'AwaitableGetAccessPointsResult',
    'get_access_points',
    'get_access_points_output',
]

@pulumi.output_type
class GetAccessPointsResult:
    """
    A collection of values returned by getAccessPoints.
    """
    def __init__(__self__, id=None, ids=None, name_regex=None, names=None, output_file=None, points=None, status=None):
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
        if points and not isinstance(points, list):
            raise TypeError("Expected argument 'points' to be a list")
        pulumi.set(__self__, "points", points)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)

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
        return pulumi.get(self, "names")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter
    def points(self) -> Sequence['outputs.GetAccessPointsPointResult']:
        return pulumi.get(self, "points")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        return pulumi.get(self, "status")


class AwaitableGetAccessPointsResult(GetAccessPointsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAccessPointsResult(
            id=self.id,
            ids=self.ids,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file,
            points=self.points,
            status=self.status)


def get_access_points(ids: Optional[Sequence[str]] = None,
                      name_regex: Optional[str] = None,
                      output_file: Optional[str] = None,
                      status: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAccessPointsResult:
    """
    This data source provides the Express Connect Access Points of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.132.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    ids = alicloud.expressconnect.get_access_points(ids=["ap-cn-hangzhou-yh-C"])
    pulumi.export("expressConnectAccessPointId1", ids.points[0].id)
    name_regex = alicloud.expressconnect.get_access_points(name_regex="^杭州-")
    pulumi.export("expressConnectAccessPointId2", name_regex.points[0].id)
    ```


    :param Sequence[str] ids: A list of Access Point IDs.
    :param str name_regex: A regex string to filter results by Access Point name.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str status: The Physical Connection to Which the Access Point State. Valid values: `disabled`, `full`, `hot`, `recommended`.
    """
    __args__ = dict()
    __args__['ids'] = ids
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    __args__['status'] = status
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:expressconnect/getAccessPoints:getAccessPoints', __args__, opts=opts, typ=GetAccessPointsResult).value

    return AwaitableGetAccessPointsResult(
        id=pulumi.get(__ret__, 'id'),
        ids=pulumi.get(__ret__, 'ids'),
        name_regex=pulumi.get(__ret__, 'name_regex'),
        names=pulumi.get(__ret__, 'names'),
        output_file=pulumi.get(__ret__, 'output_file'),
        points=pulumi.get(__ret__, 'points'),
        status=pulumi.get(__ret__, 'status'))


@_utilities.lift_output_func(get_access_points)
def get_access_points_output(ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                             name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                             output_file: Optional[pulumi.Input[Optional[str]]] = None,
                             status: Optional[pulumi.Input[Optional[str]]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAccessPointsResult]:
    """
    This data source provides the Express Connect Access Points of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.132.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    ids = alicloud.expressconnect.get_access_points(ids=["ap-cn-hangzhou-yh-C"])
    pulumi.export("expressConnectAccessPointId1", ids.points[0].id)
    name_regex = alicloud.expressconnect.get_access_points(name_regex="^杭州-")
    pulumi.export("expressConnectAccessPointId2", name_regex.points[0].id)
    ```


    :param Sequence[str] ids: A list of Access Point IDs.
    :param str name_regex: A regex string to filter results by Access Point name.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str status: The Physical Connection to Which the Access Point State. Valid values: `disabled`, `full`, `hot`, `recommended`.
    """
    ...
