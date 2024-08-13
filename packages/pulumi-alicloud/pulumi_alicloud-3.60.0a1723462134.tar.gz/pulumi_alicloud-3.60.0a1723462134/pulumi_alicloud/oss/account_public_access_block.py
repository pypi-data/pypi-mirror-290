# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['AccountPublicAccessBlockArgs', 'AccountPublicAccessBlock']

@pulumi.input_type
class AccountPublicAccessBlockArgs:
    def __init__(__self__, *,
                 block_public_access: pulumi.Input[bool]):
        """
        The set of arguments for constructing a AccountPublicAccessBlock resource.
        :param pulumi.Input[bool] block_public_access: Whether or not AlibabaCloud OSS should block public bucket policies for buckets in this account is enabled.
        """
        pulumi.set(__self__, "block_public_access", block_public_access)

    @property
    @pulumi.getter(name="blockPublicAccess")
    def block_public_access(self) -> pulumi.Input[bool]:
        """
        Whether or not AlibabaCloud OSS should block public bucket policies for buckets in this account is enabled.
        """
        return pulumi.get(self, "block_public_access")

    @block_public_access.setter
    def block_public_access(self, value: pulumi.Input[bool]):
        pulumi.set(self, "block_public_access", value)


@pulumi.input_type
class _AccountPublicAccessBlockState:
    def __init__(__self__, *,
                 block_public_access: Optional[pulumi.Input[bool]] = None):
        """
        Input properties used for looking up and filtering AccountPublicAccessBlock resources.
        :param pulumi.Input[bool] block_public_access: Whether or not AlibabaCloud OSS should block public bucket policies for buckets in this account is enabled.
        """
        if block_public_access is not None:
            pulumi.set(__self__, "block_public_access", block_public_access)

    @property
    @pulumi.getter(name="blockPublicAccess")
    def block_public_access(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether or not AlibabaCloud OSS should block public bucket policies for buckets in this account is enabled.
        """
        return pulumi.get(self, "block_public_access")

    @block_public_access.setter
    def block_public_access(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "block_public_access", value)


class AccountPublicAccessBlock(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 block_public_access: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        Provides a OSS Account Public Access Block resource. Blocking public access at the account level.

        For information about OSS Account Public Access Block and how to use it, see [What is Account Public Access Block](https://www.alibabacloud.com/help/en/oss/developer-reference/putpublicaccessblock).

        > **NOTE:** Available since v1.224.0.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "terraform-example"
        default = alicloud.oss.AccountPublicAccessBlock("default", block_public_access=True)
        ```

        ## Import

        OSS Account Public Access Block can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:oss/accountPublicAccessBlock:AccountPublicAccessBlock example
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] block_public_access: Whether or not AlibabaCloud OSS should block public bucket policies for buckets in this account is enabled.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AccountPublicAccessBlockArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a OSS Account Public Access Block resource. Blocking public access at the account level.

        For information about OSS Account Public Access Block and how to use it, see [What is Account Public Access Block](https://www.alibabacloud.com/help/en/oss/developer-reference/putpublicaccessblock).

        > **NOTE:** Available since v1.224.0.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "terraform-example"
        default = alicloud.oss.AccountPublicAccessBlock("default", block_public_access=True)
        ```

        ## Import

        OSS Account Public Access Block can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:oss/accountPublicAccessBlock:AccountPublicAccessBlock example
        ```

        :param str resource_name: The name of the resource.
        :param AccountPublicAccessBlockArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AccountPublicAccessBlockArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 block_public_access: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AccountPublicAccessBlockArgs.__new__(AccountPublicAccessBlockArgs)

            if block_public_access is None and not opts.urn:
                raise TypeError("Missing required property 'block_public_access'")
            __props__.__dict__["block_public_access"] = block_public_access
        super(AccountPublicAccessBlock, __self__).__init__(
            'alicloud:oss/accountPublicAccessBlock:AccountPublicAccessBlock',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            block_public_access: Optional[pulumi.Input[bool]] = None) -> 'AccountPublicAccessBlock':
        """
        Get an existing AccountPublicAccessBlock resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] block_public_access: Whether or not AlibabaCloud OSS should block public bucket policies for buckets in this account is enabled.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AccountPublicAccessBlockState.__new__(_AccountPublicAccessBlockState)

        __props__.__dict__["block_public_access"] = block_public_access
        return AccountPublicAccessBlock(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="blockPublicAccess")
    def block_public_access(self) -> pulumi.Output[bool]:
        """
        Whether or not AlibabaCloud OSS should block public bucket policies for buckets in this account is enabled.
        """
        return pulumi.get(self, "block_public_access")

