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
    'GetPrometheusResult',
    'AwaitableGetPrometheusResult',
    'get_prometheus',
    'get_prometheus_output',
]

@pulumi.output_type
class GetPrometheusResult:
    """
    A collection of values returned by getPrometheus.
    """
    def __init__(__self__, enable_details=None, id=None, ids=None, name_regex=None, names=None, output_file=None, prometheis=None, resource_group_id=None, tags=None):
        if enable_details and not isinstance(enable_details, bool):
            raise TypeError("Expected argument 'enable_details' to be a bool")
        pulumi.set(__self__, "enable_details", enable_details)
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
        if prometheis and not isinstance(prometheis, list):
            raise TypeError("Expected argument 'prometheis' to be a list")
        pulumi.set(__self__, "prometheis", prometheis)
        if resource_group_id and not isinstance(resource_group_id, str):
            raise TypeError("Expected argument 'resource_group_id' to be a str")
        pulumi.set(__self__, "resource_group_id", resource_group_id)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="enableDetails")
    def enable_details(self) -> Optional[bool]:
        return pulumi.get(self, "enable_details")

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
        A list of Prometheus names.
        """
        return pulumi.get(self, "names")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter
    def prometheis(self) -> Sequence['outputs.GetPrometheusPrometheiResult']:
        """
        A list of Prometheus. Each element contains the following attributes:
        """
        return pulumi.get(self, "prometheis")

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> Optional[str]:
        """
        The ID of the resource group.
        """
        return pulumi.get(self, "resource_group_id")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, Any]]:
        """
        The tag of the Prometheus.
        """
        return pulumi.get(self, "tags")


class AwaitableGetPrometheusResult(GetPrometheusResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPrometheusResult(
            enable_details=self.enable_details,
            id=self.id,
            ids=self.ids,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file,
            prometheis=self.prometheis,
            resource_group_id=self.resource_group_id,
            tags=self.tags)


def get_prometheus(enable_details: Optional[bool] = None,
                   ids: Optional[Sequence[str]] = None,
                   name_regex: Optional[str] = None,
                   output_file: Optional[str] = None,
                   resource_group_id: Optional[str] = None,
                   tags: Optional[Mapping[str, Any]] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPrometheusResult:
    """
    This data source provides the Arms Prometheus of the current Alibaba Cloud user.

    > **NOTE:** Available since v1.214.0.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    config = pulumi.Config()
    name = config.get("name")
    if name is None:
        name = "tf-example"
    default = alicloud.vpc.get_networks(name_regex="default-NODELETING")
    default_get_switches = alicloud.vpc.get_switches(vpc_id=default.ids[0])
    default_get_resource_groups = alicloud.resourcemanager.get_resource_groups()
    default_security_group = alicloud.ecs.SecurityGroup("default", vpc_id=default.ids[0])
    default_prometheus = alicloud.arms.Prometheus("default",
        cluster_type="ecs",
        grafana_instance_id="free",
        vpc_id=default.ids[0],
        vswitch_id=default_get_switches.ids[0],
        security_group_id=default_security_group.id,
        cluster_name=f"{name}-{default.ids[0]}",
        resource_group_id=default_get_resource_groups.groups[1].id,
        tags={
            "Created": "TF",
            "For": "Prometheus",
        })
    name_regex = alicloud.arms.get_prometheus_output(name_regex=default_prometheus.cluster_name)
    pulumi.export("armsPrometheusId", name_regex.prometheis[0].id)
    ```


    :param bool enable_details: Whether to query details about the instance.
    :param Sequence[str] ids: A list of Prometheus IDs.
    :param str name_regex: A regex string to filter results by Prometheus name.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str resource_group_id: The ID of the resource group.
    :param Mapping[str, Any] tags: A mapping of tags to assign to the resource.
    """
    __args__ = dict()
    __args__['enableDetails'] = enable_details
    __args__['ids'] = ids
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    __args__['resourceGroupId'] = resource_group_id
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:arms/getPrometheus:getPrometheus', __args__, opts=opts, typ=GetPrometheusResult).value

    return AwaitableGetPrometheusResult(
        enable_details=pulumi.get(__ret__, 'enable_details'),
        id=pulumi.get(__ret__, 'id'),
        ids=pulumi.get(__ret__, 'ids'),
        name_regex=pulumi.get(__ret__, 'name_regex'),
        names=pulumi.get(__ret__, 'names'),
        output_file=pulumi.get(__ret__, 'output_file'),
        prometheis=pulumi.get(__ret__, 'prometheis'),
        resource_group_id=pulumi.get(__ret__, 'resource_group_id'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_prometheus)
def get_prometheus_output(enable_details: Optional[pulumi.Input[Optional[bool]]] = None,
                          ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                          name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                          output_file: Optional[pulumi.Input[Optional[str]]] = None,
                          resource_group_id: Optional[pulumi.Input[Optional[str]]] = None,
                          tags: Optional[pulumi.Input[Optional[Mapping[str, Any]]]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetPrometheusResult]:
    """
    This data source provides the Arms Prometheus of the current Alibaba Cloud user.

    > **NOTE:** Available since v1.214.0.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    config = pulumi.Config()
    name = config.get("name")
    if name is None:
        name = "tf-example"
    default = alicloud.vpc.get_networks(name_regex="default-NODELETING")
    default_get_switches = alicloud.vpc.get_switches(vpc_id=default.ids[0])
    default_get_resource_groups = alicloud.resourcemanager.get_resource_groups()
    default_security_group = alicloud.ecs.SecurityGroup("default", vpc_id=default.ids[0])
    default_prometheus = alicloud.arms.Prometheus("default",
        cluster_type="ecs",
        grafana_instance_id="free",
        vpc_id=default.ids[0],
        vswitch_id=default_get_switches.ids[0],
        security_group_id=default_security_group.id,
        cluster_name=f"{name}-{default.ids[0]}",
        resource_group_id=default_get_resource_groups.groups[1].id,
        tags={
            "Created": "TF",
            "For": "Prometheus",
        })
    name_regex = alicloud.arms.get_prometheus_output(name_regex=default_prometheus.cluster_name)
    pulumi.export("armsPrometheusId", name_regex.prometheis[0].id)
    ```


    :param bool enable_details: Whether to query details about the instance.
    :param Sequence[str] ids: A list of Prometheus IDs.
    :param str name_regex: A regex string to filter results by Prometheus name.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str resource_group_id: The ID of the resource group.
    :param Mapping[str, Any] tags: A mapping of tags to assign to the resource.
    """
    ...
