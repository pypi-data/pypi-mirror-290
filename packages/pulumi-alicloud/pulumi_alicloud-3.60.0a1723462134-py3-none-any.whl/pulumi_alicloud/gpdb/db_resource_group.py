# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['DbResourceGroupArgs', 'DbResourceGroup']

@pulumi.input_type
class DbResourceGroupArgs:
    def __init__(__self__, *,
                 db_instance_id: pulumi.Input[str],
                 resource_group_config: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str]):
        """
        The set of arguments for constructing a DbResourceGroup resource.
        :param pulumi.Input[str] db_instance_id: The instance ID.> You can call the DescribeDBInstances operation to view the instance IDs of all AnalyticDB PostgreSQL instances in the target region.
        :param pulumi.Input[str] resource_group_config: Resource group configuration.
        :param pulumi.Input[str] resource_group_name: Resource group name.
        """
        pulumi.set(__self__, "db_instance_id", db_instance_id)
        pulumi.set(__self__, "resource_group_config", resource_group_config)
        pulumi.set(__self__, "resource_group_name", resource_group_name)

    @property
    @pulumi.getter(name="dbInstanceId")
    def db_instance_id(self) -> pulumi.Input[str]:
        """
        The instance ID.> You can call the DescribeDBInstances operation to view the instance IDs of all AnalyticDB PostgreSQL instances in the target region.
        """
        return pulumi.get(self, "db_instance_id")

    @db_instance_id.setter
    def db_instance_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "db_instance_id", value)

    @property
    @pulumi.getter(name="resourceGroupConfig")
    def resource_group_config(self) -> pulumi.Input[str]:
        """
        Resource group configuration.
        """
        return pulumi.get(self, "resource_group_config")

    @resource_group_config.setter
    def resource_group_config(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_config", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Resource group name.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)


@pulumi.input_type
class _DbResourceGroupState:
    def __init__(__self__, *,
                 db_instance_id: Optional[pulumi.Input[str]] = None,
                 resource_group_config: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering DbResourceGroup resources.
        :param pulumi.Input[str] db_instance_id: The instance ID.> You can call the DescribeDBInstances operation to view the instance IDs of all AnalyticDB PostgreSQL instances in the target region.
        :param pulumi.Input[str] resource_group_config: Resource group configuration.
        :param pulumi.Input[str] resource_group_name: Resource group name.
        """
        if db_instance_id is not None:
            pulumi.set(__self__, "db_instance_id", db_instance_id)
        if resource_group_config is not None:
            pulumi.set(__self__, "resource_group_config", resource_group_config)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)

    @property
    @pulumi.getter(name="dbInstanceId")
    def db_instance_id(self) -> Optional[pulumi.Input[str]]:
        """
        The instance ID.> You can call the DescribeDBInstances operation to view the instance IDs of all AnalyticDB PostgreSQL instances in the target region.
        """
        return pulumi.get(self, "db_instance_id")

    @db_instance_id.setter
    def db_instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "db_instance_id", value)

    @property
    @pulumi.getter(name="resourceGroupConfig")
    def resource_group_config(self) -> Optional[pulumi.Input[str]]:
        """
        Resource group configuration.
        """
        return pulumi.get(self, "resource_group_config")

    @resource_group_config.setter
    def resource_group_config(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_config", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        Resource group name.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)


class DbResourceGroup(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 db_instance_id: Optional[pulumi.Input[str]] = None,
                 resource_group_config: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Gpdb Db Resource Group resource.

        For information about Gpdb Db Resource Group and how to use it, see [What is Db Resource Group](https://www.alibabacloud.com/help/en/).

        > **NOTE:** Available since v1.225.0.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import json
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "terraform-example"
        default = alicloud.get_zones(available_resource_creation="VSwitch")
        default_zc8_rd9 = alicloud.vpc.Network("defaultZc8RD9", cidr_block="192.168.0.0/16")
        default_rv5_u_xt = alicloud.vpc.Switch("defaultRv5UXt",
            vpc_id=default_zc8_rd9.id,
            zone_id=default.zones[0].id,
            cidr_block="192.168.1.0/24")
        default_jxw_sl_w = alicloud.gpdb.Instance("defaultJXWSlW",
            instance_spec="2C8G",
            seg_node_num=2,
            seg_storage_type="cloud_essd",
            instance_network_type="VPC",
            db_instance_category="Basic",
            engine="gpdb",
            resource_management_mode="resourceGroup",
            payment_type="PayAsYouGo",
            ssl_enabled=0,
            engine_version="6.0",
            zone_id=default.zones[0].id,
            vswitch_id=default_rv5_u_xt.id,
            storage_size=50,
            master_cu=4,
            vpc_id=default_zc8_rd9.id,
            db_instance_mode="StorageElastic",
            description=name)
        default_db_resource_group = alicloud.gpdb.DbResourceGroup("default",
            resource_group_config=json.dumps({
                "CpuRateLimit": 10,
                "MemoryLimit": 10,
                "MemorySharedQuota": 80,
                "MemorySpillRatio": 0,
                "Concurrency": 10,
            }),
            db_instance_id=default_jxw_sl_w.id,
            resource_group_name="yb_example_group")
        ```

        ## Import

        Gpdb Db Resource Group can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:gpdb/dbResourceGroup:DbResourceGroup example <db_instance_id>:<resource_group_name>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] db_instance_id: The instance ID.> You can call the DescribeDBInstances operation to view the instance IDs of all AnalyticDB PostgreSQL instances in the target region.
        :param pulumi.Input[str] resource_group_config: Resource group configuration.
        :param pulumi.Input[str] resource_group_name: Resource group name.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DbResourceGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Gpdb Db Resource Group resource.

        For information about Gpdb Db Resource Group and how to use it, see [What is Db Resource Group](https://www.alibabacloud.com/help/en/).

        > **NOTE:** Available since v1.225.0.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import json
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "terraform-example"
        default = alicloud.get_zones(available_resource_creation="VSwitch")
        default_zc8_rd9 = alicloud.vpc.Network("defaultZc8RD9", cidr_block="192.168.0.0/16")
        default_rv5_u_xt = alicloud.vpc.Switch("defaultRv5UXt",
            vpc_id=default_zc8_rd9.id,
            zone_id=default.zones[0].id,
            cidr_block="192.168.1.0/24")
        default_jxw_sl_w = alicloud.gpdb.Instance("defaultJXWSlW",
            instance_spec="2C8G",
            seg_node_num=2,
            seg_storage_type="cloud_essd",
            instance_network_type="VPC",
            db_instance_category="Basic",
            engine="gpdb",
            resource_management_mode="resourceGroup",
            payment_type="PayAsYouGo",
            ssl_enabled=0,
            engine_version="6.0",
            zone_id=default.zones[0].id,
            vswitch_id=default_rv5_u_xt.id,
            storage_size=50,
            master_cu=4,
            vpc_id=default_zc8_rd9.id,
            db_instance_mode="StorageElastic",
            description=name)
        default_db_resource_group = alicloud.gpdb.DbResourceGroup("default",
            resource_group_config=json.dumps({
                "CpuRateLimit": 10,
                "MemoryLimit": 10,
                "MemorySharedQuota": 80,
                "MemorySpillRatio": 0,
                "Concurrency": 10,
            }),
            db_instance_id=default_jxw_sl_w.id,
            resource_group_name="yb_example_group")
        ```

        ## Import

        Gpdb Db Resource Group can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:gpdb/dbResourceGroup:DbResourceGroup example <db_instance_id>:<resource_group_name>
        ```

        :param str resource_name: The name of the resource.
        :param DbResourceGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DbResourceGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 db_instance_id: Optional[pulumi.Input[str]] = None,
                 resource_group_config: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DbResourceGroupArgs.__new__(DbResourceGroupArgs)

            if db_instance_id is None and not opts.urn:
                raise TypeError("Missing required property 'db_instance_id'")
            __props__.__dict__["db_instance_id"] = db_instance_id
            if resource_group_config is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_config'")
            __props__.__dict__["resource_group_config"] = resource_group_config
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
        super(DbResourceGroup, __self__).__init__(
            'alicloud:gpdb/dbResourceGroup:DbResourceGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            db_instance_id: Optional[pulumi.Input[str]] = None,
            resource_group_config: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None) -> 'DbResourceGroup':
        """
        Get an existing DbResourceGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] db_instance_id: The instance ID.> You can call the DescribeDBInstances operation to view the instance IDs of all AnalyticDB PostgreSQL instances in the target region.
        :param pulumi.Input[str] resource_group_config: Resource group configuration.
        :param pulumi.Input[str] resource_group_name: Resource group name.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DbResourceGroupState.__new__(_DbResourceGroupState)

        __props__.__dict__["db_instance_id"] = db_instance_id
        __props__.__dict__["resource_group_config"] = resource_group_config
        __props__.__dict__["resource_group_name"] = resource_group_name
        return DbResourceGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="dbInstanceId")
    def db_instance_id(self) -> pulumi.Output[str]:
        """
        The instance ID.> You can call the DescribeDBInstances operation to view the instance IDs of all AnalyticDB PostgreSQL instances in the target region.
        """
        return pulumi.get(self, "db_instance_id")

    @property
    @pulumi.getter(name="resourceGroupConfig")
    def resource_group_config(self) -> pulumi.Output[str]:
        """
        Resource group configuration.
        """
        return pulumi.get(self, "resource_group_config")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        Resource group name.
        """
        return pulumi.get(self, "resource_group_name")

