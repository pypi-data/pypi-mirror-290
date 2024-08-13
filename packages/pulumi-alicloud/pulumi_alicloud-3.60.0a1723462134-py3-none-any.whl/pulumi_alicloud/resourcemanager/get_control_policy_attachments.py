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
    'GetControlPolicyAttachmentsResult',
    'AwaitableGetControlPolicyAttachmentsResult',
    'get_control_policy_attachments',
    'get_control_policy_attachments_output',
]

@pulumi.output_type
class GetControlPolicyAttachmentsResult:
    """
    A collection of values returned by getControlPolicyAttachments.
    """
    def __init__(__self__, attachments=None, id=None, ids=None, language=None, output_file=None, policy_type=None, target_id=None):
        if attachments and not isinstance(attachments, list):
            raise TypeError("Expected argument 'attachments' to be a list")
        pulumi.set(__self__, "attachments", attachments)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if language and not isinstance(language, str):
            raise TypeError("Expected argument 'language' to be a str")
        pulumi.set(__self__, "language", language)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if policy_type and not isinstance(policy_type, str):
            raise TypeError("Expected argument 'policy_type' to be a str")
        pulumi.set(__self__, "policy_type", policy_type)
        if target_id and not isinstance(target_id, str):
            raise TypeError("Expected argument 'target_id' to be a str")
        pulumi.set(__self__, "target_id", target_id)

    @property
    @pulumi.getter
    def attachments(self) -> Sequence['outputs.GetControlPolicyAttachmentsAttachmentResult']:
        return pulumi.get(self, "attachments")

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
    def language(self) -> Optional[str]:
        return pulumi.get(self, "language")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter(name="policyType")
    def policy_type(self) -> Optional[str]:
        return pulumi.get(self, "policy_type")

    @property
    @pulumi.getter(name="targetId")
    def target_id(self) -> str:
        return pulumi.get(self, "target_id")


class AwaitableGetControlPolicyAttachmentsResult(GetControlPolicyAttachmentsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetControlPolicyAttachmentsResult(
            attachments=self.attachments,
            id=self.id,
            ids=self.ids,
            language=self.language,
            output_file=self.output_file,
            policy_type=self.policy_type,
            target_id=self.target_id)


def get_control_policy_attachments(language: Optional[str] = None,
                                   output_file: Optional[str] = None,
                                   policy_type: Optional[str] = None,
                                   target_id: Optional[str] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetControlPolicyAttachmentsResult:
    """
    This data source provides the Resource Manager Control Policy Attachments of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.120.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    example = alicloud.resourcemanager.get_control_policy_attachments(target_id="example_value")
    pulumi.export("firstResourceManagerControlPolicyAttachmentId", example.attachments[0].id)
    ```


    :param str language: The language. Valid value `zh-CN`, `en`, and `ja`. Default value `zh-CN`
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str policy_type: The policy type of control policy. Valid values: `Custom` and `System`.
    :param str target_id: The Id of target.
    """
    __args__ = dict()
    __args__['language'] = language
    __args__['outputFile'] = output_file
    __args__['policyType'] = policy_type
    __args__['targetId'] = target_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:resourcemanager/getControlPolicyAttachments:getControlPolicyAttachments', __args__, opts=opts, typ=GetControlPolicyAttachmentsResult).value

    return AwaitableGetControlPolicyAttachmentsResult(
        attachments=pulumi.get(__ret__, 'attachments'),
        id=pulumi.get(__ret__, 'id'),
        ids=pulumi.get(__ret__, 'ids'),
        language=pulumi.get(__ret__, 'language'),
        output_file=pulumi.get(__ret__, 'output_file'),
        policy_type=pulumi.get(__ret__, 'policy_type'),
        target_id=pulumi.get(__ret__, 'target_id'))


@_utilities.lift_output_func(get_control_policy_attachments)
def get_control_policy_attachments_output(language: Optional[pulumi.Input[Optional[str]]] = None,
                                          output_file: Optional[pulumi.Input[Optional[str]]] = None,
                                          policy_type: Optional[pulumi.Input[Optional[str]]] = None,
                                          target_id: Optional[pulumi.Input[str]] = None,
                                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetControlPolicyAttachmentsResult]:
    """
    This data source provides the Resource Manager Control Policy Attachments of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.120.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    example = alicloud.resourcemanager.get_control_policy_attachments(target_id="example_value")
    pulumi.export("firstResourceManagerControlPolicyAttachmentId", example.attachments[0].id)
    ```


    :param str language: The language. Valid value `zh-CN`, `en`, and `ja`. Default value `zh-CN`
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str policy_type: The policy type of control policy. Valid values: `Custom` and `System`.
    :param str target_id: The Id of target.
    """
    ...
