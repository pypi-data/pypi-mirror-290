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
    'GetFunctionsResult',
    'AwaitableGetFunctionsResult',
    'get_functions',
    'get_functions_output',
]

@pulumi.output_type
class GetFunctionsResult:
    """
    A collection of values returned by getFunctions.
    """
    def __init__(__self__, functions=None, id=None, ids=None, name_regex=None, names=None, output_file=None, service_name=None):
        if functions and not isinstance(functions, list):
            raise TypeError("Expected argument 'functions' to be a list")
        pulumi.set(__self__, "functions", functions)
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
        if service_name and not isinstance(service_name, str):
            raise TypeError("Expected argument 'service_name' to be a str")
        pulumi.set(__self__, "service_name", service_name)

    @property
    @pulumi.getter
    def functions(self) -> Sequence['outputs.GetFunctionsFunctionResult']:
        """
        A list of functions. Each element contains the following attributes:
        """
        return pulumi.get(self, "functions")

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
        A list of functions ids.
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
        A list of functions names.
        """
        return pulumi.get(self, "names")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter(name="serviceName")
    def service_name(self) -> str:
        return pulumi.get(self, "service_name")


class AwaitableGetFunctionsResult(GetFunctionsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFunctionsResult(
            functions=self.functions,
            id=self.id,
            ids=self.ids,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file,
            service_name=self.service_name)


def get_functions(ids: Optional[Sequence[str]] = None,
                  name_regex: Optional[str] = None,
                  output_file: Optional[str] = None,
                  service_name: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFunctionsResult:
    """
    This data source provides the Function Compute functions of the current Alibaba Cloud user.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    functions_ds = alicloud.fc.get_functions(service_name="sample_service",
        name_regex="sample_fc_function")
    pulumi.export("firstFcFunctionName", functions_ds.functions[0].name)
    ```


    :param Sequence[str] ids: A list of functions ids.
    :param str name_regex: A regex string to filter results by function name.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str service_name: Name of the service that contains the functions to find.
    """
    __args__ = dict()
    __args__['ids'] = ids
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    __args__['serviceName'] = service_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:fc/getFunctions:getFunctions', __args__, opts=opts, typ=GetFunctionsResult).value

    return AwaitableGetFunctionsResult(
        functions=pulumi.get(__ret__, 'functions'),
        id=pulumi.get(__ret__, 'id'),
        ids=pulumi.get(__ret__, 'ids'),
        name_regex=pulumi.get(__ret__, 'name_regex'),
        names=pulumi.get(__ret__, 'names'),
        output_file=pulumi.get(__ret__, 'output_file'),
        service_name=pulumi.get(__ret__, 'service_name'))


@_utilities.lift_output_func(get_functions)
def get_functions_output(ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                         name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                         output_file: Optional[pulumi.Input[Optional[str]]] = None,
                         service_name: Optional[pulumi.Input[str]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetFunctionsResult]:
    """
    This data source provides the Function Compute functions of the current Alibaba Cloud user.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    functions_ds = alicloud.fc.get_functions(service_name="sample_service",
        name_regex="sample_fc_function")
    pulumi.export("firstFcFunctionName", functions_ds.functions[0].name)
    ```


    :param Sequence[str] ids: A list of functions ids.
    :param str name_regex: A regex string to filter results by function name.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str service_name: Name of the service that contains the functions to find.
    """
    ...
