# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'InstanceBindVpc',
    'GetAliasesAliasResult',
    'GetKeyVersionsVersionResult',
    'GetKeysKeyResult',
    'GetSecretVersionsVersionResult',
    'GetSecretsSecretResult',
]

@pulumi.output_type
class InstanceBindVpc(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "regionId":
            suggest = "region_id"
        elif key == "vpcId":
            suggest = "vpc_id"
        elif key == "vpcOwnerId":
            suggest = "vpc_owner_id"
        elif key == "vswitchId":
            suggest = "vswitch_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in InstanceBindVpc. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        InstanceBindVpc.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        InstanceBindVpc.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 region_id: Optional[str] = None,
                 vpc_id: Optional[str] = None,
                 vpc_owner_id: Optional[int] = None,
                 vswitch_id: Optional[str] = None):
        """
        :param str region_id: region id.
        :param str vpc_id: VPC ID.
        :param int vpc_owner_id: VPC owner root user ID.
        :param str vswitch_id: vswitch id.
        """
        if region_id is not None:
            pulumi.set(__self__, "region_id", region_id)
        if vpc_id is not None:
            pulumi.set(__self__, "vpc_id", vpc_id)
        if vpc_owner_id is not None:
            pulumi.set(__self__, "vpc_owner_id", vpc_owner_id)
        if vswitch_id is not None:
            pulumi.set(__self__, "vswitch_id", vswitch_id)

    @property
    @pulumi.getter(name="regionId")
    def region_id(self) -> Optional[str]:
        """
        region id.
        """
        return pulumi.get(self, "region_id")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> Optional[str]:
        """
        VPC ID.
        """
        return pulumi.get(self, "vpc_id")

    @property
    @pulumi.getter(name="vpcOwnerId")
    def vpc_owner_id(self) -> Optional[int]:
        """
        VPC owner root user ID.
        """
        return pulumi.get(self, "vpc_owner_id")

    @property
    @pulumi.getter(name="vswitchId")
    def vswitch_id(self) -> Optional[str]:
        """
        vswitch id.
        """
        return pulumi.get(self, "vswitch_id")


@pulumi.output_type
class GetAliasesAliasResult(dict):
    def __init__(__self__, *,
                 alias_name: str,
                 id: str,
                 key_id: str):
        """
        :param str alias_name: The unique identifier of the alias.
        :param str id: ID of the alias. The value is same as KMS alias_name.
        :param str key_id: ID of the key.
        """
        pulumi.set(__self__, "alias_name", alias_name)
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "key_id", key_id)

    @property
    @pulumi.getter(name="aliasName")
    def alias_name(self) -> str:
        """
        The unique identifier of the alias.
        """
        return pulumi.get(self, "alias_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        ID of the alias. The value is same as KMS alias_name.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="keyId")
    def key_id(self) -> str:
        """
        ID of the key.
        """
        return pulumi.get(self, "key_id")


@pulumi.output_type
class GetKeyVersionsVersionResult(dict):
    def __init__(__self__, *,
                 create_time: str,
                 creation_date: str,
                 id: str,
                 key_id: str,
                 key_version_id: str):
        """
        :param str create_time: Date and time when the key version was created (UTC time).
        :param str creation_date: (Removed from v1.124.4) It has been removed and using `create_time` instead.
        :param str id: ID of the KMS KeyVersion resource.
        :param str key_id: The id of kms key.
        :param str key_version_id: ID of the key version.
        """
        pulumi.set(__self__, "create_time", create_time)
        pulumi.set(__self__, "creation_date", creation_date)
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "key_id", key_id)
        pulumi.set(__self__, "key_version_id", key_version_id)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> str:
        """
        Date and time when the key version was created (UTC time).
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="creationDate")
    def creation_date(self) -> str:
        """
        (Removed from v1.124.4) It has been removed and using `create_time` instead.
        """
        return pulumi.get(self, "creation_date")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        ID of the KMS KeyVersion resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="keyId")
    def key_id(self) -> str:
        """
        The id of kms key.
        """
        return pulumi.get(self, "key_id")

    @property
    @pulumi.getter(name="keyVersionId")
    def key_version_id(self) -> str:
        """
        ID of the key version.
        """
        return pulumi.get(self, "key_version_id")


@pulumi.output_type
class GetKeysKeyResult(dict):
    def __init__(__self__, *,
                 arn: str,
                 automatic_rotation: str,
                 creation_date: str,
                 creator: str,
                 delete_date: str,
                 description: str,
                 id: str,
                 key_id: str,
                 key_spec: str,
                 key_usage: str,
                 last_rotation_date: str,
                 material_expire_time: str,
                 next_rotation_date: str,
                 origin: str,
                 primary_key_version: str,
                 protection_level: str,
                 rotation_interval: str,
                 status: str):
        """
        :param str arn: The Alibaba Cloud Resource Name (ARN) of the key.
        :param str automatic_rotation: (Available in 1.123.1+) Specifies whether to enable automatic key rotation.
        :param str creation_date: Creation date of key.
        :param str creator: The owner of the key.
        :param str delete_date: Deletion date of key.
        :param str description: Description of the key.
        :param str id: ID of the key.
        :param str key_id: (Available in 1.123.1+)  ID of the key.
        :param str key_spec: (Available in 1.123.1+)  The type of the CMK.
        :param str key_usage: (Available in 1.123.1+)  The usage of CMK.
        :param str last_rotation_date: (Available in 1.123.1+)  The date and time the last rotation was performed.
        :param str material_expire_time: (Available in 1.123.1+)  The time and date the key material for the CMK expires.
        :param str next_rotation_date: (Available in 1.123.1+)  The time the next rotation is scheduled for execution.
        :param str origin: (Available in 1.123.1+)  The source of the key material for the CMK.
        :param str primary_key_version: (Available in 1.123.1+)  The ID of the current primary key version of the symmetric CMK.
        :param str protection_level: (Available in 1.123.1+)  The protection level of the CMK.
        :param str rotation_interval: (Available in 1.123.1+)  The period of automatic key rotation.
        :param str status: Filter the results by status of the KMS keys. Valid values: `Enabled`, `Disabled`, `PendingDeletion`.
        """
        pulumi.set(__self__, "arn", arn)
        pulumi.set(__self__, "automatic_rotation", automatic_rotation)
        pulumi.set(__self__, "creation_date", creation_date)
        pulumi.set(__self__, "creator", creator)
        pulumi.set(__self__, "delete_date", delete_date)
        pulumi.set(__self__, "description", description)
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "key_id", key_id)
        pulumi.set(__self__, "key_spec", key_spec)
        pulumi.set(__self__, "key_usage", key_usage)
        pulumi.set(__self__, "last_rotation_date", last_rotation_date)
        pulumi.set(__self__, "material_expire_time", material_expire_time)
        pulumi.set(__self__, "next_rotation_date", next_rotation_date)
        pulumi.set(__self__, "origin", origin)
        pulumi.set(__self__, "primary_key_version", primary_key_version)
        pulumi.set(__self__, "protection_level", protection_level)
        pulumi.set(__self__, "rotation_interval", rotation_interval)
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        The Alibaba Cloud Resource Name (ARN) of the key.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="automaticRotation")
    def automatic_rotation(self) -> str:
        """
        (Available in 1.123.1+) Specifies whether to enable automatic key rotation.
        """
        return pulumi.get(self, "automatic_rotation")

    @property
    @pulumi.getter(name="creationDate")
    def creation_date(self) -> str:
        """
        Creation date of key.
        """
        return pulumi.get(self, "creation_date")

    @property
    @pulumi.getter
    def creator(self) -> str:
        """
        The owner of the key.
        """
        return pulumi.get(self, "creator")

    @property
    @pulumi.getter(name="deleteDate")
    def delete_date(self) -> str:
        """
        Deletion date of key.
        """
        return pulumi.get(self, "delete_date")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description of the key.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        ID of the key.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="keyId")
    def key_id(self) -> str:
        """
        (Available in 1.123.1+)  ID of the key.
        """
        return pulumi.get(self, "key_id")

    @property
    @pulumi.getter(name="keySpec")
    def key_spec(self) -> str:
        """
        (Available in 1.123.1+)  The type of the CMK.
        """
        return pulumi.get(self, "key_spec")

    @property
    @pulumi.getter(name="keyUsage")
    def key_usage(self) -> str:
        """
        (Available in 1.123.1+)  The usage of CMK.
        """
        return pulumi.get(self, "key_usage")

    @property
    @pulumi.getter(name="lastRotationDate")
    def last_rotation_date(self) -> str:
        """
        (Available in 1.123.1+)  The date and time the last rotation was performed.
        """
        return pulumi.get(self, "last_rotation_date")

    @property
    @pulumi.getter(name="materialExpireTime")
    def material_expire_time(self) -> str:
        """
        (Available in 1.123.1+)  The time and date the key material for the CMK expires.
        """
        return pulumi.get(self, "material_expire_time")

    @property
    @pulumi.getter(name="nextRotationDate")
    def next_rotation_date(self) -> str:
        """
        (Available in 1.123.1+)  The time the next rotation is scheduled for execution.
        """
        return pulumi.get(self, "next_rotation_date")

    @property
    @pulumi.getter
    def origin(self) -> str:
        """
        (Available in 1.123.1+)  The source of the key material for the CMK.
        """
        return pulumi.get(self, "origin")

    @property
    @pulumi.getter(name="primaryKeyVersion")
    def primary_key_version(self) -> str:
        """
        (Available in 1.123.1+)  The ID of the current primary key version of the symmetric CMK.
        """
        return pulumi.get(self, "primary_key_version")

    @property
    @pulumi.getter(name="protectionLevel")
    def protection_level(self) -> str:
        """
        (Available in 1.123.1+)  The protection level of the CMK.
        """
        return pulumi.get(self, "protection_level")

    @property
    @pulumi.getter(name="rotationInterval")
    def rotation_interval(self) -> str:
        """
        (Available in 1.123.1+)  The period of automatic key rotation.
        """
        return pulumi.get(self, "rotation_interval")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Filter the results by status of the KMS keys. Valid values: `Enabled`, `Disabled`, `PendingDeletion`.
        """
        return pulumi.get(self, "status")


@pulumi.output_type
class GetSecretVersionsVersionResult(dict):
    def __init__(__self__, *,
                 secret_data: str,
                 secret_data_type: str,
                 secret_name: str,
                 version_id: str,
                 version_stages: Sequence[str]):
        """
        :param str secret_data: The secret value. Secrets Manager decrypts the stored secret value in ciphertext and returns it. (Returned when `enable_details` is true).
        :param str secret_data_type: The type of the secret value. (Returned when `enable_details` is true).
        :param str secret_name: The name of the secret.
        :param str version_id: The version number of the secret value.
        :param Sequence[str] version_stages: Stage labels that mark the secret version.
        """
        pulumi.set(__self__, "secret_data", secret_data)
        pulumi.set(__self__, "secret_data_type", secret_data_type)
        pulumi.set(__self__, "secret_name", secret_name)
        pulumi.set(__self__, "version_id", version_id)
        pulumi.set(__self__, "version_stages", version_stages)

    @property
    @pulumi.getter(name="secretData")
    def secret_data(self) -> str:
        """
        The secret value. Secrets Manager decrypts the stored secret value in ciphertext and returns it. (Returned when `enable_details` is true).
        """
        return pulumi.get(self, "secret_data")

    @property
    @pulumi.getter(name="secretDataType")
    def secret_data_type(self) -> str:
        """
        The type of the secret value. (Returned when `enable_details` is true).
        """
        return pulumi.get(self, "secret_data_type")

    @property
    @pulumi.getter(name="secretName")
    def secret_name(self) -> str:
        """
        The name of the secret.
        """
        return pulumi.get(self, "secret_name")

    @property
    @pulumi.getter(name="versionId")
    def version_id(self) -> str:
        """
        The version number of the secret value.
        """
        return pulumi.get(self, "version_id")

    @property
    @pulumi.getter(name="versionStages")
    def version_stages(self) -> Sequence[str]:
        """
        Stage labels that mark the secret version.
        """
        return pulumi.get(self, "version_stages")


@pulumi.output_type
class GetSecretsSecretResult(dict):
    def __init__(__self__, *,
                 arn: str,
                 description: str,
                 encryption_key_id: str,
                 id: str,
                 planned_delete_time: str,
                 secret_data: str,
                 secret_data_type: str,
                 secret_name: str,
                 secret_type: str,
                 tags: Mapping[str, Any],
                 version_id: str,
                 version_stages: Sequence[str]):
        """
        :param str arn: (Available in 1.124.0+) A mapping of tags to assign to the resource.
        :param str description: (Available in 1.124.0+)  The description of the secret.
        :param str encryption_key_id: (Available in 1.124.0+)  The ID of the KMS CMK that is used to encrypt the secret value.
        :param str id: ID of the Kms Secret. The value is same as KMS secret_name.
        :param str planned_delete_time: Schedule deletion time.
        :param str secret_data: (Available in 1.124.0+)  The value of the secret that you want to create.
        :param str secret_data_type: (Available in 1.124.0+)  The type of the secret data value.
        :param str secret_name: Name of the KMS Secret.
        :param str secret_type: (Available in 1.124.0+)  The type of the secret.
        :param Mapping[str, Any] tags: A mapping of tags to assign to the resource.
        :param str version_id: (Available in 1.124.0+)  The version number of the initial version.
        :param Sequence[str] version_stages: (Available in 1.124.0+)  The stage labels that mark the new secret version.
        """
        pulumi.set(__self__, "arn", arn)
        pulumi.set(__self__, "description", description)
        pulumi.set(__self__, "encryption_key_id", encryption_key_id)
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "planned_delete_time", planned_delete_time)
        pulumi.set(__self__, "secret_data", secret_data)
        pulumi.set(__self__, "secret_data_type", secret_data_type)
        pulumi.set(__self__, "secret_name", secret_name)
        pulumi.set(__self__, "secret_type", secret_type)
        pulumi.set(__self__, "tags", tags)
        pulumi.set(__self__, "version_id", version_id)
        pulumi.set(__self__, "version_stages", version_stages)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        (Available in 1.124.0+) A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        (Available in 1.124.0+)  The description of the secret.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="encryptionKeyId")
    def encryption_key_id(self) -> str:
        """
        (Available in 1.124.0+)  The ID of the KMS CMK that is used to encrypt the secret value.
        """
        return pulumi.get(self, "encryption_key_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        ID of the Kms Secret. The value is same as KMS secret_name.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="plannedDeleteTime")
    def planned_delete_time(self) -> str:
        """
        Schedule deletion time.
        """
        return pulumi.get(self, "planned_delete_time")

    @property
    @pulumi.getter(name="secretData")
    def secret_data(self) -> str:
        """
        (Available in 1.124.0+)  The value of the secret that you want to create.
        """
        return pulumi.get(self, "secret_data")

    @property
    @pulumi.getter(name="secretDataType")
    def secret_data_type(self) -> str:
        """
        (Available in 1.124.0+)  The type of the secret data value.
        """
        return pulumi.get(self, "secret_data_type")

    @property
    @pulumi.getter(name="secretName")
    def secret_name(self) -> str:
        """
        Name of the KMS Secret.
        """
        return pulumi.get(self, "secret_name")

    @property
    @pulumi.getter(name="secretType")
    def secret_type(self) -> str:
        """
        (Available in 1.124.0+)  The type of the secret.
        """
        return pulumi.get(self, "secret_type")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, Any]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="versionId")
    def version_id(self) -> str:
        """
        (Available in 1.124.0+)  The version number of the initial version.
        """
        return pulumi.get(self, "version_id")

    @property
    @pulumi.getter(name="versionStages")
    def version_stages(self) -> Sequence[str]:
        """
        (Available in 1.124.0+)  The stage labels that mark the new secret version.
        """
        return pulumi.get(self, "version_stages")


