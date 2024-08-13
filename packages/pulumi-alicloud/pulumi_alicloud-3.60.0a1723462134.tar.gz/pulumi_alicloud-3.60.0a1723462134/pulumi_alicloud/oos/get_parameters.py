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
    'GetParametersResult',
    'AwaitableGetParametersResult',
    'get_parameters',
    'get_parameters_output',
]

@pulumi.output_type
class GetParametersResult:
    """
    A collection of values returned by getParameters.
    """
    def __init__(__self__, enable_details=None, id=None, ids=None, name_regex=None, names=None, output_file=None, parameter_name=None, parameters=None, resource_group_id=None, sort_field=None, sort_order=None, tags=None, type=None):
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
        if parameter_name and not isinstance(parameter_name, str):
            raise TypeError("Expected argument 'parameter_name' to be a str")
        pulumi.set(__self__, "parameter_name", parameter_name)
        if parameters and not isinstance(parameters, list):
            raise TypeError("Expected argument 'parameters' to be a list")
        pulumi.set(__self__, "parameters", parameters)
        if resource_group_id and not isinstance(resource_group_id, str):
            raise TypeError("Expected argument 'resource_group_id' to be a str")
        pulumi.set(__self__, "resource_group_id", resource_group_id)
        if sort_field and not isinstance(sort_field, str):
            raise TypeError("Expected argument 'sort_field' to be a str")
        pulumi.set(__self__, "sort_field", sort_field)
        if sort_order and not isinstance(sort_order, str):
            raise TypeError("Expected argument 'sort_order' to be a str")
        pulumi.set(__self__, "sort_order", sort_order)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

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
        return pulumi.get(self, "names")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter(name="parameterName")
    def parameter_name(self) -> Optional[str]:
        return pulumi.get(self, "parameter_name")

    @property
    @pulumi.getter
    def parameters(self) -> Sequence['outputs.GetParametersParameterResult']:
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> Optional[str]:
        return pulumi.get(self, "resource_group_id")

    @property
    @pulumi.getter(name="sortField")
    def sort_field(self) -> Optional[str]:
        return pulumi.get(self, "sort_field")

    @property
    @pulumi.getter(name="sortOrder")
    def sort_order(self) -> Optional[str]:
        return pulumi.get(self, "sort_order")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, Any]]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        return pulumi.get(self, "type")


class AwaitableGetParametersResult(GetParametersResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetParametersResult(
            enable_details=self.enable_details,
            id=self.id,
            ids=self.ids,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file,
            parameter_name=self.parameter_name,
            parameters=self.parameters,
            resource_group_id=self.resource_group_id,
            sort_field=self.sort_field,
            sort_order=self.sort_order,
            tags=self.tags,
            type=self.type)


def get_parameters(enable_details: Optional[bool] = None,
                   ids: Optional[Sequence[str]] = None,
                   name_regex: Optional[str] = None,
                   output_file: Optional[str] = None,
                   parameter_name: Optional[str] = None,
                   resource_group_id: Optional[str] = None,
                   sort_field: Optional[str] = None,
                   sort_order: Optional[str] = None,
                   tags: Optional[Mapping[str, Any]] = None,
                   type: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetParametersResult:
    """
    This data source provides the Oos Parameters of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.147.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    ids = alicloud.oos.get_parameters(ids=["my-Parameter"])
    pulumi.export("oosParameterId1", ids.parameters[0].id)
    name_regex = alicloud.oos.get_parameters(name_regex="^my-Parameter")
    pulumi.export("oosParameterId2", name_regex.parameters[0].id)
    resource_group_id = alicloud.oos.get_parameters(ids=["my-Parameter"],
        resource_group_id="example_value")
    pulumi.export("oosParameterId3", resource_group_id.parameters[0].id)
    tags = alicloud.oos.get_parameters(ids=["my-Parameter"],
        tags={
            "Created": "TF",
            "For": "OosParameter",
        })
    pulumi.export("oosParameterId4", tags.parameters[0].id)
    ```


    :param bool enable_details: Default to `false`. Set it to `true` can output more details about resource attributes.
    :param Sequence[str] ids: A list of Parameter IDs. Its element value is same as Parameter Name.
    :param str name_regex: A regex string to filter results by Parameter name.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str parameter_name: The name of the common parameter. You can enter a keyword to query parameter names in fuzzy match mode.
    :param str resource_group_id: The ID of the Resource Group.
    :param Mapping[str, Any] tags: A mapping of tags to assign to the resource.
    :param str type: The data type of the common parameter. Valid values: `String` and `StringList`.
    """
    __args__ = dict()
    __args__['enableDetails'] = enable_details
    __args__['ids'] = ids
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    __args__['parameterName'] = parameter_name
    __args__['resourceGroupId'] = resource_group_id
    __args__['sortField'] = sort_field
    __args__['sortOrder'] = sort_order
    __args__['tags'] = tags
    __args__['type'] = type
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:oos/getParameters:getParameters', __args__, opts=opts, typ=GetParametersResult).value

    return AwaitableGetParametersResult(
        enable_details=pulumi.get(__ret__, 'enable_details'),
        id=pulumi.get(__ret__, 'id'),
        ids=pulumi.get(__ret__, 'ids'),
        name_regex=pulumi.get(__ret__, 'name_regex'),
        names=pulumi.get(__ret__, 'names'),
        output_file=pulumi.get(__ret__, 'output_file'),
        parameter_name=pulumi.get(__ret__, 'parameter_name'),
        parameters=pulumi.get(__ret__, 'parameters'),
        resource_group_id=pulumi.get(__ret__, 'resource_group_id'),
        sort_field=pulumi.get(__ret__, 'sort_field'),
        sort_order=pulumi.get(__ret__, 'sort_order'),
        tags=pulumi.get(__ret__, 'tags'),
        type=pulumi.get(__ret__, 'type'))


@_utilities.lift_output_func(get_parameters)
def get_parameters_output(enable_details: Optional[pulumi.Input[Optional[bool]]] = None,
                          ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                          name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                          output_file: Optional[pulumi.Input[Optional[str]]] = None,
                          parameter_name: Optional[pulumi.Input[Optional[str]]] = None,
                          resource_group_id: Optional[pulumi.Input[Optional[str]]] = None,
                          sort_field: Optional[pulumi.Input[Optional[str]]] = None,
                          sort_order: Optional[pulumi.Input[Optional[str]]] = None,
                          tags: Optional[pulumi.Input[Optional[Mapping[str, Any]]]] = None,
                          type: Optional[pulumi.Input[Optional[str]]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetParametersResult]:
    """
    This data source provides the Oos Parameters of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.147.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    ids = alicloud.oos.get_parameters(ids=["my-Parameter"])
    pulumi.export("oosParameterId1", ids.parameters[0].id)
    name_regex = alicloud.oos.get_parameters(name_regex="^my-Parameter")
    pulumi.export("oosParameterId2", name_regex.parameters[0].id)
    resource_group_id = alicloud.oos.get_parameters(ids=["my-Parameter"],
        resource_group_id="example_value")
    pulumi.export("oosParameterId3", resource_group_id.parameters[0].id)
    tags = alicloud.oos.get_parameters(ids=["my-Parameter"],
        tags={
            "Created": "TF",
            "For": "OosParameter",
        })
    pulumi.export("oosParameterId4", tags.parameters[0].id)
    ```


    :param bool enable_details: Default to `false`. Set it to `true` can output more details about resource attributes.
    :param Sequence[str] ids: A list of Parameter IDs. Its element value is same as Parameter Name.
    :param str name_regex: A regex string to filter results by Parameter name.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str parameter_name: The name of the common parameter. You can enter a keyword to query parameter names in fuzzy match mode.
    :param str resource_group_id: The ID of the Resource Group.
    :param Mapping[str, Any] tags: A mapping of tags to assign to the resource.
    :param str type: The data type of the common parameter. Valid values: `String` and `StringList`.
    """
    ...
