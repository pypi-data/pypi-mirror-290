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
    'GetVersionsResult',
    'AwaitableGetVersionsResult',
    'get_versions',
    'get_versions_output',
]

@pulumi.output_type
class GetVersionsResult:
    """
    A collection of values returned by getVersions.
    """
    def __init__(__self__, edition=None, id=None, ids=None, output_file=None, versions=None):
        if edition and not isinstance(edition, str):
            raise TypeError("Expected argument 'edition' to be a str")
        pulumi.set(__self__, "edition", edition)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if versions and not isinstance(versions, list):
            raise TypeError("Expected argument 'versions' to be a list")
        pulumi.set(__self__, "versions", versions)

    @property
    @pulumi.getter
    def edition(self) -> Optional[str]:
        return pulumi.get(self, "edition")

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
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter
    def versions(self) -> Sequence['outputs.GetVersionsVersionResult']:
        return pulumi.get(self, "versions")


class AwaitableGetVersionsResult(GetVersionsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVersionsResult(
            edition=self.edition,
            id=self.id,
            ids=self.ids,
            output_file=self.output_file,
            versions=self.versions)


def get_versions(edition: Optional[str] = None,
                 ids: Optional[Sequence[str]] = None,
                 output_file: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVersionsResult:
    """
    This data source provides ASM available versions in the specified region.

    > **NOTE:** Available in v1.161.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    default = alicloud.servicemesh.get_versions(edition="Default")
    pulumi.export("serviceMeshVersion", versions[0]["version"])
    ```


    :param str edition: The edition of the ASM instance. Valid values:
           - Default: Standard Edition
           - Pro: Professional Edition
    :param Sequence[str] ids: A list of ASM versions. Its element formats as `<edition>:<version>`.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    """
    __args__ = dict()
    __args__['edition'] = edition
    __args__['ids'] = ids
    __args__['outputFile'] = output_file
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:servicemesh/getVersions:getVersions', __args__, opts=opts, typ=GetVersionsResult).value

    return AwaitableGetVersionsResult(
        edition=pulumi.get(__ret__, 'edition'),
        id=pulumi.get(__ret__, 'id'),
        ids=pulumi.get(__ret__, 'ids'),
        output_file=pulumi.get(__ret__, 'output_file'),
        versions=pulumi.get(__ret__, 'versions'))


@_utilities.lift_output_func(get_versions)
def get_versions_output(edition: Optional[pulumi.Input[Optional[str]]] = None,
                        ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                        output_file: Optional[pulumi.Input[Optional[str]]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVersionsResult]:
    """
    This data source provides ASM available versions in the specified region.

    > **NOTE:** Available in v1.161.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    default = alicloud.servicemesh.get_versions(edition="Default")
    pulumi.export("serviceMeshVersion", versions[0]["version"])
    ```


    :param str edition: The edition of the ASM instance. Valid values:
           - Default: Standard Edition
           - Pro: Professional Edition
    :param Sequence[str] ids: A list of ASM versions. Its element formats as `<edition>:<version>`.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    """
    ...
