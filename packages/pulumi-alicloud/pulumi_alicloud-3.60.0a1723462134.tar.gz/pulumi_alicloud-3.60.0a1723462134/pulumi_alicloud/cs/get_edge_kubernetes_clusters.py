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
    'GetEdgeKubernetesClustersResult',
    'AwaitableGetEdgeKubernetesClustersResult',
    'get_edge_kubernetes_clusters',
    'get_edge_kubernetes_clusters_output',
]

@pulumi.output_type
class GetEdgeKubernetesClustersResult:
    """
    A collection of values returned by getEdgeKubernetesClusters.
    """
    def __init__(__self__, clusters=None, enable_details=None, id=None, ids=None, name_regex=None, names=None, output_file=None):
        if clusters and not isinstance(clusters, list):
            raise TypeError("Expected argument 'clusters' to be a list")
        pulumi.set(__self__, "clusters", clusters)
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

    @property
    @pulumi.getter
    def clusters(self) -> Sequence['outputs.GetEdgeKubernetesClustersClusterResult']:
        """
        A list of matched Kubernetes clusters. Each element contains the following attributes:
        """
        return pulumi.get(self, "clusters")

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
        """
        A list of matched Kubernetes clusters' ids.
        """
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter(name="nameRegex")
    def name_regex(self) -> Optional[str]:
        return pulumi.get(self, "name_regex")

    @property
    @pulumi.getter
    def names(self) -> Sequence[str]:
        """
        A list of matched Kubernetes clusters' names.
        """
        return pulumi.get(self, "names")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")


class AwaitableGetEdgeKubernetesClustersResult(GetEdgeKubernetesClustersResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEdgeKubernetesClustersResult(
            clusters=self.clusters,
            enable_details=self.enable_details,
            id=self.id,
            ids=self.ids,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file)


def get_edge_kubernetes_clusters(enable_details: Optional[bool] = None,
                                 ids: Optional[Sequence[str]] = None,
                                 name_regex: Optional[str] = None,
                                 output_file: Optional[str] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEdgeKubernetesClustersResult:
    """
    This data source provides a list Container Service Edge Kubernetes Clusters on Alibaba Cloud.

    > **NOTE:** Available in v1.103.0+

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    # Declare the data source
    k8s_clusters = alicloud.cs.get_edge_kubernetes_clusters(name_regex="my-first-k8s",
        output_file="my-first-k8s-json")
    pulumi.export("output", k8s_clusters.clusters)
    ```


    :param Sequence[str] ids: Cluster IDs to filter.
    :param str name_regex: A regex string to filter results by cluster name.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    """
    __args__ = dict()
    __args__['enableDetails'] = enable_details
    __args__['ids'] = ids
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:cs/getEdgeKubernetesClusters:getEdgeKubernetesClusters', __args__, opts=opts, typ=GetEdgeKubernetesClustersResult).value

    return AwaitableGetEdgeKubernetesClustersResult(
        clusters=pulumi.get(__ret__, 'clusters'),
        enable_details=pulumi.get(__ret__, 'enable_details'),
        id=pulumi.get(__ret__, 'id'),
        ids=pulumi.get(__ret__, 'ids'),
        name_regex=pulumi.get(__ret__, 'name_regex'),
        names=pulumi.get(__ret__, 'names'),
        output_file=pulumi.get(__ret__, 'output_file'))


@_utilities.lift_output_func(get_edge_kubernetes_clusters)
def get_edge_kubernetes_clusters_output(enable_details: Optional[pulumi.Input[Optional[bool]]] = None,
                                        ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                                        name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                                        output_file: Optional[pulumi.Input[Optional[str]]] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetEdgeKubernetesClustersResult]:
    """
    This data source provides a list Container Service Edge Kubernetes Clusters on Alibaba Cloud.

    > **NOTE:** Available in v1.103.0+

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    # Declare the data source
    k8s_clusters = alicloud.cs.get_edge_kubernetes_clusters(name_regex="my-first-k8s",
        output_file="my-first-k8s-json")
    pulumi.export("output", k8s_clusters.clusters)
    ```


    :param Sequence[str] ids: Cluster IDs to filter.
    :param str name_regex: A regex string to filter results by cluster name.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    """
    ...
