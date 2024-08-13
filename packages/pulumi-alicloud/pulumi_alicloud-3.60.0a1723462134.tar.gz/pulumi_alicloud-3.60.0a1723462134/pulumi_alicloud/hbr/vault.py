# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['VaultArgs', 'Vault']

@pulumi.input_type
class VaultArgs:
    def __init__(__self__, *,
                 vault_name: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 encrypt_type: Optional[pulumi.Input[str]] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 vault_storage_class: Optional[pulumi.Input[str]] = None,
                 vault_type: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Vault resource.
        :param pulumi.Input[str] vault_name: The name of Vault.
        :param pulumi.Input[str] description: The description of Vault. Defaults to an empty string.
        :param pulumi.Input[str] encrypt_type: Source Encryption Type，It is valid only when vault_type is `STANDARD` or `OTS_BACKUP`. Default value: `HBR_PRIVATE`. Valid values:
               - `HBR_PRIVATE`: HBR is fully hosted, uses the backup service's own encryption method.
               - `KMS`: Use Alibaba Cloud Kms to encryption.
        :param pulumi.Input[str] kms_key_id: The key id or alias name of Alibaba Cloud Kms. It is required and valid only when encrypt_type is `KMS`.
        :param pulumi.Input[str] vault_storage_class: The storage class of Vault. Valid values: `STANDARD`.
        :param pulumi.Input[str] vault_type: The type of Vault. Valid values: `STANDARD`, `OTS_BACKUP`.
        """
        pulumi.set(__self__, "vault_name", vault_name)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if encrypt_type is not None:
            pulumi.set(__self__, "encrypt_type", encrypt_type)
        if kms_key_id is not None:
            pulumi.set(__self__, "kms_key_id", kms_key_id)
        if vault_storage_class is not None:
            pulumi.set(__self__, "vault_storage_class", vault_storage_class)
        if vault_type is not None:
            pulumi.set(__self__, "vault_type", vault_type)

    @property
    @pulumi.getter(name="vaultName")
    def vault_name(self) -> pulumi.Input[str]:
        """
        The name of Vault.
        """
        return pulumi.get(self, "vault_name")

    @vault_name.setter
    def vault_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "vault_name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of Vault. Defaults to an empty string.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="encryptType")
    def encrypt_type(self) -> Optional[pulumi.Input[str]]:
        """
        Source Encryption Type，It is valid only when vault_type is `STANDARD` or `OTS_BACKUP`. Default value: `HBR_PRIVATE`. Valid values:
        - `HBR_PRIVATE`: HBR is fully hosted, uses the backup service's own encryption method.
        - `KMS`: Use Alibaba Cloud Kms to encryption.
        """
        return pulumi.get(self, "encrypt_type")

    @encrypt_type.setter
    def encrypt_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "encrypt_type", value)

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> Optional[pulumi.Input[str]]:
        """
        The key id or alias name of Alibaba Cloud Kms. It is required and valid only when encrypt_type is `KMS`.
        """
        return pulumi.get(self, "kms_key_id")

    @kms_key_id.setter
    def kms_key_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_key_id", value)

    @property
    @pulumi.getter(name="vaultStorageClass")
    def vault_storage_class(self) -> Optional[pulumi.Input[str]]:
        """
        The storage class of Vault. Valid values: `STANDARD`.
        """
        return pulumi.get(self, "vault_storage_class")

    @vault_storage_class.setter
    def vault_storage_class(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vault_storage_class", value)

    @property
    @pulumi.getter(name="vaultType")
    def vault_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of Vault. Valid values: `STANDARD`, `OTS_BACKUP`.
        """
        return pulumi.get(self, "vault_type")

    @vault_type.setter
    def vault_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vault_type", value)


@pulumi.input_type
class _VaultState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 encrypt_type: Optional[pulumi.Input[str]] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 vault_name: Optional[pulumi.Input[str]] = None,
                 vault_storage_class: Optional[pulumi.Input[str]] = None,
                 vault_type: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Vault resources.
        :param pulumi.Input[str] description: The description of Vault. Defaults to an empty string.
        :param pulumi.Input[str] encrypt_type: Source Encryption Type，It is valid only when vault_type is `STANDARD` or `OTS_BACKUP`. Default value: `HBR_PRIVATE`. Valid values:
               - `HBR_PRIVATE`: HBR is fully hosted, uses the backup service's own encryption method.
               - `KMS`: Use Alibaba Cloud Kms to encryption.
        :param pulumi.Input[str] kms_key_id: The key id or alias name of Alibaba Cloud Kms. It is required and valid only when encrypt_type is `KMS`.
        :param pulumi.Input[str] status: The status of the Vault.
        :param pulumi.Input[str] vault_name: The name of Vault.
        :param pulumi.Input[str] vault_storage_class: The storage class of Vault. Valid values: `STANDARD`.
        :param pulumi.Input[str] vault_type: The type of Vault. Valid values: `STANDARD`, `OTS_BACKUP`.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if encrypt_type is not None:
            pulumi.set(__self__, "encrypt_type", encrypt_type)
        if kms_key_id is not None:
            pulumi.set(__self__, "kms_key_id", kms_key_id)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if vault_name is not None:
            pulumi.set(__self__, "vault_name", vault_name)
        if vault_storage_class is not None:
            pulumi.set(__self__, "vault_storage_class", vault_storage_class)
        if vault_type is not None:
            pulumi.set(__self__, "vault_type", vault_type)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of Vault. Defaults to an empty string.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="encryptType")
    def encrypt_type(self) -> Optional[pulumi.Input[str]]:
        """
        Source Encryption Type，It is valid only when vault_type is `STANDARD` or `OTS_BACKUP`. Default value: `HBR_PRIVATE`. Valid values:
        - `HBR_PRIVATE`: HBR is fully hosted, uses the backup service's own encryption method.
        - `KMS`: Use Alibaba Cloud Kms to encryption.
        """
        return pulumi.get(self, "encrypt_type")

    @encrypt_type.setter
    def encrypt_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "encrypt_type", value)

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> Optional[pulumi.Input[str]]:
        """
        The key id or alias name of Alibaba Cloud Kms. It is required and valid only when encrypt_type is `KMS`.
        """
        return pulumi.get(self, "kms_key_id")

    @kms_key_id.setter
    def kms_key_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_key_id", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the Vault.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter(name="vaultName")
    def vault_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of Vault.
        """
        return pulumi.get(self, "vault_name")

    @vault_name.setter
    def vault_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vault_name", value)

    @property
    @pulumi.getter(name="vaultStorageClass")
    def vault_storage_class(self) -> Optional[pulumi.Input[str]]:
        """
        The storage class of Vault. Valid values: `STANDARD`.
        """
        return pulumi.get(self, "vault_storage_class")

    @vault_storage_class.setter
    def vault_storage_class(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vault_storage_class", value)

    @property
    @pulumi.getter(name="vaultType")
    def vault_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of Vault. Valid values: `STANDARD`, `OTS_BACKUP`.
        """
        return pulumi.get(self, "vault_type")

    @vault_type.setter
    def vault_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vault_type", value)


class Vault(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 encrypt_type: Optional[pulumi.Input[str]] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 vault_name: Optional[pulumi.Input[str]] = None,
                 vault_storage_class: Optional[pulumi.Input[str]] = None,
                 vault_type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a HBR Backup vault resource.

        For information about HBR Backup vault and how to use it, see [What is Backup vault](https://www.alibabacloud.com/help/en/hybrid-backup-recovery/latest/api-hbr-2017-09-08-createvault).

        > **NOTE:** Available since v1.129.0.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud
        import pulumi_random as random

        default = random.index.Integer("default",
            min=10000,
            max=99999)
        example = alicloud.hbr.Vault("example", vault_name=f"example_value_{default['result']}")
        ```

        ## Import

        HBR Vault can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:hbr/vault:Vault example <id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of Vault. Defaults to an empty string.
        :param pulumi.Input[str] encrypt_type: Source Encryption Type，It is valid only when vault_type is `STANDARD` or `OTS_BACKUP`. Default value: `HBR_PRIVATE`. Valid values:
               - `HBR_PRIVATE`: HBR is fully hosted, uses the backup service's own encryption method.
               - `KMS`: Use Alibaba Cloud Kms to encryption.
        :param pulumi.Input[str] kms_key_id: The key id or alias name of Alibaba Cloud Kms. It is required and valid only when encrypt_type is `KMS`.
        :param pulumi.Input[str] vault_name: The name of Vault.
        :param pulumi.Input[str] vault_storage_class: The storage class of Vault. Valid values: `STANDARD`.
        :param pulumi.Input[str] vault_type: The type of Vault. Valid values: `STANDARD`, `OTS_BACKUP`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: VaultArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a HBR Backup vault resource.

        For information about HBR Backup vault and how to use it, see [What is Backup vault](https://www.alibabacloud.com/help/en/hybrid-backup-recovery/latest/api-hbr-2017-09-08-createvault).

        > **NOTE:** Available since v1.129.0.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud
        import pulumi_random as random

        default = random.index.Integer("default",
            min=10000,
            max=99999)
        example = alicloud.hbr.Vault("example", vault_name=f"example_value_{default['result']}")
        ```

        ## Import

        HBR Vault can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:hbr/vault:Vault example <id>
        ```

        :param str resource_name: The name of the resource.
        :param VaultArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VaultArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 encrypt_type: Optional[pulumi.Input[str]] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 vault_name: Optional[pulumi.Input[str]] = None,
                 vault_storage_class: Optional[pulumi.Input[str]] = None,
                 vault_type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = VaultArgs.__new__(VaultArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["encrypt_type"] = encrypt_type
            __props__.__dict__["kms_key_id"] = kms_key_id
            if vault_name is None and not opts.urn:
                raise TypeError("Missing required property 'vault_name'")
            __props__.__dict__["vault_name"] = vault_name
            __props__.__dict__["vault_storage_class"] = vault_storage_class
            __props__.__dict__["vault_type"] = vault_type
            __props__.__dict__["status"] = None
        super(Vault, __self__).__init__(
            'alicloud:hbr/vault:Vault',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            encrypt_type: Optional[pulumi.Input[str]] = None,
            kms_key_id: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            vault_name: Optional[pulumi.Input[str]] = None,
            vault_storage_class: Optional[pulumi.Input[str]] = None,
            vault_type: Optional[pulumi.Input[str]] = None) -> 'Vault':
        """
        Get an existing Vault resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of Vault. Defaults to an empty string.
        :param pulumi.Input[str] encrypt_type: Source Encryption Type，It is valid only when vault_type is `STANDARD` or `OTS_BACKUP`. Default value: `HBR_PRIVATE`. Valid values:
               - `HBR_PRIVATE`: HBR is fully hosted, uses the backup service's own encryption method.
               - `KMS`: Use Alibaba Cloud Kms to encryption.
        :param pulumi.Input[str] kms_key_id: The key id or alias name of Alibaba Cloud Kms. It is required and valid only when encrypt_type is `KMS`.
        :param pulumi.Input[str] status: The status of the Vault.
        :param pulumi.Input[str] vault_name: The name of Vault.
        :param pulumi.Input[str] vault_storage_class: The storage class of Vault. Valid values: `STANDARD`.
        :param pulumi.Input[str] vault_type: The type of Vault. Valid values: `STANDARD`, `OTS_BACKUP`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _VaultState.__new__(_VaultState)

        __props__.__dict__["description"] = description
        __props__.__dict__["encrypt_type"] = encrypt_type
        __props__.__dict__["kms_key_id"] = kms_key_id
        __props__.__dict__["status"] = status
        __props__.__dict__["vault_name"] = vault_name
        __props__.__dict__["vault_storage_class"] = vault_storage_class
        __props__.__dict__["vault_type"] = vault_type
        return Vault(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of Vault. Defaults to an empty string.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="encryptType")
    def encrypt_type(self) -> pulumi.Output[str]:
        """
        Source Encryption Type，It is valid only when vault_type is `STANDARD` or `OTS_BACKUP`. Default value: `HBR_PRIVATE`. Valid values:
        - `HBR_PRIVATE`: HBR is fully hosted, uses the backup service's own encryption method.
        - `KMS`: Use Alibaba Cloud Kms to encryption.
        """
        return pulumi.get(self, "encrypt_type")

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> pulumi.Output[Optional[str]]:
        """
        The key id or alias name of Alibaba Cloud Kms. It is required and valid only when encrypt_type is `KMS`.
        """
        return pulumi.get(self, "kms_key_id")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The status of the Vault.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="vaultName")
    def vault_name(self) -> pulumi.Output[str]:
        """
        The name of Vault.
        """
        return pulumi.get(self, "vault_name")

    @property
    @pulumi.getter(name="vaultStorageClass")
    def vault_storage_class(self) -> pulumi.Output[str]:
        """
        The storage class of Vault. Valid values: `STANDARD`.
        """
        return pulumi.get(self, "vault_storage_class")

    @property
    @pulumi.getter(name="vaultType")
    def vault_type(self) -> pulumi.Output[str]:
        """
        The type of Vault. Valid values: `STANDARD`, `OTS_BACKUP`.
        """
        return pulumi.get(self, "vault_type")

