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
    def __init__(__self__, domains=None, enable_details=None, id=None, ids=None, key_word=None, name_regex=None, names=None, output_file=None, status=None):
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
        if key_word and not isinstance(key_word, str):
            raise TypeError("Expected argument 'key_word' to be a str")
        pulumi.set(__self__, "key_word", key_word)
        if name_regex and not isinstance(name_regex, str):
            raise TypeError("Expected argument 'name_regex' to be a str")
        pulumi.set(__self__, "name_regex", name_regex)
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        pulumi.set(__self__, "names", names)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def domains(self) -> Sequence['outputs.GetDomainsDomainResult']:
        """
        A list of Domains. Each element contains the following attributes:
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
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter(name="keyWord")
    def key_word(self) -> Optional[str]:
        return pulumi.get(self, "key_word")

    @property
    @pulumi.getter(name="nameRegex")
    def name_regex(self) -> Optional[str]:
        return pulumi.get(self, "name_regex")

    @property
    @pulumi.getter
    def names(self) -> Sequence[str]:
        """
        A list of Domain names.
        """
        return pulumi.get(self, "names")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        The status of the domain name.
        """
        return pulumi.get(self, "status")


class AwaitableGetDomainsResult(GetDomainsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDomainsResult(
            domains=self.domains,
            enable_details=self.enable_details,
            id=self.id,
            ids=self.ids,
            key_word=self.key_word,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file,
            status=self.status)


def get_domains(enable_details: Optional[bool] = None,
                ids: Optional[Sequence[str]] = None,
                key_word: Optional[str] = None,
                name_regex: Optional[str] = None,
                output_file: Optional[str] = None,
                status: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDomainsResult:
    """
    This data source provides the Direct Mail Domains of the current Alibaba Cloud user.

    > **NOTE:** Available since v1.134.0.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    config = pulumi.Config()
    name = config.get("name")
    if name is None:
        name = "terraform-example.pop.com"
    default = alicloud.directmail.Domain("default", domain_name=name)
    ids = alicloud.directmail.get_domains_output(ids=[default.id])
    pulumi.export("directMailDomainsId0", ids.domains[0].id)
    ```


    :param bool enable_details: Whether to query the detailed list of resource attributes. Default value: `false`.
    :param Sequence[str] ids: A list of Domain IDs.
    :param str key_word: The domain name. It must be 1 to 50 characters in length and can contain digits, letters, periods (.), and hyphens (-).
    :param str name_regex: A regex string to filter results by Domain name.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str status: The status of the domain name. Valid values:
    """
    __args__ = dict()
    __args__['enableDetails'] = enable_details
    __args__['ids'] = ids
    __args__['keyWord'] = key_word
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    __args__['status'] = status
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:directmail/getDomains:getDomains', __args__, opts=opts, typ=GetDomainsResult).value

    return AwaitableGetDomainsResult(
        domains=pulumi.get(__ret__, 'domains'),
        enable_details=pulumi.get(__ret__, 'enable_details'),
        id=pulumi.get(__ret__, 'id'),
        ids=pulumi.get(__ret__, 'ids'),
        key_word=pulumi.get(__ret__, 'key_word'),
        name_regex=pulumi.get(__ret__, 'name_regex'),
        names=pulumi.get(__ret__, 'names'),
        output_file=pulumi.get(__ret__, 'output_file'),
        status=pulumi.get(__ret__, 'status'))


@_utilities.lift_output_func(get_domains)
def get_domains_output(enable_details: Optional[pulumi.Input[Optional[bool]]] = None,
                       ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                       key_word: Optional[pulumi.Input[Optional[str]]] = None,
                       name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                       output_file: Optional[pulumi.Input[Optional[str]]] = None,
                       status: Optional[pulumi.Input[Optional[str]]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDomainsResult]:
    """
    This data source provides the Direct Mail Domains of the current Alibaba Cloud user.

    > **NOTE:** Available since v1.134.0.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    config = pulumi.Config()
    name = config.get("name")
    if name is None:
        name = "terraform-example.pop.com"
    default = alicloud.directmail.Domain("default", domain_name=name)
    ids = alicloud.directmail.get_domains_output(ids=[default.id])
    pulumi.export("directMailDomainsId0", ids.domains[0].id)
    ```


    :param bool enable_details: Whether to query the detailed list of resource attributes. Default value: `false`.
    :param Sequence[str] ids: A list of Domain IDs.
    :param str key_word: The domain name. It must be 1 to 50 characters in length and can contain digits, letters, periods (.), and hyphens (-).
    :param str name_regex: A regex string to filter results by Domain name.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str status: The status of the domain name. Valid values:
    """
    ...
