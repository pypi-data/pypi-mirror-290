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

__all__ = ['EnterpriseSnapshotPolicyArgs', 'EnterpriseSnapshotPolicy']

@pulumi.input_type
class EnterpriseSnapshotPolicyArgs:
    def __init__(__self__, *,
                 enterprise_snapshot_policy_name: pulumi.Input[str],
                 retain_rule: pulumi.Input['EnterpriseSnapshotPolicyRetainRuleArgs'],
                 schedule: pulumi.Input['EnterpriseSnapshotPolicyScheduleArgs'],
                 target_type: pulumi.Input[str],
                 cross_region_copy_info: Optional[pulumi.Input['EnterpriseSnapshotPolicyCrossRegionCopyInfoArgs']] = None,
                 desc: Optional[pulumi.Input[str]] = None,
                 resource_group_id: Optional[pulumi.Input[str]] = None,
                 special_retain_rules: Optional[pulumi.Input['EnterpriseSnapshotPolicySpecialRetainRulesArgs']] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 storage_rule: Optional[pulumi.Input['EnterpriseSnapshotPolicyStorageRuleArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None):
        """
        The set of arguments for constructing a EnterpriseSnapshotPolicy resource.
        :param pulumi.Input[str] enterprise_snapshot_policy_name: The name of the resource.
        :param pulumi.Input['EnterpriseSnapshotPolicyRetainRuleArgs'] retain_rule: Snapshot retention policy representing resources. See `retain_rule` below.
        :param pulumi.Input['EnterpriseSnapshotPolicyScheduleArgs'] schedule: The scheduling plan that represents the resource. See `schedule` below.
        :param pulumi.Input[str] target_type: Represents the target type of resource binding.
        :param pulumi.Input['EnterpriseSnapshotPolicyCrossRegionCopyInfoArgs'] cross_region_copy_info: Snapshot replication information. See `cross_region_copy_info` below.
        :param pulumi.Input[str] desc: Description information representing the resource.
        :param pulumi.Input[str] resource_group_id: The ID of the resource group.
        :param pulumi.Input['EnterpriseSnapshotPolicySpecialRetainRulesArgs'] special_retain_rules: Snapshot special retention rules. See `special_retain_rules` below.
        :param pulumi.Input[str] status: The status of the resource.
        :param pulumi.Input['EnterpriseSnapshotPolicyStorageRuleArgs'] storage_rule: Snapshot storage policy. See `storage_rule` below.
        :param pulumi.Input[Mapping[str, Any]] tags: The tag of the resource.
        """
        pulumi.set(__self__, "enterprise_snapshot_policy_name", enterprise_snapshot_policy_name)
        pulumi.set(__self__, "retain_rule", retain_rule)
        pulumi.set(__self__, "schedule", schedule)
        pulumi.set(__self__, "target_type", target_type)
        if cross_region_copy_info is not None:
            pulumi.set(__self__, "cross_region_copy_info", cross_region_copy_info)
        if desc is not None:
            pulumi.set(__self__, "desc", desc)
        if resource_group_id is not None:
            pulumi.set(__self__, "resource_group_id", resource_group_id)
        if special_retain_rules is not None:
            pulumi.set(__self__, "special_retain_rules", special_retain_rules)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if storage_rule is not None:
            pulumi.set(__self__, "storage_rule", storage_rule)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="enterpriseSnapshotPolicyName")
    def enterprise_snapshot_policy_name(self) -> pulumi.Input[str]:
        """
        The name of the resource.
        """
        return pulumi.get(self, "enterprise_snapshot_policy_name")

    @enterprise_snapshot_policy_name.setter
    def enterprise_snapshot_policy_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "enterprise_snapshot_policy_name", value)

    @property
    @pulumi.getter(name="retainRule")
    def retain_rule(self) -> pulumi.Input['EnterpriseSnapshotPolicyRetainRuleArgs']:
        """
        Snapshot retention policy representing resources. See `retain_rule` below.
        """
        return pulumi.get(self, "retain_rule")

    @retain_rule.setter
    def retain_rule(self, value: pulumi.Input['EnterpriseSnapshotPolicyRetainRuleArgs']):
        pulumi.set(self, "retain_rule", value)

    @property
    @pulumi.getter
    def schedule(self) -> pulumi.Input['EnterpriseSnapshotPolicyScheduleArgs']:
        """
        The scheduling plan that represents the resource. See `schedule` below.
        """
        return pulumi.get(self, "schedule")

    @schedule.setter
    def schedule(self, value: pulumi.Input['EnterpriseSnapshotPolicyScheduleArgs']):
        pulumi.set(self, "schedule", value)

    @property
    @pulumi.getter(name="targetType")
    def target_type(self) -> pulumi.Input[str]:
        """
        Represents the target type of resource binding.
        """
        return pulumi.get(self, "target_type")

    @target_type.setter
    def target_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "target_type", value)

    @property
    @pulumi.getter(name="crossRegionCopyInfo")
    def cross_region_copy_info(self) -> Optional[pulumi.Input['EnterpriseSnapshotPolicyCrossRegionCopyInfoArgs']]:
        """
        Snapshot replication information. See `cross_region_copy_info` below.
        """
        return pulumi.get(self, "cross_region_copy_info")

    @cross_region_copy_info.setter
    def cross_region_copy_info(self, value: Optional[pulumi.Input['EnterpriseSnapshotPolicyCrossRegionCopyInfoArgs']]):
        pulumi.set(self, "cross_region_copy_info", value)

    @property
    @pulumi.getter
    def desc(self) -> Optional[pulumi.Input[str]]:
        """
        Description information representing the resource.
        """
        return pulumi.get(self, "desc")

    @desc.setter
    def desc(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "desc", value)

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the resource group.
        """
        return pulumi.get(self, "resource_group_id")

    @resource_group_id.setter
    def resource_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_id", value)

    @property
    @pulumi.getter(name="specialRetainRules")
    def special_retain_rules(self) -> Optional[pulumi.Input['EnterpriseSnapshotPolicySpecialRetainRulesArgs']]:
        """
        Snapshot special retention rules. See `special_retain_rules` below.
        """
        return pulumi.get(self, "special_retain_rules")

    @special_retain_rules.setter
    def special_retain_rules(self, value: Optional[pulumi.Input['EnterpriseSnapshotPolicySpecialRetainRulesArgs']]):
        pulumi.set(self, "special_retain_rules", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the resource.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter(name="storageRule")
    def storage_rule(self) -> Optional[pulumi.Input['EnterpriseSnapshotPolicyStorageRuleArgs']]:
        """
        Snapshot storage policy. See `storage_rule` below.
        """
        return pulumi.get(self, "storage_rule")

    @storage_rule.setter
    def storage_rule(self, value: Optional[pulumi.Input['EnterpriseSnapshotPolicyStorageRuleArgs']]):
        pulumi.set(self, "storage_rule", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        The tag of the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _EnterpriseSnapshotPolicyState:
    def __init__(__self__, *,
                 create_time: Optional[pulumi.Input[str]] = None,
                 cross_region_copy_info: Optional[pulumi.Input['EnterpriseSnapshotPolicyCrossRegionCopyInfoArgs']] = None,
                 desc: Optional[pulumi.Input[str]] = None,
                 enterprise_snapshot_policy_name: Optional[pulumi.Input[str]] = None,
                 resource_group_id: Optional[pulumi.Input[str]] = None,
                 retain_rule: Optional[pulumi.Input['EnterpriseSnapshotPolicyRetainRuleArgs']] = None,
                 schedule: Optional[pulumi.Input['EnterpriseSnapshotPolicyScheduleArgs']] = None,
                 special_retain_rules: Optional[pulumi.Input['EnterpriseSnapshotPolicySpecialRetainRulesArgs']] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 storage_rule: Optional[pulumi.Input['EnterpriseSnapshotPolicyStorageRuleArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 target_type: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering EnterpriseSnapshotPolicy resources.
        :param pulumi.Input[str] create_time: The creation time of the resource.
        :param pulumi.Input['EnterpriseSnapshotPolicyCrossRegionCopyInfoArgs'] cross_region_copy_info: Snapshot replication information. See `cross_region_copy_info` below.
        :param pulumi.Input[str] desc: Description information representing the resource.
        :param pulumi.Input[str] enterprise_snapshot_policy_name: The name of the resource.
        :param pulumi.Input[str] resource_group_id: The ID of the resource group.
        :param pulumi.Input['EnterpriseSnapshotPolicyRetainRuleArgs'] retain_rule: Snapshot retention policy representing resources. See `retain_rule` below.
        :param pulumi.Input['EnterpriseSnapshotPolicyScheduleArgs'] schedule: The scheduling plan that represents the resource. See `schedule` below.
        :param pulumi.Input['EnterpriseSnapshotPolicySpecialRetainRulesArgs'] special_retain_rules: Snapshot special retention rules. See `special_retain_rules` below.
        :param pulumi.Input[str] status: The status of the resource.
        :param pulumi.Input['EnterpriseSnapshotPolicyStorageRuleArgs'] storage_rule: Snapshot storage policy. See `storage_rule` below.
        :param pulumi.Input[Mapping[str, Any]] tags: The tag of the resource.
        :param pulumi.Input[str] target_type: Represents the target type of resource binding.
        """
        if create_time is not None:
            pulumi.set(__self__, "create_time", create_time)
        if cross_region_copy_info is not None:
            pulumi.set(__self__, "cross_region_copy_info", cross_region_copy_info)
        if desc is not None:
            pulumi.set(__self__, "desc", desc)
        if enterprise_snapshot_policy_name is not None:
            pulumi.set(__self__, "enterprise_snapshot_policy_name", enterprise_snapshot_policy_name)
        if resource_group_id is not None:
            pulumi.set(__self__, "resource_group_id", resource_group_id)
        if retain_rule is not None:
            pulumi.set(__self__, "retain_rule", retain_rule)
        if schedule is not None:
            pulumi.set(__self__, "schedule", schedule)
        if special_retain_rules is not None:
            pulumi.set(__self__, "special_retain_rules", special_retain_rules)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if storage_rule is not None:
            pulumi.set(__self__, "storage_rule", storage_rule)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if target_type is not None:
            pulumi.set(__self__, "target_type", target_type)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> Optional[pulumi.Input[str]]:
        """
        The creation time of the resource.
        """
        return pulumi.get(self, "create_time")

    @create_time.setter
    def create_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create_time", value)

    @property
    @pulumi.getter(name="crossRegionCopyInfo")
    def cross_region_copy_info(self) -> Optional[pulumi.Input['EnterpriseSnapshotPolicyCrossRegionCopyInfoArgs']]:
        """
        Snapshot replication information. See `cross_region_copy_info` below.
        """
        return pulumi.get(self, "cross_region_copy_info")

    @cross_region_copy_info.setter
    def cross_region_copy_info(self, value: Optional[pulumi.Input['EnterpriseSnapshotPolicyCrossRegionCopyInfoArgs']]):
        pulumi.set(self, "cross_region_copy_info", value)

    @property
    @pulumi.getter
    def desc(self) -> Optional[pulumi.Input[str]]:
        """
        Description information representing the resource.
        """
        return pulumi.get(self, "desc")

    @desc.setter
    def desc(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "desc", value)

    @property
    @pulumi.getter(name="enterpriseSnapshotPolicyName")
    def enterprise_snapshot_policy_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource.
        """
        return pulumi.get(self, "enterprise_snapshot_policy_name")

    @enterprise_snapshot_policy_name.setter
    def enterprise_snapshot_policy_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "enterprise_snapshot_policy_name", value)

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the resource group.
        """
        return pulumi.get(self, "resource_group_id")

    @resource_group_id.setter
    def resource_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_id", value)

    @property
    @pulumi.getter(name="retainRule")
    def retain_rule(self) -> Optional[pulumi.Input['EnterpriseSnapshotPolicyRetainRuleArgs']]:
        """
        Snapshot retention policy representing resources. See `retain_rule` below.
        """
        return pulumi.get(self, "retain_rule")

    @retain_rule.setter
    def retain_rule(self, value: Optional[pulumi.Input['EnterpriseSnapshotPolicyRetainRuleArgs']]):
        pulumi.set(self, "retain_rule", value)

    @property
    @pulumi.getter
    def schedule(self) -> Optional[pulumi.Input['EnterpriseSnapshotPolicyScheduleArgs']]:
        """
        The scheduling plan that represents the resource. See `schedule` below.
        """
        return pulumi.get(self, "schedule")

    @schedule.setter
    def schedule(self, value: Optional[pulumi.Input['EnterpriseSnapshotPolicyScheduleArgs']]):
        pulumi.set(self, "schedule", value)

    @property
    @pulumi.getter(name="specialRetainRules")
    def special_retain_rules(self) -> Optional[pulumi.Input['EnterpriseSnapshotPolicySpecialRetainRulesArgs']]:
        """
        Snapshot special retention rules. See `special_retain_rules` below.
        """
        return pulumi.get(self, "special_retain_rules")

    @special_retain_rules.setter
    def special_retain_rules(self, value: Optional[pulumi.Input['EnterpriseSnapshotPolicySpecialRetainRulesArgs']]):
        pulumi.set(self, "special_retain_rules", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the resource.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter(name="storageRule")
    def storage_rule(self) -> Optional[pulumi.Input['EnterpriseSnapshotPolicyStorageRuleArgs']]:
        """
        Snapshot storage policy. See `storage_rule` below.
        """
        return pulumi.get(self, "storage_rule")

    @storage_rule.setter
    def storage_rule(self, value: Optional[pulumi.Input['EnterpriseSnapshotPolicyStorageRuleArgs']]):
        pulumi.set(self, "storage_rule", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        The tag of the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="targetType")
    def target_type(self) -> Optional[pulumi.Input[str]]:
        """
        Represents the target type of resource binding.
        """
        return pulumi.get(self, "target_type")

    @target_type.setter
    def target_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_type", value)


class EnterpriseSnapshotPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cross_region_copy_info: Optional[pulumi.Input[Union['EnterpriseSnapshotPolicyCrossRegionCopyInfoArgs', 'EnterpriseSnapshotPolicyCrossRegionCopyInfoArgsDict']]] = None,
                 desc: Optional[pulumi.Input[str]] = None,
                 enterprise_snapshot_policy_name: Optional[pulumi.Input[str]] = None,
                 resource_group_id: Optional[pulumi.Input[str]] = None,
                 retain_rule: Optional[pulumi.Input[Union['EnterpriseSnapshotPolicyRetainRuleArgs', 'EnterpriseSnapshotPolicyRetainRuleArgsDict']]] = None,
                 schedule: Optional[pulumi.Input[Union['EnterpriseSnapshotPolicyScheduleArgs', 'EnterpriseSnapshotPolicyScheduleArgsDict']]] = None,
                 special_retain_rules: Optional[pulumi.Input[Union['EnterpriseSnapshotPolicySpecialRetainRulesArgs', 'EnterpriseSnapshotPolicySpecialRetainRulesArgsDict']]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 storage_rule: Optional[pulumi.Input[Union['EnterpriseSnapshotPolicyStorageRuleArgs', 'EnterpriseSnapshotPolicyStorageRuleArgsDict']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 target_type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a EBS Enterprise Snapshot Policy resource. enterprise snapshot policy.

        For information about EBS Enterprise Snapshot Policy and how to use it, see [What is Enterprise Snapshot Policy](https://www.alibabacloud.com/help/en/).

        > **NOTE:** Available since v1.215.0.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "terraform-example"
        default_jk_w46o = alicloud.ecs.EcsDisk("defaultJkW46o",
            category="cloud_essd",
            description="esp-attachment-test",
            zone_id="cn-hangzhou-i",
            performance_level="PL1",
            size=20,
            disk_name=name)
        default_pe3jj_r = alicloud.ebs.EnterpriseSnapshotPolicy("defaultPE3jjR",
            status="DISABLED",
            desc="DESC",
            schedule={
                "cron_expression": "0 0 0 1 * ?",
            },
            enterprise_snapshot_policy_name=name,
            target_type="DISK",
            retain_rule={
                "time_interval": 120,
                "time_unit": "DAYS",
            })
        ```

        ## Import

        EBS Enterprise Snapshot Policy can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:ebs/enterpriseSnapshotPolicy:EnterpriseSnapshotPolicy example <id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union['EnterpriseSnapshotPolicyCrossRegionCopyInfoArgs', 'EnterpriseSnapshotPolicyCrossRegionCopyInfoArgsDict']] cross_region_copy_info: Snapshot replication information. See `cross_region_copy_info` below.
        :param pulumi.Input[str] desc: Description information representing the resource.
        :param pulumi.Input[str] enterprise_snapshot_policy_name: The name of the resource.
        :param pulumi.Input[str] resource_group_id: The ID of the resource group.
        :param pulumi.Input[Union['EnterpriseSnapshotPolicyRetainRuleArgs', 'EnterpriseSnapshotPolicyRetainRuleArgsDict']] retain_rule: Snapshot retention policy representing resources. See `retain_rule` below.
        :param pulumi.Input[Union['EnterpriseSnapshotPolicyScheduleArgs', 'EnterpriseSnapshotPolicyScheduleArgsDict']] schedule: The scheduling plan that represents the resource. See `schedule` below.
        :param pulumi.Input[Union['EnterpriseSnapshotPolicySpecialRetainRulesArgs', 'EnterpriseSnapshotPolicySpecialRetainRulesArgsDict']] special_retain_rules: Snapshot special retention rules. See `special_retain_rules` below.
        :param pulumi.Input[str] status: The status of the resource.
        :param pulumi.Input[Union['EnterpriseSnapshotPolicyStorageRuleArgs', 'EnterpriseSnapshotPolicyStorageRuleArgsDict']] storage_rule: Snapshot storage policy. See `storage_rule` below.
        :param pulumi.Input[Mapping[str, Any]] tags: The tag of the resource.
        :param pulumi.Input[str] target_type: Represents the target type of resource binding.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EnterpriseSnapshotPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a EBS Enterprise Snapshot Policy resource. enterprise snapshot policy.

        For information about EBS Enterprise Snapshot Policy and how to use it, see [What is Enterprise Snapshot Policy](https://www.alibabacloud.com/help/en/).

        > **NOTE:** Available since v1.215.0.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "terraform-example"
        default_jk_w46o = alicloud.ecs.EcsDisk("defaultJkW46o",
            category="cloud_essd",
            description="esp-attachment-test",
            zone_id="cn-hangzhou-i",
            performance_level="PL1",
            size=20,
            disk_name=name)
        default_pe3jj_r = alicloud.ebs.EnterpriseSnapshotPolicy("defaultPE3jjR",
            status="DISABLED",
            desc="DESC",
            schedule={
                "cron_expression": "0 0 0 1 * ?",
            },
            enterprise_snapshot_policy_name=name,
            target_type="DISK",
            retain_rule={
                "time_interval": 120,
                "time_unit": "DAYS",
            })
        ```

        ## Import

        EBS Enterprise Snapshot Policy can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:ebs/enterpriseSnapshotPolicy:EnterpriseSnapshotPolicy example <id>
        ```

        :param str resource_name: The name of the resource.
        :param EnterpriseSnapshotPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EnterpriseSnapshotPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cross_region_copy_info: Optional[pulumi.Input[Union['EnterpriseSnapshotPolicyCrossRegionCopyInfoArgs', 'EnterpriseSnapshotPolicyCrossRegionCopyInfoArgsDict']]] = None,
                 desc: Optional[pulumi.Input[str]] = None,
                 enterprise_snapshot_policy_name: Optional[pulumi.Input[str]] = None,
                 resource_group_id: Optional[pulumi.Input[str]] = None,
                 retain_rule: Optional[pulumi.Input[Union['EnterpriseSnapshotPolicyRetainRuleArgs', 'EnterpriseSnapshotPolicyRetainRuleArgsDict']]] = None,
                 schedule: Optional[pulumi.Input[Union['EnterpriseSnapshotPolicyScheduleArgs', 'EnterpriseSnapshotPolicyScheduleArgsDict']]] = None,
                 special_retain_rules: Optional[pulumi.Input[Union['EnterpriseSnapshotPolicySpecialRetainRulesArgs', 'EnterpriseSnapshotPolicySpecialRetainRulesArgsDict']]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 storage_rule: Optional[pulumi.Input[Union['EnterpriseSnapshotPolicyStorageRuleArgs', 'EnterpriseSnapshotPolicyStorageRuleArgsDict']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 target_type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EnterpriseSnapshotPolicyArgs.__new__(EnterpriseSnapshotPolicyArgs)

            __props__.__dict__["cross_region_copy_info"] = cross_region_copy_info
            __props__.__dict__["desc"] = desc
            if enterprise_snapshot_policy_name is None and not opts.urn:
                raise TypeError("Missing required property 'enterprise_snapshot_policy_name'")
            __props__.__dict__["enterprise_snapshot_policy_name"] = enterprise_snapshot_policy_name
            __props__.__dict__["resource_group_id"] = resource_group_id
            if retain_rule is None and not opts.urn:
                raise TypeError("Missing required property 'retain_rule'")
            __props__.__dict__["retain_rule"] = retain_rule
            if schedule is None and not opts.urn:
                raise TypeError("Missing required property 'schedule'")
            __props__.__dict__["schedule"] = schedule
            __props__.__dict__["special_retain_rules"] = special_retain_rules
            __props__.__dict__["status"] = status
            __props__.__dict__["storage_rule"] = storage_rule
            __props__.__dict__["tags"] = tags
            if target_type is None and not opts.urn:
                raise TypeError("Missing required property 'target_type'")
            __props__.__dict__["target_type"] = target_type
            __props__.__dict__["create_time"] = None
        super(EnterpriseSnapshotPolicy, __self__).__init__(
            'alicloud:ebs/enterpriseSnapshotPolicy:EnterpriseSnapshotPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            create_time: Optional[pulumi.Input[str]] = None,
            cross_region_copy_info: Optional[pulumi.Input[Union['EnterpriseSnapshotPolicyCrossRegionCopyInfoArgs', 'EnterpriseSnapshotPolicyCrossRegionCopyInfoArgsDict']]] = None,
            desc: Optional[pulumi.Input[str]] = None,
            enterprise_snapshot_policy_name: Optional[pulumi.Input[str]] = None,
            resource_group_id: Optional[pulumi.Input[str]] = None,
            retain_rule: Optional[pulumi.Input[Union['EnterpriseSnapshotPolicyRetainRuleArgs', 'EnterpriseSnapshotPolicyRetainRuleArgsDict']]] = None,
            schedule: Optional[pulumi.Input[Union['EnterpriseSnapshotPolicyScheduleArgs', 'EnterpriseSnapshotPolicyScheduleArgsDict']]] = None,
            special_retain_rules: Optional[pulumi.Input[Union['EnterpriseSnapshotPolicySpecialRetainRulesArgs', 'EnterpriseSnapshotPolicySpecialRetainRulesArgsDict']]] = None,
            status: Optional[pulumi.Input[str]] = None,
            storage_rule: Optional[pulumi.Input[Union['EnterpriseSnapshotPolicyStorageRuleArgs', 'EnterpriseSnapshotPolicyStorageRuleArgsDict']]] = None,
            tags: Optional[pulumi.Input[Mapping[str, Any]]] = None,
            target_type: Optional[pulumi.Input[str]] = None) -> 'EnterpriseSnapshotPolicy':
        """
        Get an existing EnterpriseSnapshotPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] create_time: The creation time of the resource.
        :param pulumi.Input[Union['EnterpriseSnapshotPolicyCrossRegionCopyInfoArgs', 'EnterpriseSnapshotPolicyCrossRegionCopyInfoArgsDict']] cross_region_copy_info: Snapshot replication information. See `cross_region_copy_info` below.
        :param pulumi.Input[str] desc: Description information representing the resource.
        :param pulumi.Input[str] enterprise_snapshot_policy_name: The name of the resource.
        :param pulumi.Input[str] resource_group_id: The ID of the resource group.
        :param pulumi.Input[Union['EnterpriseSnapshotPolicyRetainRuleArgs', 'EnterpriseSnapshotPolicyRetainRuleArgsDict']] retain_rule: Snapshot retention policy representing resources. See `retain_rule` below.
        :param pulumi.Input[Union['EnterpriseSnapshotPolicyScheduleArgs', 'EnterpriseSnapshotPolicyScheduleArgsDict']] schedule: The scheduling plan that represents the resource. See `schedule` below.
        :param pulumi.Input[Union['EnterpriseSnapshotPolicySpecialRetainRulesArgs', 'EnterpriseSnapshotPolicySpecialRetainRulesArgsDict']] special_retain_rules: Snapshot special retention rules. See `special_retain_rules` below.
        :param pulumi.Input[str] status: The status of the resource.
        :param pulumi.Input[Union['EnterpriseSnapshotPolicyStorageRuleArgs', 'EnterpriseSnapshotPolicyStorageRuleArgsDict']] storage_rule: Snapshot storage policy. See `storage_rule` below.
        :param pulumi.Input[Mapping[str, Any]] tags: The tag of the resource.
        :param pulumi.Input[str] target_type: Represents the target type of resource binding.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _EnterpriseSnapshotPolicyState.__new__(_EnterpriseSnapshotPolicyState)

        __props__.__dict__["create_time"] = create_time
        __props__.__dict__["cross_region_copy_info"] = cross_region_copy_info
        __props__.__dict__["desc"] = desc
        __props__.__dict__["enterprise_snapshot_policy_name"] = enterprise_snapshot_policy_name
        __props__.__dict__["resource_group_id"] = resource_group_id
        __props__.__dict__["retain_rule"] = retain_rule
        __props__.__dict__["schedule"] = schedule
        __props__.__dict__["special_retain_rules"] = special_retain_rules
        __props__.__dict__["status"] = status
        __props__.__dict__["storage_rule"] = storage_rule
        __props__.__dict__["tags"] = tags
        __props__.__dict__["target_type"] = target_type
        return EnterpriseSnapshotPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        The creation time of the resource.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="crossRegionCopyInfo")
    def cross_region_copy_info(self) -> pulumi.Output['outputs.EnterpriseSnapshotPolicyCrossRegionCopyInfo']:
        """
        Snapshot replication information. See `cross_region_copy_info` below.
        """
        return pulumi.get(self, "cross_region_copy_info")

    @property
    @pulumi.getter
    def desc(self) -> pulumi.Output[Optional[str]]:
        """
        Description information representing the resource.
        """
        return pulumi.get(self, "desc")

    @property
    @pulumi.getter(name="enterpriseSnapshotPolicyName")
    def enterprise_snapshot_policy_name(self) -> pulumi.Output[str]:
        """
        The name of the resource.
        """
        return pulumi.get(self, "enterprise_snapshot_policy_name")

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> pulumi.Output[str]:
        """
        The ID of the resource group.
        """
        return pulumi.get(self, "resource_group_id")

    @property
    @pulumi.getter(name="retainRule")
    def retain_rule(self) -> pulumi.Output['outputs.EnterpriseSnapshotPolicyRetainRule']:
        """
        Snapshot retention policy representing resources. See `retain_rule` below.
        """
        return pulumi.get(self, "retain_rule")

    @property
    @pulumi.getter
    def schedule(self) -> pulumi.Output['outputs.EnterpriseSnapshotPolicySchedule']:
        """
        The scheduling plan that represents the resource. See `schedule` below.
        """
        return pulumi.get(self, "schedule")

    @property
    @pulumi.getter(name="specialRetainRules")
    def special_retain_rules(self) -> pulumi.Output['outputs.EnterpriseSnapshotPolicySpecialRetainRules']:
        """
        Snapshot special retention rules. See `special_retain_rules` below.
        """
        return pulumi.get(self, "special_retain_rules")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The status of the resource.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="storageRule")
    def storage_rule(self) -> pulumi.Output[Optional['outputs.EnterpriseSnapshotPolicyStorageRule']]:
        """
        Snapshot storage policy. See `storage_rule` below.
        """
        return pulumi.get(self, "storage_rule")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, Any]]]:
        """
        The tag of the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="targetType")
    def target_type(self) -> pulumi.Output[str]:
        """
        Represents the target type of resource binding.
        """
        return pulumi.get(self, "target_type")

