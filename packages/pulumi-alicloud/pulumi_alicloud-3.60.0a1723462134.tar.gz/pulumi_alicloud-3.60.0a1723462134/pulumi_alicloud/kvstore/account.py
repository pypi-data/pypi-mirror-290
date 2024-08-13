# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['AccountArgs', 'Account']

@pulumi.input_type
class AccountArgs:
    def __init__(__self__, *,
                 account_name: pulumi.Input[str],
                 instance_id: pulumi.Input[str],
                 account_password: Optional[pulumi.Input[str]] = None,
                 account_privilege: Optional[pulumi.Input[str]] = None,
                 account_type: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 kms_encrypted_password: Optional[pulumi.Input[str]] = None,
                 kms_encryption_context: Optional[pulumi.Input[Mapping[str, Any]]] = None):
        """
        The set of arguments for constructing a Account resource.
        :param pulumi.Input[str] account_name: The name of the account. The name must meet the following requirements:
               * The name can contain lowercase letters, digits, and hyphens (-), and must start with a lowercase letter.
               * The name can be up to 100 characters in length.
               * The name cannot be one of the reserved words in the [Reserved words for Redis account names](https://www.alibabacloud.com/help/zh/doc-detail/92665.htm) section.
        :param pulumi.Input[str] instance_id: The Id of instance in which account belongs (The engine version of instance must be 4.0 or 4.0+).
        :param pulumi.Input[str] account_password: The password of the account. The password must be 8 to 32 characters in length. It must contain at least three of the following character types: uppercase letters, lowercase letters, digits, and special characters. Special characters include `!@ # $ % ^ & * ( ) _ + - =`. You have to specify one of `account_password` and `kms_encrypted_password` fields.
        :param pulumi.Input[str] account_privilege: The privilege of account access database. Default value: `RoleReadWrite` 
               - `RoleReadOnly`: This value is only for Redis and Memcache
               - `RoleReadWrite`: This value is only for Redis and Memcache
        :param pulumi.Input[str] account_type: Privilege type of account.
               - Normal: Common privilege.
               Default to Normal.
        :param pulumi.Input[str] description: Database description. It cannot begin with https://. It must start with a Chinese character or English letter. It can include Chinese and English characters, underlines (_), hyphens (-), and numbers. The length may be 2-256 characters.
        :param pulumi.Input[str] kms_encrypted_password: An KMS encrypts password used to a KVStore account. If the `account_password` is filled in, this field will be ignored.
        :param pulumi.Input[Mapping[str, Any]] kms_encryption_context: An KMS encryption context used to decrypt `kms_encrypted_password` before creating or updating a KVStore account with `kms_encrypted_password`. See [Encryption Context](https://www.alibabacloud.com/help/doc-detail/42975.htm). It is valid when `kms_encrypted_password` is set.
        """
        pulumi.set(__self__, "account_name", account_name)
        pulumi.set(__self__, "instance_id", instance_id)
        if account_password is not None:
            pulumi.set(__self__, "account_password", account_password)
        if account_privilege is not None:
            pulumi.set(__self__, "account_privilege", account_privilege)
        if account_type is not None:
            pulumi.set(__self__, "account_type", account_type)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if kms_encrypted_password is not None:
            pulumi.set(__self__, "kms_encrypted_password", kms_encrypted_password)
        if kms_encryption_context is not None:
            pulumi.set(__self__, "kms_encryption_context", kms_encryption_context)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> pulumi.Input[str]:
        """
        The name of the account. The name must meet the following requirements:
        * The name can contain lowercase letters, digits, and hyphens (-), and must start with a lowercase letter.
        * The name can be up to 100 characters in length.
        * The name cannot be one of the reserved words in the [Reserved words for Redis account names](https://www.alibabacloud.com/help/zh/doc-detail/92665.htm) section.
        """
        return pulumi.get(self, "account_name")

    @account_name.setter
    def account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "account_name", value)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Input[str]:
        """
        The Id of instance in which account belongs (The engine version of instance must be 4.0 or 4.0+).
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter(name="accountPassword")
    def account_password(self) -> Optional[pulumi.Input[str]]:
        """
        The password of the account. The password must be 8 to 32 characters in length. It must contain at least three of the following character types: uppercase letters, lowercase letters, digits, and special characters. Special characters include `!@ # $ % ^ & * ( ) _ + - =`. You have to specify one of `account_password` and `kms_encrypted_password` fields.
        """
        return pulumi.get(self, "account_password")

    @account_password.setter
    def account_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_password", value)

    @property
    @pulumi.getter(name="accountPrivilege")
    def account_privilege(self) -> Optional[pulumi.Input[str]]:
        """
        The privilege of account access database. Default value: `RoleReadWrite` 
        - `RoleReadOnly`: This value is only for Redis and Memcache
        - `RoleReadWrite`: This value is only for Redis and Memcache
        """
        return pulumi.get(self, "account_privilege")

    @account_privilege.setter
    def account_privilege(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_privilege", value)

    @property
    @pulumi.getter(name="accountType")
    def account_type(self) -> Optional[pulumi.Input[str]]:
        """
        Privilege type of account.
        - Normal: Common privilege.
        Default to Normal.
        """
        return pulumi.get(self, "account_type")

    @account_type.setter
    def account_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_type", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Database description. It cannot begin with https://. It must start with a Chinese character or English letter. It can include Chinese and English characters, underlines (_), hyphens (-), and numbers. The length may be 2-256 characters.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="kmsEncryptedPassword")
    def kms_encrypted_password(self) -> Optional[pulumi.Input[str]]:
        """
        An KMS encrypts password used to a KVStore account. If the `account_password` is filled in, this field will be ignored.
        """
        return pulumi.get(self, "kms_encrypted_password")

    @kms_encrypted_password.setter
    def kms_encrypted_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_encrypted_password", value)

    @property
    @pulumi.getter(name="kmsEncryptionContext")
    def kms_encryption_context(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        An KMS encryption context used to decrypt `kms_encrypted_password` before creating or updating a KVStore account with `kms_encrypted_password`. See [Encryption Context](https://www.alibabacloud.com/help/doc-detail/42975.htm). It is valid when `kms_encrypted_password` is set.
        """
        return pulumi.get(self, "kms_encryption_context")

    @kms_encryption_context.setter
    def kms_encryption_context(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "kms_encryption_context", value)


@pulumi.input_type
class _AccountState:
    def __init__(__self__, *,
                 account_name: Optional[pulumi.Input[str]] = None,
                 account_password: Optional[pulumi.Input[str]] = None,
                 account_privilege: Optional[pulumi.Input[str]] = None,
                 account_type: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 kms_encrypted_password: Optional[pulumi.Input[str]] = None,
                 kms_encryption_context: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Account resources.
        :param pulumi.Input[str] account_name: The name of the account. The name must meet the following requirements:
               * The name can contain lowercase letters, digits, and hyphens (-), and must start with a lowercase letter.
               * The name can be up to 100 characters in length.
               * The name cannot be one of the reserved words in the [Reserved words for Redis account names](https://www.alibabacloud.com/help/zh/doc-detail/92665.htm) section.
        :param pulumi.Input[str] account_password: The password of the account. The password must be 8 to 32 characters in length. It must contain at least three of the following character types: uppercase letters, lowercase letters, digits, and special characters. Special characters include `!@ # $ % ^ & * ( ) _ + - =`. You have to specify one of `account_password` and `kms_encrypted_password` fields.
        :param pulumi.Input[str] account_privilege: The privilege of account access database. Default value: `RoleReadWrite` 
               - `RoleReadOnly`: This value is only for Redis and Memcache
               - `RoleReadWrite`: This value is only for Redis and Memcache
        :param pulumi.Input[str] account_type: Privilege type of account.
               - Normal: Common privilege.
               Default to Normal.
        :param pulumi.Input[str] description: Database description. It cannot begin with https://. It must start with a Chinese character or English letter. It can include Chinese and English characters, underlines (_), hyphens (-), and numbers. The length may be 2-256 characters.
        :param pulumi.Input[str] instance_id: The Id of instance in which account belongs (The engine version of instance must be 4.0 or 4.0+).
        :param pulumi.Input[str] kms_encrypted_password: An KMS encrypts password used to a KVStore account. If the `account_password` is filled in, this field will be ignored.
        :param pulumi.Input[Mapping[str, Any]] kms_encryption_context: An KMS encryption context used to decrypt `kms_encrypted_password` before creating or updating a KVStore account with `kms_encrypted_password`. See [Encryption Context](https://www.alibabacloud.com/help/doc-detail/42975.htm). It is valid when `kms_encrypted_password` is set.
        :param pulumi.Input[str] status: The status of KVStore Account.
        """
        if account_name is not None:
            pulumi.set(__self__, "account_name", account_name)
        if account_password is not None:
            pulumi.set(__self__, "account_password", account_password)
        if account_privilege is not None:
            pulumi.set(__self__, "account_privilege", account_privilege)
        if account_type is not None:
            pulumi.set(__self__, "account_type", account_type)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if instance_id is not None:
            pulumi.set(__self__, "instance_id", instance_id)
        if kms_encrypted_password is not None:
            pulumi.set(__self__, "kms_encrypted_password", kms_encrypted_password)
        if kms_encryption_context is not None:
            pulumi.set(__self__, "kms_encryption_context", kms_encryption_context)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the account. The name must meet the following requirements:
        * The name can contain lowercase letters, digits, and hyphens (-), and must start with a lowercase letter.
        * The name can be up to 100 characters in length.
        * The name cannot be one of the reserved words in the [Reserved words for Redis account names](https://www.alibabacloud.com/help/zh/doc-detail/92665.htm) section.
        """
        return pulumi.get(self, "account_name")

    @account_name.setter
    def account_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_name", value)

    @property
    @pulumi.getter(name="accountPassword")
    def account_password(self) -> Optional[pulumi.Input[str]]:
        """
        The password of the account. The password must be 8 to 32 characters in length. It must contain at least three of the following character types: uppercase letters, lowercase letters, digits, and special characters. Special characters include `!@ # $ % ^ & * ( ) _ + - =`. You have to specify one of `account_password` and `kms_encrypted_password` fields.
        """
        return pulumi.get(self, "account_password")

    @account_password.setter
    def account_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_password", value)

    @property
    @pulumi.getter(name="accountPrivilege")
    def account_privilege(self) -> Optional[pulumi.Input[str]]:
        """
        The privilege of account access database. Default value: `RoleReadWrite` 
        - `RoleReadOnly`: This value is only for Redis and Memcache
        - `RoleReadWrite`: This value is only for Redis and Memcache
        """
        return pulumi.get(self, "account_privilege")

    @account_privilege.setter
    def account_privilege(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_privilege", value)

    @property
    @pulumi.getter(name="accountType")
    def account_type(self) -> Optional[pulumi.Input[str]]:
        """
        Privilege type of account.
        - Normal: Common privilege.
        Default to Normal.
        """
        return pulumi.get(self, "account_type")

    @account_type.setter
    def account_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_type", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Database description. It cannot begin with https://. It must start with a Chinese character or English letter. It can include Chinese and English characters, underlines (_), hyphens (-), and numbers. The length may be 2-256 characters.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Id of instance in which account belongs (The engine version of instance must be 4.0 or 4.0+).
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter(name="kmsEncryptedPassword")
    def kms_encrypted_password(self) -> Optional[pulumi.Input[str]]:
        """
        An KMS encrypts password used to a KVStore account. If the `account_password` is filled in, this field will be ignored.
        """
        return pulumi.get(self, "kms_encrypted_password")

    @kms_encrypted_password.setter
    def kms_encrypted_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_encrypted_password", value)

    @property
    @pulumi.getter(name="kmsEncryptionContext")
    def kms_encryption_context(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        An KMS encryption context used to decrypt `kms_encrypted_password` before creating or updating a KVStore account with `kms_encrypted_password`. See [Encryption Context](https://www.alibabacloud.com/help/doc-detail/42975.htm). It is valid when `kms_encrypted_password` is set.
        """
        return pulumi.get(self, "kms_encryption_context")

    @kms_encryption_context.setter
    def kms_encryption_context(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "kms_encryption_context", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of KVStore Account.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


class Account(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 account_password: Optional[pulumi.Input[str]] = None,
                 account_privilege: Optional[pulumi.Input[str]] = None,
                 account_type: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 kms_encrypted_password: Optional[pulumi.Input[str]] = None,
                 kms_encryption_context: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 __props__=None):
        """
        Provides a KVStore Account resource.

        For information about KVStore Account and how to use it, see [What is Account](https://www.alibabacloud.com/help/doc-detail/95973.htm).

        > **NOTE:** Available since v1.66.0.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "tf-example"
        default = alicloud.kvstore.get_zones()
        default_get_resource_groups = alicloud.resourcemanager.get_resource_groups(status="OK")
        default_network = alicloud.vpc.Network("default",
            vpc_name=name,
            cidr_block="10.4.0.0/16")
        default_switch = alicloud.vpc.Switch("default",
            vswitch_name=name,
            cidr_block="10.4.0.0/24",
            vpc_id=default_network.id,
            zone_id=default.zones[0].id)
        default_instance = alicloud.kvstore.Instance("default",
            db_instance_name=name,
            vswitch_id=default_switch.id,
            resource_group_id=default_get_resource_groups.ids[0],
            zone_id=default.zones[0].id,
            instance_class="redis.master.large.default",
            instance_type="Redis",
            engine_version="5.0",
            security_ips=["10.23.12.24"],
            config={
                "appendonly": "yes",
                "lazyfree-lazy-eviction": "yes",
            },
            tags={
                "Created": "TF",
                "For": "example",
            })
        default_account = alicloud.kvstore.Account("default",
            account_name="tfexamplename",
            account_password="YourPassword_123",
            instance_id=default_instance.id)
        ```

        ## Import

        KVStore account can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:kvstore/account:Account example <instance_id>:<account_name>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The name of the account. The name must meet the following requirements:
               * The name can contain lowercase letters, digits, and hyphens (-), and must start with a lowercase letter.
               * The name can be up to 100 characters in length.
               * The name cannot be one of the reserved words in the [Reserved words for Redis account names](https://www.alibabacloud.com/help/zh/doc-detail/92665.htm) section.
        :param pulumi.Input[str] account_password: The password of the account. The password must be 8 to 32 characters in length. It must contain at least three of the following character types: uppercase letters, lowercase letters, digits, and special characters. Special characters include `!@ # $ % ^ & * ( ) _ + - =`. You have to specify one of `account_password` and `kms_encrypted_password` fields.
        :param pulumi.Input[str] account_privilege: The privilege of account access database. Default value: `RoleReadWrite` 
               - `RoleReadOnly`: This value is only for Redis and Memcache
               - `RoleReadWrite`: This value is only for Redis and Memcache
        :param pulumi.Input[str] account_type: Privilege type of account.
               - Normal: Common privilege.
               Default to Normal.
        :param pulumi.Input[str] description: Database description. It cannot begin with https://. It must start with a Chinese character or English letter. It can include Chinese and English characters, underlines (_), hyphens (-), and numbers. The length may be 2-256 characters.
        :param pulumi.Input[str] instance_id: The Id of instance in which account belongs (The engine version of instance must be 4.0 or 4.0+).
        :param pulumi.Input[str] kms_encrypted_password: An KMS encrypts password used to a KVStore account. If the `account_password` is filled in, this field will be ignored.
        :param pulumi.Input[Mapping[str, Any]] kms_encryption_context: An KMS encryption context used to decrypt `kms_encrypted_password` before creating or updating a KVStore account with `kms_encrypted_password`. See [Encryption Context](https://www.alibabacloud.com/help/doc-detail/42975.htm). It is valid when `kms_encrypted_password` is set.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AccountArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a KVStore Account resource.

        For information about KVStore Account and how to use it, see [What is Account](https://www.alibabacloud.com/help/doc-detail/95973.htm).

        > **NOTE:** Available since v1.66.0.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "tf-example"
        default = alicloud.kvstore.get_zones()
        default_get_resource_groups = alicloud.resourcemanager.get_resource_groups(status="OK")
        default_network = alicloud.vpc.Network("default",
            vpc_name=name,
            cidr_block="10.4.0.0/16")
        default_switch = alicloud.vpc.Switch("default",
            vswitch_name=name,
            cidr_block="10.4.0.0/24",
            vpc_id=default_network.id,
            zone_id=default.zones[0].id)
        default_instance = alicloud.kvstore.Instance("default",
            db_instance_name=name,
            vswitch_id=default_switch.id,
            resource_group_id=default_get_resource_groups.ids[0],
            zone_id=default.zones[0].id,
            instance_class="redis.master.large.default",
            instance_type="Redis",
            engine_version="5.0",
            security_ips=["10.23.12.24"],
            config={
                "appendonly": "yes",
                "lazyfree-lazy-eviction": "yes",
            },
            tags={
                "Created": "TF",
                "For": "example",
            })
        default_account = alicloud.kvstore.Account("default",
            account_name="tfexamplename",
            account_password="YourPassword_123",
            instance_id=default_instance.id)
        ```

        ## Import

        KVStore account can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:kvstore/account:Account example <instance_id>:<account_name>
        ```

        :param str resource_name: The name of the resource.
        :param AccountArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AccountArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 account_password: Optional[pulumi.Input[str]] = None,
                 account_privilege: Optional[pulumi.Input[str]] = None,
                 account_type: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 kms_encrypted_password: Optional[pulumi.Input[str]] = None,
                 kms_encryption_context: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AccountArgs.__new__(AccountArgs)

            if account_name is None and not opts.urn:
                raise TypeError("Missing required property 'account_name'")
            __props__.__dict__["account_name"] = account_name
            __props__.__dict__["account_password"] = None if account_password is None else pulumi.Output.secret(account_password)
            __props__.__dict__["account_privilege"] = account_privilege
            __props__.__dict__["account_type"] = account_type
            __props__.__dict__["description"] = description
            if instance_id is None and not opts.urn:
                raise TypeError("Missing required property 'instance_id'")
            __props__.__dict__["instance_id"] = instance_id
            __props__.__dict__["kms_encrypted_password"] = kms_encrypted_password
            __props__.__dict__["kms_encryption_context"] = kms_encryption_context
            __props__.__dict__["status"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["accountPassword"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(Account, __self__).__init__(
            'alicloud:kvstore/account:Account',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            account_name: Optional[pulumi.Input[str]] = None,
            account_password: Optional[pulumi.Input[str]] = None,
            account_privilege: Optional[pulumi.Input[str]] = None,
            account_type: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            instance_id: Optional[pulumi.Input[str]] = None,
            kms_encrypted_password: Optional[pulumi.Input[str]] = None,
            kms_encryption_context: Optional[pulumi.Input[Mapping[str, Any]]] = None,
            status: Optional[pulumi.Input[str]] = None) -> 'Account':
        """
        Get an existing Account resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The name of the account. The name must meet the following requirements:
               * The name can contain lowercase letters, digits, and hyphens (-), and must start with a lowercase letter.
               * The name can be up to 100 characters in length.
               * The name cannot be one of the reserved words in the [Reserved words for Redis account names](https://www.alibabacloud.com/help/zh/doc-detail/92665.htm) section.
        :param pulumi.Input[str] account_password: The password of the account. The password must be 8 to 32 characters in length. It must contain at least three of the following character types: uppercase letters, lowercase letters, digits, and special characters. Special characters include `!@ # $ % ^ & * ( ) _ + - =`. You have to specify one of `account_password` and `kms_encrypted_password` fields.
        :param pulumi.Input[str] account_privilege: The privilege of account access database. Default value: `RoleReadWrite` 
               - `RoleReadOnly`: This value is only for Redis and Memcache
               - `RoleReadWrite`: This value is only for Redis and Memcache
        :param pulumi.Input[str] account_type: Privilege type of account.
               - Normal: Common privilege.
               Default to Normal.
        :param pulumi.Input[str] description: Database description. It cannot begin with https://. It must start with a Chinese character or English letter. It can include Chinese and English characters, underlines (_), hyphens (-), and numbers. The length may be 2-256 characters.
        :param pulumi.Input[str] instance_id: The Id of instance in which account belongs (The engine version of instance must be 4.0 or 4.0+).
        :param pulumi.Input[str] kms_encrypted_password: An KMS encrypts password used to a KVStore account. If the `account_password` is filled in, this field will be ignored.
        :param pulumi.Input[Mapping[str, Any]] kms_encryption_context: An KMS encryption context used to decrypt `kms_encrypted_password` before creating or updating a KVStore account with `kms_encrypted_password`. See [Encryption Context](https://www.alibabacloud.com/help/doc-detail/42975.htm). It is valid when `kms_encrypted_password` is set.
        :param pulumi.Input[str] status: The status of KVStore Account.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AccountState.__new__(_AccountState)

        __props__.__dict__["account_name"] = account_name
        __props__.__dict__["account_password"] = account_password
        __props__.__dict__["account_privilege"] = account_privilege
        __props__.__dict__["account_type"] = account_type
        __props__.__dict__["description"] = description
        __props__.__dict__["instance_id"] = instance_id
        __props__.__dict__["kms_encrypted_password"] = kms_encrypted_password
        __props__.__dict__["kms_encryption_context"] = kms_encryption_context
        __props__.__dict__["status"] = status
        return Account(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> pulumi.Output[str]:
        """
        The name of the account. The name must meet the following requirements:
        * The name can contain lowercase letters, digits, and hyphens (-), and must start with a lowercase letter.
        * The name can be up to 100 characters in length.
        * The name cannot be one of the reserved words in the [Reserved words for Redis account names](https://www.alibabacloud.com/help/zh/doc-detail/92665.htm) section.
        """
        return pulumi.get(self, "account_name")

    @property
    @pulumi.getter(name="accountPassword")
    def account_password(self) -> pulumi.Output[Optional[str]]:
        """
        The password of the account. The password must be 8 to 32 characters in length. It must contain at least three of the following character types: uppercase letters, lowercase letters, digits, and special characters. Special characters include `!@ # $ % ^ & * ( ) _ + - =`. You have to specify one of `account_password` and `kms_encrypted_password` fields.
        """
        return pulumi.get(self, "account_password")

    @property
    @pulumi.getter(name="accountPrivilege")
    def account_privilege(self) -> pulumi.Output[Optional[str]]:
        """
        The privilege of account access database. Default value: `RoleReadWrite` 
        - `RoleReadOnly`: This value is only for Redis and Memcache
        - `RoleReadWrite`: This value is only for Redis and Memcache
        """
        return pulumi.get(self, "account_privilege")

    @property
    @pulumi.getter(name="accountType")
    def account_type(self) -> pulumi.Output[Optional[str]]:
        """
        Privilege type of account.
        - Normal: Common privilege.
        Default to Normal.
        """
        return pulumi.get(self, "account_type")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Database description. It cannot begin with https://. It must start with a Chinese character or English letter. It can include Chinese and English characters, underlines (_), hyphens (-), and numbers. The length may be 2-256 characters.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Output[str]:
        """
        The Id of instance in which account belongs (The engine version of instance must be 4.0 or 4.0+).
        """
        return pulumi.get(self, "instance_id")

    @property
    @pulumi.getter(name="kmsEncryptedPassword")
    def kms_encrypted_password(self) -> pulumi.Output[Optional[str]]:
        """
        An KMS encrypts password used to a KVStore account. If the `account_password` is filled in, this field will be ignored.
        """
        return pulumi.get(self, "kms_encrypted_password")

    @property
    @pulumi.getter(name="kmsEncryptionContext")
    def kms_encryption_context(self) -> pulumi.Output[Optional[Mapping[str, Any]]]:
        """
        An KMS encryption context used to decrypt `kms_encrypted_password` before creating or updating a KVStore account with `kms_encrypted_password`. See [Encryption Context](https://www.alibabacloud.com/help/doc-detail/42975.htm). It is valid when `kms_encrypted_password` is set.
        """
        return pulumi.get(self, "kms_encryption_context")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The status of KVStore Account.
        """
        return pulumi.get(self, "status")

