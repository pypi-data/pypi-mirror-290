# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['PolicyArgs', 'Policy']

@pulumi.input_type
class PolicyArgs:
    def __init__(__self__, *,
                 access_control_rules: pulumi.Input[str],
                 kms_instance_id: pulumi.Input[str],
                 permissions: pulumi.Input[Sequence[pulumi.Input[str]]],
                 policy_name: pulumi.Input[str],
                 resources: pulumi.Input[Sequence[pulumi.Input[str]]],
                 description: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Policy resource.
        :param pulumi.Input[str] access_control_rules: Network Rules in JSON struct.
        :param pulumi.Input[str] kms_instance_id: KMS instance .
        :param pulumi.Input[Sequence[pulumi.Input[str]]] permissions: Allowed permissions (RBAC)Optional values:"RbacPermission/Template/CryptoServiceKeyUser" and "RbacPermission/Template/CryptoServiceSecretUser".
        :param pulumi.Input[str] policy_name: Policy Name.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] resources: The resources that the permission policy allows to access.Use "key/${KeyId}" or "key/*"  to specify a key or all keys.Use "secret/${SecretName}" or "secret/*" to specify a secret or all secrets.
        :param pulumi.Input[str] description: Description.
        """
        pulumi.set(__self__, "access_control_rules", access_control_rules)
        pulumi.set(__self__, "kms_instance_id", kms_instance_id)
        pulumi.set(__self__, "permissions", permissions)
        pulumi.set(__self__, "policy_name", policy_name)
        pulumi.set(__self__, "resources", resources)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter(name="accessControlRules")
    def access_control_rules(self) -> pulumi.Input[str]:
        """
        Network Rules in JSON struct.
        """
        return pulumi.get(self, "access_control_rules")

    @access_control_rules.setter
    def access_control_rules(self, value: pulumi.Input[str]):
        pulumi.set(self, "access_control_rules", value)

    @property
    @pulumi.getter(name="kmsInstanceId")
    def kms_instance_id(self) -> pulumi.Input[str]:
        """
        KMS instance .
        """
        return pulumi.get(self, "kms_instance_id")

    @kms_instance_id.setter
    def kms_instance_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "kms_instance_id", value)

    @property
    @pulumi.getter
    def permissions(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        Allowed permissions (RBAC)Optional values:"RbacPermission/Template/CryptoServiceKeyUser" and "RbacPermission/Template/CryptoServiceSecretUser".
        """
        return pulumi.get(self, "permissions")

    @permissions.setter
    def permissions(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "permissions", value)

    @property
    @pulumi.getter(name="policyName")
    def policy_name(self) -> pulumi.Input[str]:
        """
        Policy Name.
        """
        return pulumi.get(self, "policy_name")

    @policy_name.setter
    def policy_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy_name", value)

    @property
    @pulumi.getter
    def resources(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The resources that the permission policy allows to access.Use "key/${KeyId}" or "key/*"  to specify a key or all keys.Use "secret/${SecretName}" or "secret/*" to specify a secret or all secrets.
        """
        return pulumi.get(self, "resources")

    @resources.setter
    def resources(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "resources", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


@pulumi.input_type
class _PolicyState:
    def __init__(__self__, *,
                 access_control_rules: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 kms_instance_id: Optional[pulumi.Input[str]] = None,
                 permissions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 policy_name: Optional[pulumi.Input[str]] = None,
                 resources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering Policy resources.
        :param pulumi.Input[str] access_control_rules: Network Rules in JSON struct.
        :param pulumi.Input[str] description: Description.
        :param pulumi.Input[str] kms_instance_id: KMS instance .
        :param pulumi.Input[Sequence[pulumi.Input[str]]] permissions: Allowed permissions (RBAC)Optional values:"RbacPermission/Template/CryptoServiceKeyUser" and "RbacPermission/Template/CryptoServiceSecretUser".
        :param pulumi.Input[str] policy_name: Policy Name.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] resources: The resources that the permission policy allows to access.Use "key/${KeyId}" or "key/*"  to specify a key or all keys.Use "secret/${SecretName}" or "secret/*" to specify a secret or all secrets.
        """
        if access_control_rules is not None:
            pulumi.set(__self__, "access_control_rules", access_control_rules)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if kms_instance_id is not None:
            pulumi.set(__self__, "kms_instance_id", kms_instance_id)
        if permissions is not None:
            pulumi.set(__self__, "permissions", permissions)
        if policy_name is not None:
            pulumi.set(__self__, "policy_name", policy_name)
        if resources is not None:
            pulumi.set(__self__, "resources", resources)

    @property
    @pulumi.getter(name="accessControlRules")
    def access_control_rules(self) -> Optional[pulumi.Input[str]]:
        """
        Network Rules in JSON struct.
        """
        return pulumi.get(self, "access_control_rules")

    @access_control_rules.setter
    def access_control_rules(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "access_control_rules", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="kmsInstanceId")
    def kms_instance_id(self) -> Optional[pulumi.Input[str]]:
        """
        KMS instance .
        """
        return pulumi.get(self, "kms_instance_id")

    @kms_instance_id.setter
    def kms_instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_instance_id", value)

    @property
    @pulumi.getter
    def permissions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Allowed permissions (RBAC)Optional values:"RbacPermission/Template/CryptoServiceKeyUser" and "RbacPermission/Template/CryptoServiceSecretUser".
        """
        return pulumi.get(self, "permissions")

    @permissions.setter
    def permissions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "permissions", value)

    @property
    @pulumi.getter(name="policyName")
    def policy_name(self) -> Optional[pulumi.Input[str]]:
        """
        Policy Name.
        """
        return pulumi.get(self, "policy_name")

    @policy_name.setter
    def policy_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_name", value)

    @property
    @pulumi.getter
    def resources(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The resources that the permission policy allows to access.Use "key/${KeyId}" or "key/*"  to specify a key or all keys.Use "secret/${SecretName}" or "secret/*" to specify a secret or all secrets.
        """
        return pulumi.get(self, "resources")

    @resources.setter
    def resources(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "resources", value)


class Policy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_control_rules: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 kms_instance_id: Optional[pulumi.Input[str]] = None,
                 permissions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 policy_name: Optional[pulumi.Input[str]] = None,
                 resources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides a KMS Policy resource. Permission policies which can be bound to the Application Access Points.

        For information about KMS Policy and how to use it, see [What is Policy](https://www.alibabacloud.com/help/zh/key-management-service/latest/api-createpolicy).

        > **NOTE:** Available since v1.210.0.

        ## Import

        KMS Policy can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:kms/policy:Policy example <id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] access_control_rules: Network Rules in JSON struct.
        :param pulumi.Input[str] description: Description.
        :param pulumi.Input[str] kms_instance_id: KMS instance .
        :param pulumi.Input[Sequence[pulumi.Input[str]]] permissions: Allowed permissions (RBAC)Optional values:"RbacPermission/Template/CryptoServiceKeyUser" and "RbacPermission/Template/CryptoServiceSecretUser".
        :param pulumi.Input[str] policy_name: Policy Name.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] resources: The resources that the permission policy allows to access.Use "key/${KeyId}" or "key/*"  to specify a key or all keys.Use "secret/${SecretName}" or "secret/*" to specify a secret or all secrets.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a KMS Policy resource. Permission policies which can be bound to the Application Access Points.

        For information about KMS Policy and how to use it, see [What is Policy](https://www.alibabacloud.com/help/zh/key-management-service/latest/api-createpolicy).

        > **NOTE:** Available since v1.210.0.

        ## Import

        KMS Policy can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:kms/policy:Policy example <id>
        ```

        :param str resource_name: The name of the resource.
        :param PolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_control_rules: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 kms_instance_id: Optional[pulumi.Input[str]] = None,
                 permissions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 policy_name: Optional[pulumi.Input[str]] = None,
                 resources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PolicyArgs.__new__(PolicyArgs)

            if access_control_rules is None and not opts.urn:
                raise TypeError("Missing required property 'access_control_rules'")
            __props__.__dict__["access_control_rules"] = access_control_rules
            __props__.__dict__["description"] = description
            if kms_instance_id is None and not opts.urn:
                raise TypeError("Missing required property 'kms_instance_id'")
            __props__.__dict__["kms_instance_id"] = kms_instance_id
            if permissions is None and not opts.urn:
                raise TypeError("Missing required property 'permissions'")
            __props__.__dict__["permissions"] = permissions
            if policy_name is None and not opts.urn:
                raise TypeError("Missing required property 'policy_name'")
            __props__.__dict__["policy_name"] = policy_name
            if resources is None and not opts.urn:
                raise TypeError("Missing required property 'resources'")
            __props__.__dict__["resources"] = resources
        super(Policy, __self__).__init__(
            'alicloud:kms/policy:Policy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            access_control_rules: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            kms_instance_id: Optional[pulumi.Input[str]] = None,
            permissions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            policy_name: Optional[pulumi.Input[str]] = None,
            resources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None) -> 'Policy':
        """
        Get an existing Policy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] access_control_rules: Network Rules in JSON struct.
        :param pulumi.Input[str] description: Description.
        :param pulumi.Input[str] kms_instance_id: KMS instance .
        :param pulumi.Input[Sequence[pulumi.Input[str]]] permissions: Allowed permissions (RBAC)Optional values:"RbacPermission/Template/CryptoServiceKeyUser" and "RbacPermission/Template/CryptoServiceSecretUser".
        :param pulumi.Input[str] policy_name: Policy Name.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] resources: The resources that the permission policy allows to access.Use "key/${KeyId}" or "key/*"  to specify a key or all keys.Use "secret/${SecretName}" or "secret/*" to specify a secret or all secrets.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PolicyState.__new__(_PolicyState)

        __props__.__dict__["access_control_rules"] = access_control_rules
        __props__.__dict__["description"] = description
        __props__.__dict__["kms_instance_id"] = kms_instance_id
        __props__.__dict__["permissions"] = permissions
        __props__.__dict__["policy_name"] = policy_name
        __props__.__dict__["resources"] = resources
        return Policy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accessControlRules")
    def access_control_rules(self) -> pulumi.Output[str]:
        """
        Network Rules in JSON struct.
        """
        return pulumi.get(self, "access_control_rules")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="kmsInstanceId")
    def kms_instance_id(self) -> pulumi.Output[str]:
        """
        KMS instance .
        """
        return pulumi.get(self, "kms_instance_id")

    @property
    @pulumi.getter
    def permissions(self) -> pulumi.Output[Sequence[str]]:
        """
        Allowed permissions (RBAC)Optional values:"RbacPermission/Template/CryptoServiceKeyUser" and "RbacPermission/Template/CryptoServiceSecretUser".
        """
        return pulumi.get(self, "permissions")

    @property
    @pulumi.getter(name="policyName")
    def policy_name(self) -> pulumi.Output[str]:
        """
        Policy Name.
        """
        return pulumi.get(self, "policy_name")

    @property
    @pulumi.getter
    def resources(self) -> pulumi.Output[Sequence[str]]:
        """
        The resources that the permission policy allows to access.Use "key/${KeyId}" or "key/*"  to specify a key or all keys.Use "secret/${SecretName}" or "secret/*" to specify a secret or all secrets.
        """
        return pulumi.get(self, "resources")

