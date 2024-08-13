# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['EnterpriseProxyAccessArgs', 'EnterpriseProxyAccess']

@pulumi.input_type
class EnterpriseProxyAccessArgs:
    def __init__(__self__, *,
                 proxy_id: pulumi.Input[str],
                 user_id: pulumi.Input[str],
                 indep_account: Optional[pulumi.Input[str]] = None,
                 indep_password: Optional[pulumi.Input[str]] = None,
                 proxy_access_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a EnterpriseProxyAccess resource.
        :param pulumi.Input[str] proxy_id: The ID of the security agent.
        :param pulumi.Input[str] user_id: The user ID.
        :param pulumi.Input[str] indep_account: Database account.
        :param pulumi.Input[str] indep_password: Database password.
        :param pulumi.Input[str] proxy_access_id: Security Protection authorization ID. After the target user is authorized by the security protection agent, the system automatically generates a security protection authorization ID, which is globally unique.
        """
        pulumi.set(__self__, "proxy_id", proxy_id)
        pulumi.set(__self__, "user_id", user_id)
        if indep_account is not None:
            pulumi.set(__self__, "indep_account", indep_account)
        if indep_password is not None:
            pulumi.set(__self__, "indep_password", indep_password)
        if proxy_access_id is not None:
            pulumi.set(__self__, "proxy_access_id", proxy_access_id)

    @property
    @pulumi.getter(name="proxyId")
    def proxy_id(self) -> pulumi.Input[str]:
        """
        The ID of the security agent.
        """
        return pulumi.get(self, "proxy_id")

    @proxy_id.setter
    def proxy_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "proxy_id", value)

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> pulumi.Input[str]:
        """
        The user ID.
        """
        return pulumi.get(self, "user_id")

    @user_id.setter
    def user_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "user_id", value)

    @property
    @pulumi.getter(name="indepAccount")
    def indep_account(self) -> Optional[pulumi.Input[str]]:
        """
        Database account.
        """
        return pulumi.get(self, "indep_account")

    @indep_account.setter
    def indep_account(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "indep_account", value)

    @property
    @pulumi.getter(name="indepPassword")
    def indep_password(self) -> Optional[pulumi.Input[str]]:
        """
        Database password.
        """
        return pulumi.get(self, "indep_password")

    @indep_password.setter
    def indep_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "indep_password", value)

    @property
    @pulumi.getter(name="proxyAccessId")
    def proxy_access_id(self) -> Optional[pulumi.Input[str]]:
        """
        Security Protection authorization ID. After the target user is authorized by the security protection agent, the system automatically generates a security protection authorization ID, which is globally unique.
        """
        return pulumi.get(self, "proxy_access_id")

    @proxy_access_id.setter
    def proxy_access_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "proxy_access_id", value)


@pulumi.input_type
class _EnterpriseProxyAccessState:
    def __init__(__self__, *,
                 access_id: Optional[pulumi.Input[str]] = None,
                 access_secret: Optional[pulumi.Input[str]] = None,
                 create_time: Optional[pulumi.Input[str]] = None,
                 indep_account: Optional[pulumi.Input[str]] = None,
                 indep_password: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 origin_info: Optional[pulumi.Input[str]] = None,
                 proxy_access_id: Optional[pulumi.Input[str]] = None,
                 proxy_id: Optional[pulumi.Input[str]] = None,
                 user_id: Optional[pulumi.Input[str]] = None,
                 user_name: Optional[pulumi.Input[str]] = None,
                 user_uid: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering EnterpriseProxyAccess resources.
        :param pulumi.Input[str] access_id: The authorized account of the security agent.
        :param pulumi.Input[str] access_secret: Secure access agent authorization password.
        :param pulumi.Input[str] indep_account: Database account.
        :param pulumi.Input[str] indep_password: Database password.
        :param pulumi.Input[str] instance_id: The ID of the instance.
        :param pulumi.Input[str] origin_info: The source information of the security access agent permission is enabled, and the return value is as follows:
               * **Owner Authorization**: The UID of the owner in parentheses.
               * **Work Order Authorization**: The ticket number in parentheses is the number of the user to apply for permission.
        :param pulumi.Input[str] proxy_access_id: Security Protection authorization ID. After the target user is authorized by the security protection agent, the system automatically generates a security protection authorization ID, which is globally unique.
        :param pulumi.Input[str] proxy_id: The ID of the security agent.
        :param pulumi.Input[str] user_id: The user ID.
        :param pulumi.Input[str] user_name: User nickname.
        :param pulumi.Input[str] user_uid: User UID.
        """
        if access_id is not None:
            pulumi.set(__self__, "access_id", access_id)
        if access_secret is not None:
            pulumi.set(__self__, "access_secret", access_secret)
        if create_time is not None:
            pulumi.set(__self__, "create_time", create_time)
        if indep_account is not None:
            pulumi.set(__self__, "indep_account", indep_account)
        if indep_password is not None:
            pulumi.set(__self__, "indep_password", indep_password)
        if instance_id is not None:
            pulumi.set(__self__, "instance_id", instance_id)
        if origin_info is not None:
            pulumi.set(__self__, "origin_info", origin_info)
        if proxy_access_id is not None:
            pulumi.set(__self__, "proxy_access_id", proxy_access_id)
        if proxy_id is not None:
            pulumi.set(__self__, "proxy_id", proxy_id)
        if user_id is not None:
            pulumi.set(__self__, "user_id", user_id)
        if user_name is not None:
            pulumi.set(__self__, "user_name", user_name)
        if user_uid is not None:
            pulumi.set(__self__, "user_uid", user_uid)

    @property
    @pulumi.getter(name="accessId")
    def access_id(self) -> Optional[pulumi.Input[str]]:
        """
        The authorized account of the security agent.
        """
        return pulumi.get(self, "access_id")

    @access_id.setter
    def access_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "access_id", value)

    @property
    @pulumi.getter(name="accessSecret")
    def access_secret(self) -> Optional[pulumi.Input[str]]:
        """
        Secure access agent authorization password.
        """
        return pulumi.get(self, "access_secret")

    @access_secret.setter
    def access_secret(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "access_secret", value)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "create_time")

    @create_time.setter
    def create_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create_time", value)

    @property
    @pulumi.getter(name="indepAccount")
    def indep_account(self) -> Optional[pulumi.Input[str]]:
        """
        Database account.
        """
        return pulumi.get(self, "indep_account")

    @indep_account.setter
    def indep_account(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "indep_account", value)

    @property
    @pulumi.getter(name="indepPassword")
    def indep_password(self) -> Optional[pulumi.Input[str]]:
        """
        Database password.
        """
        return pulumi.get(self, "indep_password")

    @indep_password.setter
    def indep_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "indep_password", value)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the instance.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter(name="originInfo")
    def origin_info(self) -> Optional[pulumi.Input[str]]:
        """
        The source information of the security access agent permission is enabled, and the return value is as follows:
        * **Owner Authorization**: The UID of the owner in parentheses.
        * **Work Order Authorization**: The ticket number in parentheses is the number of the user to apply for permission.
        """
        return pulumi.get(self, "origin_info")

    @origin_info.setter
    def origin_info(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "origin_info", value)

    @property
    @pulumi.getter(name="proxyAccessId")
    def proxy_access_id(self) -> Optional[pulumi.Input[str]]:
        """
        Security Protection authorization ID. After the target user is authorized by the security protection agent, the system automatically generates a security protection authorization ID, which is globally unique.
        """
        return pulumi.get(self, "proxy_access_id")

    @proxy_access_id.setter
    def proxy_access_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "proxy_access_id", value)

    @property
    @pulumi.getter(name="proxyId")
    def proxy_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the security agent.
        """
        return pulumi.get(self, "proxy_id")

    @proxy_id.setter
    def proxy_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "proxy_id", value)

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> Optional[pulumi.Input[str]]:
        """
        The user ID.
        """
        return pulumi.get(self, "user_id")

    @user_id.setter
    def user_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_id", value)

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> Optional[pulumi.Input[str]]:
        """
        User nickname.
        """
        return pulumi.get(self, "user_name")

    @user_name.setter
    def user_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_name", value)

    @property
    @pulumi.getter(name="userUid")
    def user_uid(self) -> Optional[pulumi.Input[str]]:
        """
        User UID.
        """
        return pulumi.get(self, "user_uid")

    @user_uid.setter
    def user_uid(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_uid", value)


class EnterpriseProxyAccess(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 indep_account: Optional[pulumi.Input[str]] = None,
                 indep_password: Optional[pulumi.Input[str]] = None,
                 proxy_access_id: Optional[pulumi.Input[str]] = None,
                 proxy_id: Optional[pulumi.Input[str]] = None,
                 user_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a DMS Enterprise Proxy Access resource.

        For information about DMS Enterprise Proxy Access and how to use it, see [What is Proxy Access](https://next.api.alibabacloud.com/document/dms-enterprise/2018-11-01/CreateProxyAccess).

        > **NOTE:** Available since v1.195.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        dms_enterprise_users_ds = alicloud.dms.get_enterprise_users(role="USER",
            status="NORMAL")
        ids = alicloud.dms.get_enterprise_proxies()
        default = alicloud.dms.EnterpriseProxyAccess("default",
            proxy_id=ids.proxies[0].id,
            user_id=dms_enterprise_users_ds.users[0].user_id)
        ```

        ## Import

        DMS Enterprise Proxy Access can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:dms/enterpriseProxyAccess:EnterpriseProxyAccess example <id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] indep_account: Database account.
        :param pulumi.Input[str] indep_password: Database password.
        :param pulumi.Input[str] proxy_access_id: Security Protection authorization ID. After the target user is authorized by the security protection agent, the system automatically generates a security protection authorization ID, which is globally unique.
        :param pulumi.Input[str] proxy_id: The ID of the security agent.
        :param pulumi.Input[str] user_id: The user ID.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EnterpriseProxyAccessArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a DMS Enterprise Proxy Access resource.

        For information about DMS Enterprise Proxy Access and how to use it, see [What is Proxy Access](https://next.api.alibabacloud.com/document/dms-enterprise/2018-11-01/CreateProxyAccess).

        > **NOTE:** Available since v1.195.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        dms_enterprise_users_ds = alicloud.dms.get_enterprise_users(role="USER",
            status="NORMAL")
        ids = alicloud.dms.get_enterprise_proxies()
        default = alicloud.dms.EnterpriseProxyAccess("default",
            proxy_id=ids.proxies[0].id,
            user_id=dms_enterprise_users_ds.users[0].user_id)
        ```

        ## Import

        DMS Enterprise Proxy Access can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:dms/enterpriseProxyAccess:EnterpriseProxyAccess example <id>
        ```

        :param str resource_name: The name of the resource.
        :param EnterpriseProxyAccessArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EnterpriseProxyAccessArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 indep_account: Optional[pulumi.Input[str]] = None,
                 indep_password: Optional[pulumi.Input[str]] = None,
                 proxy_access_id: Optional[pulumi.Input[str]] = None,
                 proxy_id: Optional[pulumi.Input[str]] = None,
                 user_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EnterpriseProxyAccessArgs.__new__(EnterpriseProxyAccessArgs)

            __props__.__dict__["indep_account"] = indep_account
            __props__.__dict__["indep_password"] = None if indep_password is None else pulumi.Output.secret(indep_password)
            __props__.__dict__["proxy_access_id"] = proxy_access_id
            if proxy_id is None and not opts.urn:
                raise TypeError("Missing required property 'proxy_id'")
            __props__.__dict__["proxy_id"] = proxy_id
            if user_id is None and not opts.urn:
                raise TypeError("Missing required property 'user_id'")
            __props__.__dict__["user_id"] = user_id
            __props__.__dict__["access_id"] = None
            __props__.__dict__["access_secret"] = None
            __props__.__dict__["create_time"] = None
            __props__.__dict__["instance_id"] = None
            __props__.__dict__["origin_info"] = None
            __props__.__dict__["user_name"] = None
            __props__.__dict__["user_uid"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["accessSecret", "indepPassword"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(EnterpriseProxyAccess, __self__).__init__(
            'alicloud:dms/enterpriseProxyAccess:EnterpriseProxyAccess',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            access_id: Optional[pulumi.Input[str]] = None,
            access_secret: Optional[pulumi.Input[str]] = None,
            create_time: Optional[pulumi.Input[str]] = None,
            indep_account: Optional[pulumi.Input[str]] = None,
            indep_password: Optional[pulumi.Input[str]] = None,
            instance_id: Optional[pulumi.Input[str]] = None,
            origin_info: Optional[pulumi.Input[str]] = None,
            proxy_access_id: Optional[pulumi.Input[str]] = None,
            proxy_id: Optional[pulumi.Input[str]] = None,
            user_id: Optional[pulumi.Input[str]] = None,
            user_name: Optional[pulumi.Input[str]] = None,
            user_uid: Optional[pulumi.Input[str]] = None) -> 'EnterpriseProxyAccess':
        """
        Get an existing EnterpriseProxyAccess resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] access_id: The authorized account of the security agent.
        :param pulumi.Input[str] access_secret: Secure access agent authorization password.
        :param pulumi.Input[str] indep_account: Database account.
        :param pulumi.Input[str] indep_password: Database password.
        :param pulumi.Input[str] instance_id: The ID of the instance.
        :param pulumi.Input[str] origin_info: The source information of the security access agent permission is enabled, and the return value is as follows:
               * **Owner Authorization**: The UID of the owner in parentheses.
               * **Work Order Authorization**: The ticket number in parentheses is the number of the user to apply for permission.
        :param pulumi.Input[str] proxy_access_id: Security Protection authorization ID. After the target user is authorized by the security protection agent, the system automatically generates a security protection authorization ID, which is globally unique.
        :param pulumi.Input[str] proxy_id: The ID of the security agent.
        :param pulumi.Input[str] user_id: The user ID.
        :param pulumi.Input[str] user_name: User nickname.
        :param pulumi.Input[str] user_uid: User UID.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _EnterpriseProxyAccessState.__new__(_EnterpriseProxyAccessState)

        __props__.__dict__["access_id"] = access_id
        __props__.__dict__["access_secret"] = access_secret
        __props__.__dict__["create_time"] = create_time
        __props__.__dict__["indep_account"] = indep_account
        __props__.__dict__["indep_password"] = indep_password
        __props__.__dict__["instance_id"] = instance_id
        __props__.__dict__["origin_info"] = origin_info
        __props__.__dict__["proxy_access_id"] = proxy_access_id
        __props__.__dict__["proxy_id"] = proxy_id
        __props__.__dict__["user_id"] = user_id
        __props__.__dict__["user_name"] = user_name
        __props__.__dict__["user_uid"] = user_uid
        return EnterpriseProxyAccess(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accessId")
    def access_id(self) -> pulumi.Output[str]:
        """
        The authorized account of the security agent.
        """
        return pulumi.get(self, "access_id")

    @property
    @pulumi.getter(name="accessSecret")
    def access_secret(self) -> pulumi.Output[str]:
        """
        Secure access agent authorization password.
        """
        return pulumi.get(self, "access_secret")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="indepAccount")
    def indep_account(self) -> pulumi.Output[Optional[str]]:
        """
        Database account.
        """
        return pulumi.get(self, "indep_account")

    @property
    @pulumi.getter(name="indepPassword")
    def indep_password(self) -> pulumi.Output[Optional[str]]:
        """
        Database password.
        """
        return pulumi.get(self, "indep_password")

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Output[str]:
        """
        The ID of the instance.
        """
        return pulumi.get(self, "instance_id")

    @property
    @pulumi.getter(name="originInfo")
    def origin_info(self) -> pulumi.Output[str]:
        """
        The source information of the security access agent permission is enabled, and the return value is as follows:
        * **Owner Authorization**: The UID of the owner in parentheses.
        * **Work Order Authorization**: The ticket number in parentheses is the number of the user to apply for permission.
        """
        return pulumi.get(self, "origin_info")

    @property
    @pulumi.getter(name="proxyAccessId")
    def proxy_access_id(self) -> pulumi.Output[str]:
        """
        Security Protection authorization ID. After the target user is authorized by the security protection agent, the system automatically generates a security protection authorization ID, which is globally unique.
        """
        return pulumi.get(self, "proxy_access_id")

    @property
    @pulumi.getter(name="proxyId")
    def proxy_id(self) -> pulumi.Output[str]:
        """
        The ID of the security agent.
        """
        return pulumi.get(self, "proxy_id")

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> pulumi.Output[str]:
        """
        The user ID.
        """
        return pulumi.get(self, "user_id")

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> pulumi.Output[str]:
        """
        User nickname.
        """
        return pulumi.get(self, "user_name")

    @property
    @pulumi.getter(name="userUid")
    def user_uid(self) -> pulumi.Output[str]:
        """
        User UID.
        """
        return pulumi.get(self, "user_uid")

