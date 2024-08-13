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
    'GetCommandsResult',
    'AwaitableGetCommandsResult',
    'get_commands',
    'get_commands_output',
]

@pulumi.output_type
class GetCommandsResult:
    """
    A collection of values returned by getCommands.
    """
    def __init__(__self__, command_type=None, commands=None, content_encoding=None, desktop_id=None, id=None, ids=None, output_file=None, status=None):
        if command_type and not isinstance(command_type, str):
            raise TypeError("Expected argument 'command_type' to be a str")
        pulumi.set(__self__, "command_type", command_type)
        if commands and not isinstance(commands, list):
            raise TypeError("Expected argument 'commands' to be a list")
        pulumi.set(__self__, "commands", commands)
        if content_encoding and not isinstance(content_encoding, str):
            raise TypeError("Expected argument 'content_encoding' to be a str")
        pulumi.set(__self__, "content_encoding", content_encoding)
        if desktop_id and not isinstance(desktop_id, str):
            raise TypeError("Expected argument 'desktop_id' to be a str")
        pulumi.set(__self__, "desktop_id", desktop_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="commandType")
    def command_type(self) -> Optional[str]:
        return pulumi.get(self, "command_type")

    @property
    @pulumi.getter
    def commands(self) -> Sequence['outputs.GetCommandsCommandResult']:
        return pulumi.get(self, "commands")

    @property
    @pulumi.getter(name="contentEncoding")
    def content_encoding(self) -> Optional[str]:
        return pulumi.get(self, "content_encoding")

    @property
    @pulumi.getter(name="desktopId")
    def desktop_id(self) -> Optional[str]:
        return pulumi.get(self, "desktop_id")

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
    def status(self) -> Optional[str]:
        return pulumi.get(self, "status")


class AwaitableGetCommandsResult(GetCommandsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCommandsResult(
            command_type=self.command_type,
            commands=self.commands,
            content_encoding=self.content_encoding,
            desktop_id=self.desktop_id,
            id=self.id,
            ids=self.ids,
            output_file=self.output_file,
            status=self.status)


def get_commands(command_type: Optional[str] = None,
                 content_encoding: Optional[str] = None,
                 desktop_id: Optional[str] = None,
                 ids: Optional[Sequence[str]] = None,
                 output_file: Optional[str] = None,
                 status: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCommandsResult:
    """
    This data source provides the Ecd Commands of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.146.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    default_simple_office_site = alicloud.eds.SimpleOfficeSite("default",
        cidr_block="172.16.0.0/12",
        desktop_access_type="Internet",
        office_site_name="your_office_site_name")
    default = alicloud.eds.get_bundles(bundle_type="SYSTEM",
        name_regex="windows")
    default_ecd_policy_group = alicloud.eds.EcdPolicyGroup("default",
        policy_group_name="your_policy_group_name",
        clipboard="readwrite",
        local_drive="read",
        authorize_access_policy_rules=[{
            "description": "example_value",
            "cidr_ip": "1.2.3.4/24",
        }],
        authorize_security_policy_rules=[{
            "type": "inflow",
            "policy": "accept",
            "description": "example_value",
            "port_range": "80/80",
            "ip_protocol": "TCP",
            "priority": "1",
            "cidr_ip": "0.0.0.0/0",
        }])
    default_desktop = alicloud.eds.Desktop("default",
        office_site_id=default_simple_office_site.id,
        policy_group_id=default_ecd_policy_group.id,
        bundle_id=default.bundles[0].id,
        desktop_name=name)
    default_command = alicloud.eds.Command("default",
        command_content="ipconfig",
        command_type="RunPowerShellScript",
        desktop_id=default_desktop.id)
    ids = alicloud.eds.get_commands()
    pulumi.export("ecdCommandId1", ids.commands[0].id)
    ```


    :param str command_type: The Script Type. Valid values: `RunBatScript`, `RunPowerShellScript`.
    :param str content_encoding: That Returns the Data Encoding Method. Valid values: `Base64`, `PlainText`.
    :param str desktop_id: The desktop id of the Desktop.
    :param Sequence[str] ids: A list of Command IDs.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str status: Script Is Executed in the Overall Implementation of the State. Valid values: `Pending`, `Failed`, `PartialFailed`, `Running`, `Stopped`, `Stopping`, `Finished`, `Success`.
    """
    __args__ = dict()
    __args__['commandType'] = command_type
    __args__['contentEncoding'] = content_encoding
    __args__['desktopId'] = desktop_id
    __args__['ids'] = ids
    __args__['outputFile'] = output_file
    __args__['status'] = status
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:eds/getCommands:getCommands', __args__, opts=opts, typ=GetCommandsResult).value

    return AwaitableGetCommandsResult(
        command_type=pulumi.get(__ret__, 'command_type'),
        commands=pulumi.get(__ret__, 'commands'),
        content_encoding=pulumi.get(__ret__, 'content_encoding'),
        desktop_id=pulumi.get(__ret__, 'desktop_id'),
        id=pulumi.get(__ret__, 'id'),
        ids=pulumi.get(__ret__, 'ids'),
        output_file=pulumi.get(__ret__, 'output_file'),
        status=pulumi.get(__ret__, 'status'))


@_utilities.lift_output_func(get_commands)
def get_commands_output(command_type: Optional[pulumi.Input[Optional[str]]] = None,
                        content_encoding: Optional[pulumi.Input[Optional[str]]] = None,
                        desktop_id: Optional[pulumi.Input[Optional[str]]] = None,
                        ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                        output_file: Optional[pulumi.Input[Optional[str]]] = None,
                        status: Optional[pulumi.Input[Optional[str]]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetCommandsResult]:
    """
    This data source provides the Ecd Commands of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.146.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    default_simple_office_site = alicloud.eds.SimpleOfficeSite("default",
        cidr_block="172.16.0.0/12",
        desktop_access_type="Internet",
        office_site_name="your_office_site_name")
    default = alicloud.eds.get_bundles(bundle_type="SYSTEM",
        name_regex="windows")
    default_ecd_policy_group = alicloud.eds.EcdPolicyGroup("default",
        policy_group_name="your_policy_group_name",
        clipboard="readwrite",
        local_drive="read",
        authorize_access_policy_rules=[{
            "description": "example_value",
            "cidr_ip": "1.2.3.4/24",
        }],
        authorize_security_policy_rules=[{
            "type": "inflow",
            "policy": "accept",
            "description": "example_value",
            "port_range": "80/80",
            "ip_protocol": "TCP",
            "priority": "1",
            "cidr_ip": "0.0.0.0/0",
        }])
    default_desktop = alicloud.eds.Desktop("default",
        office_site_id=default_simple_office_site.id,
        policy_group_id=default_ecd_policy_group.id,
        bundle_id=default.bundles[0].id,
        desktop_name=name)
    default_command = alicloud.eds.Command("default",
        command_content="ipconfig",
        command_type="RunPowerShellScript",
        desktop_id=default_desktop.id)
    ids = alicloud.eds.get_commands()
    pulumi.export("ecdCommandId1", ids.commands[0].id)
    ```


    :param str command_type: The Script Type. Valid values: `RunBatScript`, `RunPowerShellScript`.
    :param str content_encoding: That Returns the Data Encoding Method. Valid values: `Base64`, `PlainText`.
    :param str desktop_id: The desktop id of the Desktop.
    :param Sequence[str] ids: A list of Command IDs.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str status: Script Is Executed in the Overall Implementation of the State. Valid values: `Pending`, `Failed`, `PartialFailed`, `Running`, `Stopped`, `Stopping`, `Finished`, `Success`.
    """
    ...
