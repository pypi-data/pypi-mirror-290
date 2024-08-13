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
    def __init__(__self__, command_provider=None, commands=None, content_encoding=None, description=None, id=None, ids=None, name=None, name_regex=None, names=None, output_file=None, type=None):
        if command_provider and not isinstance(command_provider, str):
            raise TypeError("Expected argument 'command_provider' to be a str")
        pulumi.set(__self__, "command_provider", command_provider)
        if commands and not isinstance(commands, list):
            raise TypeError("Expected argument 'commands' to be a list")
        pulumi.set(__self__, "commands", commands)
        if content_encoding and not isinstance(content_encoding, str):
            raise TypeError("Expected argument 'content_encoding' to be a str")
        pulumi.set(__self__, "content_encoding", content_encoding)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if name_regex and not isinstance(name_regex, str):
            raise TypeError("Expected argument 'name_regex' to be a str")
        pulumi.set(__self__, "name_regex", name_regex)
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        pulumi.set(__self__, "names", names)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="commandProvider")
    def command_provider(self) -> Optional[str]:
        return pulumi.get(self, "command_provider")

    @property
    @pulumi.getter
    def commands(self) -> Sequence['outputs.GetCommandsCommandResult']:
        return pulumi.get(self, "commands")

    @property
    @pulumi.getter(name="contentEncoding")
    def content_encoding(self) -> Optional[str]:
        return pulumi.get(self, "content_encoding")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        return pulumi.get(self, "description")

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
    @pulumi.getter
    def name(self) -> Optional[str]:
        return pulumi.get(self, "name")

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
    def type(self) -> Optional[str]:
        return pulumi.get(self, "type")


class AwaitableGetCommandsResult(GetCommandsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCommandsResult(
            command_provider=self.command_provider,
            commands=self.commands,
            content_encoding=self.content_encoding,
            description=self.description,
            id=self.id,
            ids=self.ids,
            name=self.name,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file,
            type=self.type)


def get_commands(command_provider: Optional[str] = None,
                 content_encoding: Optional[str] = None,
                 description: Optional[str] = None,
                 ids: Optional[Sequence[str]] = None,
                 name: Optional[str] = None,
                 name_regex: Optional[str] = None,
                 output_file: Optional[str] = None,
                 type: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCommandsResult:
    """
    This data source provides the Ecs Commands of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.116.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    example = alicloud.ecs.get_commands(ids=["E2RY53-xxxx"],
        name_regex="tf-testAcc")
    pulumi.export("firstEcsCommandId", example.commands[0].id)
    ```


    :param str command_provider: Public order provider.
    :param str content_encoding: The Base64-encoded content of the command.
    :param str description: The description of command.
    :param Sequence[str] ids: A list of Command IDs.
    :param str name: The name of the command.
    :param str name_regex: A regex string to filter results by Command name.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str type: The command type. Valid Values: `RunBatScript`, `RunPowerShellScript` and `RunShellScript`.
    """
    __args__ = dict()
    __args__['commandProvider'] = command_provider
    __args__['contentEncoding'] = content_encoding
    __args__['description'] = description
    __args__['ids'] = ids
    __args__['name'] = name
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    __args__['type'] = type
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:ecs/getCommands:getCommands', __args__, opts=opts, typ=GetCommandsResult).value

    return AwaitableGetCommandsResult(
        command_provider=pulumi.get(__ret__, 'command_provider'),
        commands=pulumi.get(__ret__, 'commands'),
        content_encoding=pulumi.get(__ret__, 'content_encoding'),
        description=pulumi.get(__ret__, 'description'),
        id=pulumi.get(__ret__, 'id'),
        ids=pulumi.get(__ret__, 'ids'),
        name=pulumi.get(__ret__, 'name'),
        name_regex=pulumi.get(__ret__, 'name_regex'),
        names=pulumi.get(__ret__, 'names'),
        output_file=pulumi.get(__ret__, 'output_file'),
        type=pulumi.get(__ret__, 'type'))


@_utilities.lift_output_func(get_commands)
def get_commands_output(command_provider: Optional[pulumi.Input[Optional[str]]] = None,
                        content_encoding: Optional[pulumi.Input[Optional[str]]] = None,
                        description: Optional[pulumi.Input[Optional[str]]] = None,
                        ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                        name: Optional[pulumi.Input[Optional[str]]] = None,
                        name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                        output_file: Optional[pulumi.Input[Optional[str]]] = None,
                        type: Optional[pulumi.Input[Optional[str]]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetCommandsResult]:
    """
    This data source provides the Ecs Commands of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.116.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    example = alicloud.ecs.get_commands(ids=["E2RY53-xxxx"],
        name_regex="tf-testAcc")
    pulumi.export("firstEcsCommandId", example.commands[0].id)
    ```


    :param str command_provider: Public order provider.
    :param str content_encoding: The Base64-encoded content of the command.
    :param str description: The description of command.
    :param Sequence[str] ids: A list of Command IDs.
    :param str name: The name of the command.
    :param str name_regex: A regex string to filter results by Command name.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str type: The command type. Valid Values: `RunBatScript`, `RunPowerShellScript` and `RunShellScript`.
    """
    ...
