# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['AliasArgs', 'Alias']

@pulumi.input_type
class AliasArgs:
    def __init__(__self__, *,
                 alias_name: pulumi.Input[str],
                 key_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a Alias resource.
        :param pulumi.Input[str] alias_name: The alias of CMK. `Encrypt`、`GenerateDataKey`、`DescribeKey` can be called using aliases. Length of characters other than prefixes: minimum length of 1 character and maximum length of 255 characters. Must contain prefix `alias/`.
        :param pulumi.Input[str] key_id: The id of the key.
               
               > **NOTE:** Each alias represents only one master key(CMK).
               
               > **NOTE:** Within an area of the same user, alias is not reproducible.
               
               > **NOTE:** UpdateAlias can be used to update the mapping relationship between alias and master key(CMK).
        """
        pulumi.set(__self__, "alias_name", alias_name)
        pulumi.set(__self__, "key_id", key_id)

    @property
    @pulumi.getter(name="aliasName")
    def alias_name(self) -> pulumi.Input[str]:
        """
        The alias of CMK. `Encrypt`、`GenerateDataKey`、`DescribeKey` can be called using aliases. Length of characters other than prefixes: minimum length of 1 character and maximum length of 255 characters. Must contain prefix `alias/`.
        """
        return pulumi.get(self, "alias_name")

    @alias_name.setter
    def alias_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "alias_name", value)

    @property
    @pulumi.getter(name="keyId")
    def key_id(self) -> pulumi.Input[str]:
        """
        The id of the key.

        > **NOTE:** Each alias represents only one master key(CMK).

        > **NOTE:** Within an area of the same user, alias is not reproducible.

        > **NOTE:** UpdateAlias can be used to update the mapping relationship between alias and master key(CMK).
        """
        return pulumi.get(self, "key_id")

    @key_id.setter
    def key_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "key_id", value)


@pulumi.input_type
class _AliasState:
    def __init__(__self__, *,
                 alias_name: Optional[pulumi.Input[str]] = None,
                 key_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Alias resources.
        :param pulumi.Input[str] alias_name: The alias of CMK. `Encrypt`、`GenerateDataKey`、`DescribeKey` can be called using aliases. Length of characters other than prefixes: minimum length of 1 character and maximum length of 255 characters. Must contain prefix `alias/`.
        :param pulumi.Input[str] key_id: The id of the key.
               
               > **NOTE:** Each alias represents only one master key(CMK).
               
               > **NOTE:** Within an area of the same user, alias is not reproducible.
               
               > **NOTE:** UpdateAlias can be used to update the mapping relationship between alias and master key(CMK).
        """
        if alias_name is not None:
            pulumi.set(__self__, "alias_name", alias_name)
        if key_id is not None:
            pulumi.set(__self__, "key_id", key_id)

    @property
    @pulumi.getter(name="aliasName")
    def alias_name(self) -> Optional[pulumi.Input[str]]:
        """
        The alias of CMK. `Encrypt`、`GenerateDataKey`、`DescribeKey` can be called using aliases. Length of characters other than prefixes: minimum length of 1 character and maximum length of 255 characters. Must contain prefix `alias/`.
        """
        return pulumi.get(self, "alias_name")

    @alias_name.setter
    def alias_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "alias_name", value)

    @property
    @pulumi.getter(name="keyId")
    def key_id(self) -> Optional[pulumi.Input[str]]:
        """
        The id of the key.

        > **NOTE:** Each alias represents only one master key(CMK).

        > **NOTE:** Within an area of the same user, alias is not reproducible.

        > **NOTE:** UpdateAlias can be used to update the mapping relationship between alias and master key(CMK).
        """
        return pulumi.get(self, "key_id")

    @key_id.setter
    def key_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_id", value)


class Alias(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 alias_name: Optional[pulumi.Input[str]] = None,
                 key_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Create an alias for the master key (CMK).

        > **NOTE:** Available since v1.77.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        this = alicloud.kms.Key("this", pending_window_in_days=7)
        this_alias = alicloud.kms.Alias("this",
            alias_name="alias/example_kms_alias",
            key_id=this.id)
        ```

        ## Import

        KMS alias can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:kms/alias:Alias example alias/test_kms_alias
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] alias_name: The alias of CMK. `Encrypt`、`GenerateDataKey`、`DescribeKey` can be called using aliases. Length of characters other than prefixes: minimum length of 1 character and maximum length of 255 characters. Must contain prefix `alias/`.
        :param pulumi.Input[str] key_id: The id of the key.
               
               > **NOTE:** Each alias represents only one master key(CMK).
               
               > **NOTE:** Within an area of the same user, alias is not reproducible.
               
               > **NOTE:** UpdateAlias can be used to update the mapping relationship between alias and master key(CMK).
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AliasArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create an alias for the master key (CMK).

        > **NOTE:** Available since v1.77.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        this = alicloud.kms.Key("this", pending_window_in_days=7)
        this_alias = alicloud.kms.Alias("this",
            alias_name="alias/example_kms_alias",
            key_id=this.id)
        ```

        ## Import

        KMS alias can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:kms/alias:Alias example alias/test_kms_alias
        ```

        :param str resource_name: The name of the resource.
        :param AliasArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AliasArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 alias_name: Optional[pulumi.Input[str]] = None,
                 key_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AliasArgs.__new__(AliasArgs)

            if alias_name is None and not opts.urn:
                raise TypeError("Missing required property 'alias_name'")
            __props__.__dict__["alias_name"] = alias_name
            if key_id is None and not opts.urn:
                raise TypeError("Missing required property 'key_id'")
            __props__.__dict__["key_id"] = key_id
        super(Alias, __self__).__init__(
            'alicloud:kms/alias:Alias',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            alias_name: Optional[pulumi.Input[str]] = None,
            key_id: Optional[pulumi.Input[str]] = None) -> 'Alias':
        """
        Get an existing Alias resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] alias_name: The alias of CMK. `Encrypt`、`GenerateDataKey`、`DescribeKey` can be called using aliases. Length of characters other than prefixes: minimum length of 1 character and maximum length of 255 characters. Must contain prefix `alias/`.
        :param pulumi.Input[str] key_id: The id of the key.
               
               > **NOTE:** Each alias represents only one master key(CMK).
               
               > **NOTE:** Within an area of the same user, alias is not reproducible.
               
               > **NOTE:** UpdateAlias can be used to update the mapping relationship between alias and master key(CMK).
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AliasState.__new__(_AliasState)

        __props__.__dict__["alias_name"] = alias_name
        __props__.__dict__["key_id"] = key_id
        return Alias(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="aliasName")
    def alias_name(self) -> pulumi.Output[str]:
        """
        The alias of CMK. `Encrypt`、`GenerateDataKey`、`DescribeKey` can be called using aliases. Length of characters other than prefixes: minimum length of 1 character and maximum length of 255 characters. Must contain prefix `alias/`.
        """
        return pulumi.get(self, "alias_name")

    @property
    @pulumi.getter(name="keyId")
    def key_id(self) -> pulumi.Output[str]:
        """
        The id of the key.

        > **NOTE:** Each alias represents only one master key(CMK).

        > **NOTE:** Within an area of the same user, alias is not reproducible.

        > **NOTE:** UpdateAlias can be used to update the mapping relationship between alias and master key(CMK).
        """
        return pulumi.get(self, "key_id")

