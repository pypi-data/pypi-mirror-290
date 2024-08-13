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
    'GetRecordsResult',
    'AwaitableGetRecordsResult',
    'get_records',
    'get_records_output',
]

@pulumi.output_type
class GetRecordsResult:
    """
    A collection of values returned by getRecords.
    """
    def __init__(__self__, domain_name=None, host_record_regex=None, id=None, ids=None, is_locked=None, line=None, output_file=None, records=None, status=None, type=None, urls=None, value_regex=None):
        if domain_name and not isinstance(domain_name, str):
            raise TypeError("Expected argument 'domain_name' to be a str")
        pulumi.set(__self__, "domain_name", domain_name)
        if host_record_regex and not isinstance(host_record_regex, str):
            raise TypeError("Expected argument 'host_record_regex' to be a str")
        pulumi.set(__self__, "host_record_regex", host_record_regex)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if is_locked and not isinstance(is_locked, bool):
            raise TypeError("Expected argument 'is_locked' to be a bool")
        pulumi.set(__self__, "is_locked", is_locked)
        if line and not isinstance(line, str):
            raise TypeError("Expected argument 'line' to be a str")
        pulumi.set(__self__, "line", line)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if records and not isinstance(records, list):
            raise TypeError("Expected argument 'records' to be a list")
        pulumi.set(__self__, "records", records)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if urls and not isinstance(urls, list):
            raise TypeError("Expected argument 'urls' to be a list")
        pulumi.set(__self__, "urls", urls)
        if value_regex and not isinstance(value_regex, str):
            raise TypeError("Expected argument 'value_regex' to be a str")
        pulumi.set(__self__, "value_regex", value_regex)

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> str:
        """
        Name of the domain the record belongs to.
        """
        return pulumi.get(self, "domain_name")

    @property
    @pulumi.getter(name="hostRecordRegex")
    def host_record_regex(self) -> Optional[str]:
        return pulumi.get(self, "host_record_regex")

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
        A list of record IDs.
        """
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter(name="isLocked")
    def is_locked(self) -> Optional[bool]:
        return pulumi.get(self, "is_locked")

    @property
    @pulumi.getter
    def line(self) -> Optional[str]:
        """
        ISP line of the record.
        """
        return pulumi.get(self, "line")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter
    def records(self) -> Sequence['outputs.GetRecordsRecordResult']:
        """
        A list of records. Each element contains the following attributes:
        """
        return pulumi.get(self, "records")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        Status of the record.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        Type of the record.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def urls(self) -> Sequence[str]:
        """
        A list of entire URLs. Each item format as `<host_record>.<domain_name>`.
        """
        return pulumi.get(self, "urls")

    @property
    @pulumi.getter(name="valueRegex")
    def value_regex(self) -> Optional[str]:
        return pulumi.get(self, "value_regex")


class AwaitableGetRecordsResult(GetRecordsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRecordsResult(
            domain_name=self.domain_name,
            host_record_regex=self.host_record_regex,
            id=self.id,
            ids=self.ids,
            is_locked=self.is_locked,
            line=self.line,
            output_file=self.output_file,
            records=self.records,
            status=self.status,
            type=self.type,
            urls=self.urls,
            value_regex=self.value_regex)


def get_records(domain_name: Optional[str] = None,
                host_record_regex: Optional[str] = None,
                ids: Optional[Sequence[str]] = None,
                is_locked: Optional[bool] = None,
                line: Optional[str] = None,
                output_file: Optional[str] = None,
                status: Optional[str] = None,
                type: Optional[str] = None,
                value_regex: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRecordsResult:
    """
    This data source provides a list of DNS Domain Records in an Alibaba Cloud account according to the specified filters.

    > **NOTE:** Available since v1.0.0.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    records_ds = alicloud.dns.get_records(domain_name="xiaozhu.top",
        is_locked=False,
        type="A",
        host_record_regex="^@",
        output_file="records.txt")
    pulumi.export("firstRecordId", records_ds.records[0].record_id)
    ```


    :param str domain_name: The domain name associated to the records.
    :param str host_record_regex: Host record regex.
    :param Sequence[str] ids: A list of record IDs.
    :param bool is_locked: Whether the record is locked or not.
    :param str line: ISP line. Valid items are `default`, `telecom`, `unicom`, `mobile`, `oversea`, `edu`, `drpeng`, `btvn`, .etc. For checking all resolution lines enumeration please visit [Alibaba Cloud DNS doc](https://www.alibabacloud.com/help/en/doc-detail/29807.htm)
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str status: Record status. Valid items are `ENABLE` and `DISABLE`.
    :param str type: Record type. Valid items are `A`, `NS`, `MX`, `TXT`, `CNAME`, `SRV`, `AAAA`, `REDIRECT_URL`, `FORWORD_URL` .
    :param str value_regex: Host record value regex.
    """
    __args__ = dict()
    __args__['domainName'] = domain_name
    __args__['hostRecordRegex'] = host_record_regex
    __args__['ids'] = ids
    __args__['isLocked'] = is_locked
    __args__['line'] = line
    __args__['outputFile'] = output_file
    __args__['status'] = status
    __args__['type'] = type
    __args__['valueRegex'] = value_regex
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:dns/getRecords:getRecords', __args__, opts=opts, typ=GetRecordsResult).value

    return AwaitableGetRecordsResult(
        domain_name=pulumi.get(__ret__, 'domain_name'),
        host_record_regex=pulumi.get(__ret__, 'host_record_regex'),
        id=pulumi.get(__ret__, 'id'),
        ids=pulumi.get(__ret__, 'ids'),
        is_locked=pulumi.get(__ret__, 'is_locked'),
        line=pulumi.get(__ret__, 'line'),
        output_file=pulumi.get(__ret__, 'output_file'),
        records=pulumi.get(__ret__, 'records'),
        status=pulumi.get(__ret__, 'status'),
        type=pulumi.get(__ret__, 'type'),
        urls=pulumi.get(__ret__, 'urls'),
        value_regex=pulumi.get(__ret__, 'value_regex'))


@_utilities.lift_output_func(get_records)
def get_records_output(domain_name: Optional[pulumi.Input[str]] = None,
                       host_record_regex: Optional[pulumi.Input[Optional[str]]] = None,
                       ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                       is_locked: Optional[pulumi.Input[Optional[bool]]] = None,
                       line: Optional[pulumi.Input[Optional[str]]] = None,
                       output_file: Optional[pulumi.Input[Optional[str]]] = None,
                       status: Optional[pulumi.Input[Optional[str]]] = None,
                       type: Optional[pulumi.Input[Optional[str]]] = None,
                       value_regex: Optional[pulumi.Input[Optional[str]]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRecordsResult]:
    """
    This data source provides a list of DNS Domain Records in an Alibaba Cloud account according to the specified filters.

    > **NOTE:** Available since v1.0.0.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    records_ds = alicloud.dns.get_records(domain_name="xiaozhu.top",
        is_locked=False,
        type="A",
        host_record_regex="^@",
        output_file="records.txt")
    pulumi.export("firstRecordId", records_ds.records[0].record_id)
    ```


    :param str domain_name: The domain name associated to the records.
    :param str host_record_regex: Host record regex.
    :param Sequence[str] ids: A list of record IDs.
    :param bool is_locked: Whether the record is locked or not.
    :param str line: ISP line. Valid items are `default`, `telecom`, `unicom`, `mobile`, `oversea`, `edu`, `drpeng`, `btvn`, .etc. For checking all resolution lines enumeration please visit [Alibaba Cloud DNS doc](https://www.alibabacloud.com/help/en/doc-detail/29807.htm)
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str status: Record status. Valid items are `ENABLE` and `DISABLE`.
    :param str type: Record type. Valid items are `A`, `NS`, `MX`, `TXT`, `CNAME`, `SRV`, `AAAA`, `REDIRECT_URL`, `FORWORD_URL` .
    :param str value_regex: Host record value regex.
    """
    ...
