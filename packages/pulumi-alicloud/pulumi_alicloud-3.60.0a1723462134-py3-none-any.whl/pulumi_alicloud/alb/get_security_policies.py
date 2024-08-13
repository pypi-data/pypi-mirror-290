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
    'GetSecurityPoliciesResult',
    'AwaitableGetSecurityPoliciesResult',
    'get_security_policies',
    'get_security_policies_output',
]

@pulumi.output_type
class GetSecurityPoliciesResult:
    """
    A collection of values returned by getSecurityPolicies.
    """
    def __init__(__self__, id=None, ids=None, name_regex=None, names=None, output_file=None, policies=None, resource_group_id=None, security_policy_ids=None, security_policy_name=None, status=None, tags=None):
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
        if policies and not isinstance(policies, list):
            raise TypeError("Expected argument 'policies' to be a list")
        pulumi.set(__self__, "policies", policies)
        if resource_group_id and not isinstance(resource_group_id, str):
            raise TypeError("Expected argument 'resource_group_id' to be a str")
        pulumi.set(__self__, "resource_group_id", resource_group_id)
        if security_policy_ids and not isinstance(security_policy_ids, list):
            raise TypeError("Expected argument 'security_policy_ids' to be a list")
        pulumi.set(__self__, "security_policy_ids", security_policy_ids)
        if security_policy_name and not isinstance(security_policy_name, str):
            raise TypeError("Expected argument 'security_policy_name' to be a str")
        pulumi.set(__self__, "security_policy_name", security_policy_name)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

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
    def policies(self) -> Sequence['outputs.GetSecurityPoliciesPolicyResult']:
        return pulumi.get(self, "policies")

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> Optional[str]:
        return pulumi.get(self, "resource_group_id")

    @property
    @pulumi.getter(name="securityPolicyIds")
    def security_policy_ids(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "security_policy_ids")

    @property
    @pulumi.getter(name="securityPolicyName")
    def security_policy_name(self) -> Optional[str]:
        return pulumi.get(self, "security_policy_name")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, Any]]:
        return pulumi.get(self, "tags")


class AwaitableGetSecurityPoliciesResult(GetSecurityPoliciesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSecurityPoliciesResult(
            id=self.id,
            ids=self.ids,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file,
            policies=self.policies,
            resource_group_id=self.resource_group_id,
            security_policy_ids=self.security_policy_ids,
            security_policy_name=self.security_policy_name,
            status=self.status,
            tags=self.tags)


def get_security_policies(ids: Optional[Sequence[str]] = None,
                          name_regex: Optional[str] = None,
                          output_file: Optional[str] = None,
                          resource_group_id: Optional[str] = None,
                          security_policy_ids: Optional[Sequence[str]] = None,
                          security_policy_name: Optional[str] = None,
                          status: Optional[str] = None,
                          tags: Optional[Mapping[str, Any]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSecurityPoliciesResult:
    """
    This data source provides the Alb Security Policies of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.130.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    ids = alicloud.alb.get_security_policies()
    pulumi.export("albSecurityPolicyId1", ids.policies[0].id)
    name_regex = alicloud.alb.get_security_policies(name_regex="^my-SecurityPolicy")
    pulumi.export("albSecurityPolicyId2", name_regex.policies[0].id)
    ```


    :param Sequence[str] ids: A list of Security Policy IDs.
    :param str name_regex: A regex string to filter results by Security Policy name.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str resource_group_id: The ID of the resource group.
    :param Sequence[str] security_policy_ids: The security policy ids.
    :param str security_policy_name: The name of the resource.
    :param str status: The status of the resource. Valid values : `Available`, `Configuring`.
    """
    __args__ = dict()
    __args__['ids'] = ids
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    __args__['resourceGroupId'] = resource_group_id
    __args__['securityPolicyIds'] = security_policy_ids
    __args__['securityPolicyName'] = security_policy_name
    __args__['status'] = status
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:alb/getSecurityPolicies:getSecurityPolicies', __args__, opts=opts, typ=GetSecurityPoliciesResult).value

    return AwaitableGetSecurityPoliciesResult(
        id=pulumi.get(__ret__, 'id'),
        ids=pulumi.get(__ret__, 'ids'),
        name_regex=pulumi.get(__ret__, 'name_regex'),
        names=pulumi.get(__ret__, 'names'),
        output_file=pulumi.get(__ret__, 'output_file'),
        policies=pulumi.get(__ret__, 'policies'),
        resource_group_id=pulumi.get(__ret__, 'resource_group_id'),
        security_policy_ids=pulumi.get(__ret__, 'security_policy_ids'),
        security_policy_name=pulumi.get(__ret__, 'security_policy_name'),
        status=pulumi.get(__ret__, 'status'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_security_policies)
def get_security_policies_output(ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                                 name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                                 output_file: Optional[pulumi.Input[Optional[str]]] = None,
                                 resource_group_id: Optional[pulumi.Input[Optional[str]]] = None,
                                 security_policy_ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                                 security_policy_name: Optional[pulumi.Input[Optional[str]]] = None,
                                 status: Optional[pulumi.Input[Optional[str]]] = None,
                                 tags: Optional[pulumi.Input[Optional[Mapping[str, Any]]]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSecurityPoliciesResult]:
    """
    This data source provides the Alb Security Policies of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.130.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    ids = alicloud.alb.get_security_policies()
    pulumi.export("albSecurityPolicyId1", ids.policies[0].id)
    name_regex = alicloud.alb.get_security_policies(name_regex="^my-SecurityPolicy")
    pulumi.export("albSecurityPolicyId2", name_regex.policies[0].id)
    ```


    :param Sequence[str] ids: A list of Security Policy IDs.
    :param str name_regex: A regex string to filter results by Security Policy name.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str resource_group_id: The ID of the resource group.
    :param Sequence[str] security_policy_ids: The security policy ids.
    :param str security_policy_name: The name of the resource.
    :param str status: The status of the resource. Valid values : `Available`, `Configuring`.
    """
    ...
