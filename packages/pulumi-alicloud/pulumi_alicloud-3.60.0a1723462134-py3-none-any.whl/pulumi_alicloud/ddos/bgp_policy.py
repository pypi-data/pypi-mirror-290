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
from ._inputs import *

__all__ = ['BgpPolicyArgs', 'BgpPolicy']

@pulumi.input_type
class BgpPolicyArgs:
    def __init__(__self__, *,
                 policy_name: pulumi.Input[str],
                 type: pulumi.Input[str],
                 content: Optional[pulumi.Input['BgpPolicyContentArgs']] = None):
        """
        The set of arguments for constructing a BgpPolicy resource.
        :param pulumi.Input[str] policy_name: The name of the resource
        :param pulumi.Input[str] type: Type
        :param pulumi.Input['BgpPolicyContentArgs'] content: Configuration Content See `content` below.
        """
        pulumi.set(__self__, "policy_name", policy_name)
        pulumi.set(__self__, "type", type)
        if content is not None:
            pulumi.set(__self__, "content", content)

    @property
    @pulumi.getter(name="policyName")
    def policy_name(self) -> pulumi.Input[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "policy_name")

    @policy_name.setter
    def policy_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy_name", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        Type
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def content(self) -> Optional[pulumi.Input['BgpPolicyContentArgs']]:
        """
        Configuration Content See `content` below.
        """
        return pulumi.get(self, "content")

    @content.setter
    def content(self, value: Optional[pulumi.Input['BgpPolicyContentArgs']]):
        pulumi.set(self, "content", value)


@pulumi.input_type
class _BgpPolicyState:
    def __init__(__self__, *,
                 content: Optional[pulumi.Input['BgpPolicyContentArgs']] = None,
                 policy_name: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering BgpPolicy resources.
        :param pulumi.Input['BgpPolicyContentArgs'] content: Configuration Content See `content` below.
        :param pulumi.Input[str] policy_name: The name of the resource
        :param pulumi.Input[str] type: Type
        """
        if content is not None:
            pulumi.set(__self__, "content", content)
        if policy_name is not None:
            pulumi.set(__self__, "policy_name", policy_name)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def content(self) -> Optional[pulumi.Input['BgpPolicyContentArgs']]:
        """
        Configuration Content See `content` below.
        """
        return pulumi.get(self, "content")

    @content.setter
    def content(self, value: Optional[pulumi.Input['BgpPolicyContentArgs']]):
        pulumi.set(self, "content", value)

    @property
    @pulumi.getter(name="policyName")
    def policy_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource
        """
        return pulumi.get(self, "policy_name")

    @policy_name.setter
    def policy_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_name", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Type
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


class BgpPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 content: Optional[pulumi.Input[Union['BgpPolicyContentArgs', 'BgpPolicyContentArgsDict']]] = None,
                 policy_name: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Ddos Bgp Policy resource.

        Ddos protection policy.

        For information about Ddos Bgp Policy and how to use it, see [What is Policy](https://www.alibabacloud.com/help/en/).

        > **NOTE:** Available since v1.226.0.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "tf_exampleacc_bgp32594"
        policy_name = config.get("policyName")
        if policy_name is None:
            policy_name = "example_l4_policy"
        default = alicloud.ddos.BgpPolicy("default",
            content={
                "enable_defense": False,
                "layer4_rule_lists": [{
                    "method": "hex",
                    "match": "1",
                    "action": "1",
                    "limited": 0,
                    "condition_lists": [{
                        "arg": "3C",
                        "position": 1,
                        "depth": 2,
                    }],
                    "name": "11",
                    "priority": 10,
                }],
            },
            type="l4",
            policy_name="tf_exampleacc_bgp32594")
        ```

        ## Import

        Ddos Bgp Policy can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:ddos/bgpPolicy:BgpPolicy example <id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union['BgpPolicyContentArgs', 'BgpPolicyContentArgsDict']] content: Configuration Content See `content` below.
        :param pulumi.Input[str] policy_name: The name of the resource
        :param pulumi.Input[str] type: Type
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BgpPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Ddos Bgp Policy resource.

        Ddos protection policy.

        For information about Ddos Bgp Policy and how to use it, see [What is Policy](https://www.alibabacloud.com/help/en/).

        > **NOTE:** Available since v1.226.0.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "tf_exampleacc_bgp32594"
        policy_name = config.get("policyName")
        if policy_name is None:
            policy_name = "example_l4_policy"
        default = alicloud.ddos.BgpPolicy("default",
            content={
                "enable_defense": False,
                "layer4_rule_lists": [{
                    "method": "hex",
                    "match": "1",
                    "action": "1",
                    "limited": 0,
                    "condition_lists": [{
                        "arg": "3C",
                        "position": 1,
                        "depth": 2,
                    }],
                    "name": "11",
                    "priority": 10,
                }],
            },
            type="l4",
            policy_name="tf_exampleacc_bgp32594")
        ```

        ## Import

        Ddos Bgp Policy can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:ddos/bgpPolicy:BgpPolicy example <id>
        ```

        :param str resource_name: The name of the resource.
        :param BgpPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BgpPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 content: Optional[pulumi.Input[Union['BgpPolicyContentArgs', 'BgpPolicyContentArgsDict']]] = None,
                 policy_name: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BgpPolicyArgs.__new__(BgpPolicyArgs)

            __props__.__dict__["content"] = content
            if policy_name is None and not opts.urn:
                raise TypeError("Missing required property 'policy_name'")
            __props__.__dict__["policy_name"] = policy_name
            if type is None and not opts.urn:
                raise TypeError("Missing required property 'type'")
            __props__.__dict__["type"] = type
        super(BgpPolicy, __self__).__init__(
            'alicloud:ddos/bgpPolicy:BgpPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            content: Optional[pulumi.Input[Union['BgpPolicyContentArgs', 'BgpPolicyContentArgsDict']]] = None,
            policy_name: Optional[pulumi.Input[str]] = None,
            type: Optional[pulumi.Input[str]] = None) -> 'BgpPolicy':
        """
        Get an existing BgpPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union['BgpPolicyContentArgs', 'BgpPolicyContentArgsDict']] content: Configuration Content See `content` below.
        :param pulumi.Input[str] policy_name: The name of the resource
        :param pulumi.Input[str] type: Type
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _BgpPolicyState.__new__(_BgpPolicyState)

        __props__.__dict__["content"] = content
        __props__.__dict__["policy_name"] = policy_name
        __props__.__dict__["type"] = type
        return BgpPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def content(self) -> pulumi.Output['outputs.BgpPolicyContent']:
        """
        Configuration Content See `content` below.
        """
        return pulumi.get(self, "content")

    @property
    @pulumi.getter(name="policyName")
    def policy_name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "policy_name")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type
        """
        return pulumi.get(self, "type")

