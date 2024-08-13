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
    'GetDomainsResult',
    'AwaitableGetDomainsResult',
    'get_domains',
    'get_domains_output',
]

@pulumi.output_type
class GetDomainsResult:
    """
    A collection of values returned by getDomains.
    """
    def __init__(__self__, change_end_time=None, change_start_time=None, check_domain_show=None, domain_search_type=None, domains=None, enable_details=None, id=None, ids=None, name_regex=None, names=None, output_file=None, resource_group_id=None, security_token=None, status=None):
        if change_end_time and not isinstance(change_end_time, str):
            raise TypeError("Expected argument 'change_end_time' to be a str")
        pulumi.set(__self__, "change_end_time", change_end_time)
        if change_start_time and not isinstance(change_start_time, str):
            raise TypeError("Expected argument 'change_start_time' to be a str")
        pulumi.set(__self__, "change_start_time", change_start_time)
        if check_domain_show and not isinstance(check_domain_show, bool):
            raise TypeError("Expected argument 'check_domain_show' to be a bool")
        pulumi.set(__self__, "check_domain_show", check_domain_show)
        if domain_search_type and not isinstance(domain_search_type, str):
            raise TypeError("Expected argument 'domain_search_type' to be a str")
        pulumi.set(__self__, "domain_search_type", domain_search_type)
        if domains and not isinstance(domains, list):
            raise TypeError("Expected argument 'domains' to be a list")
        pulumi.set(__self__, "domains", domains)
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
        if resource_group_id and not isinstance(resource_group_id, str):
            raise TypeError("Expected argument 'resource_group_id' to be a str")
        pulumi.set(__self__, "resource_group_id", resource_group_id)
        if security_token and not isinstance(security_token, str):
            raise TypeError("Expected argument 'security_token' to be a str")
        pulumi.set(__self__, "security_token", security_token)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="changeEndTime")
    def change_end_time(self) -> Optional[str]:
        return pulumi.get(self, "change_end_time")

    @property
    @pulumi.getter(name="changeStartTime")
    def change_start_time(self) -> Optional[str]:
        return pulumi.get(self, "change_start_time")

    @property
    @pulumi.getter(name="checkDomainShow")
    def check_domain_show(self) -> Optional[bool]:
        return pulumi.get(self, "check_domain_show")

    @property
    @pulumi.getter(name="domainSearchType")
    def domain_search_type(self) -> Optional[str]:
        return pulumi.get(self, "domain_search_type")

    @property
    @pulumi.getter
    def domains(self) -> Sequence['outputs.GetDomainsDomainResult']:
        """
        A list of domains. Each element contains the following attributes:
        """
        return pulumi.get(self, "domains")

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
        A list ids of DCDN Domain.
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
        A list of DCDN Domain names.
        """
        return pulumi.get(self, "names")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> Optional[str]:
        """
        The ID of the resource group.
        """
        return pulumi.get(self, "resource_group_id")

    @property
    @pulumi.getter(name="securityToken")
    def security_token(self) -> Optional[str]:
        return pulumi.get(self, "security_token")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        The status of DCDN Domain. Valid values: `online`, `offline`, `check_failed`, `checking`, `configure_failed`, `configuring`.
        """
        return pulumi.get(self, "status")


class AwaitableGetDomainsResult(GetDomainsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDomainsResult(
            change_end_time=self.change_end_time,
            change_start_time=self.change_start_time,
            check_domain_show=self.check_domain_show,
            domain_search_type=self.domain_search_type,
            domains=self.domains,
            enable_details=self.enable_details,
            id=self.id,
            ids=self.ids,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file,
            resource_group_id=self.resource_group_id,
            security_token=self.security_token,
            status=self.status)


def get_domains(change_end_time: Optional[str] = None,
                change_start_time: Optional[str] = None,
                check_domain_show: Optional[bool] = None,
                domain_search_type: Optional[str] = None,
                enable_details: Optional[bool] = None,
                ids: Optional[Sequence[str]] = None,
                name_regex: Optional[str] = None,
                output_file: Optional[str] = None,
                resource_group_id: Optional[str] = None,
                security_token: Optional[str] = None,
                status: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDomainsResult:
    """
    Provides a collection of DCDN Domains to the specified filters.

    > **NOTE:** Available in 1.94.0+.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    example = alicloud.dcdn.get_domains(ids=["example.com"])
    pulumi.export("domainId", example.domains[0].id)
    ```


    :param str change_end_time: The end time of the update. Specify the time in the ISO 8601 standard in the `yyyy-MM-ddTHH:mm:ssZ` format. The time must be in UTC.
    :param str change_start_time: The start time of the update. Specify the time in the ISO 8601 standard in the `yyyy-MM-ddTHH:mm:ssZ` format. The time must be in UTC.
    :param bool check_domain_show: Specifies whether to display the domains in the checking, check_failed, or configure_failed status. Valid values: `true` or `false`.
    :param str domain_search_type: The search method. Default value: `fuzzy_match`. Valid values: `fuzzy_match`, `pre_match`, `suf_match`, `full_match`.
    :param bool enable_details: Default to `false`. Set it to true can output more details.
    :param Sequence[str] ids: A list ids of DCDN Domain.
    :param str name_regex: A regex string to filter results by the DCDN Domain.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str resource_group_id: The ID of the resource group.
    :param str status: The status of DCDN Domain.
    """
    __args__ = dict()
    __args__['changeEndTime'] = change_end_time
    __args__['changeStartTime'] = change_start_time
    __args__['checkDomainShow'] = check_domain_show
    __args__['domainSearchType'] = domain_search_type
    __args__['enableDetails'] = enable_details
    __args__['ids'] = ids
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    __args__['resourceGroupId'] = resource_group_id
    __args__['securityToken'] = security_token
    __args__['status'] = status
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:dcdn/getDomains:getDomains', __args__, opts=opts, typ=GetDomainsResult).value

    return AwaitableGetDomainsResult(
        change_end_time=pulumi.get(__ret__, 'change_end_time'),
        change_start_time=pulumi.get(__ret__, 'change_start_time'),
        check_domain_show=pulumi.get(__ret__, 'check_domain_show'),
        domain_search_type=pulumi.get(__ret__, 'domain_search_type'),
        domains=pulumi.get(__ret__, 'domains'),
        enable_details=pulumi.get(__ret__, 'enable_details'),
        id=pulumi.get(__ret__, 'id'),
        ids=pulumi.get(__ret__, 'ids'),
        name_regex=pulumi.get(__ret__, 'name_regex'),
        names=pulumi.get(__ret__, 'names'),
        output_file=pulumi.get(__ret__, 'output_file'),
        resource_group_id=pulumi.get(__ret__, 'resource_group_id'),
        security_token=pulumi.get(__ret__, 'security_token'),
        status=pulumi.get(__ret__, 'status'))


@_utilities.lift_output_func(get_domains)
def get_domains_output(change_end_time: Optional[pulumi.Input[Optional[str]]] = None,
                       change_start_time: Optional[pulumi.Input[Optional[str]]] = None,
                       check_domain_show: Optional[pulumi.Input[Optional[bool]]] = None,
                       domain_search_type: Optional[pulumi.Input[Optional[str]]] = None,
                       enable_details: Optional[pulumi.Input[Optional[bool]]] = None,
                       ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                       name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                       output_file: Optional[pulumi.Input[Optional[str]]] = None,
                       resource_group_id: Optional[pulumi.Input[Optional[str]]] = None,
                       security_token: Optional[pulumi.Input[Optional[str]]] = None,
                       status: Optional[pulumi.Input[Optional[str]]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDomainsResult]:
    """
    Provides a collection of DCDN Domains to the specified filters.

    > **NOTE:** Available in 1.94.0+.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    example = alicloud.dcdn.get_domains(ids=["example.com"])
    pulumi.export("domainId", example.domains[0].id)
    ```


    :param str change_end_time: The end time of the update. Specify the time in the ISO 8601 standard in the `yyyy-MM-ddTHH:mm:ssZ` format. The time must be in UTC.
    :param str change_start_time: The start time of the update. Specify the time in the ISO 8601 standard in the `yyyy-MM-ddTHH:mm:ssZ` format. The time must be in UTC.
    :param bool check_domain_show: Specifies whether to display the domains in the checking, check_failed, or configure_failed status. Valid values: `true` or `false`.
    :param str domain_search_type: The search method. Default value: `fuzzy_match`. Valid values: `fuzzy_match`, `pre_match`, `suf_match`, `full_match`.
    :param bool enable_details: Default to `false`. Set it to true can output more details.
    :param Sequence[str] ids: A list ids of DCDN Domain.
    :param str name_regex: A regex string to filter results by the DCDN Domain.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str resource_group_id: The ID of the resource group.
    :param str status: The status of DCDN Domain.
    """
    ...
