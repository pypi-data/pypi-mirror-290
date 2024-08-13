# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['BackupPolicyArgs', 'BackupPolicy']

@pulumi.input_type
class BackupPolicyArgs:
    def __init__(__self__, *,
                 db_cluster_id: pulumi.Input[str],
                 preferred_backup_periods: pulumi.Input[Sequence[pulumi.Input[str]]],
                 preferred_backup_time: pulumi.Input[str]):
        """
        The set of arguments for constructing a BackupPolicy resource.
        :param pulumi.Input[str] db_cluster_id: The Id of cluster that can run database.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] preferred_backup_periods: ADB Cluster backup period. Valid values: [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday].
        :param pulumi.Input[str] preferred_backup_time: ADB Cluster backup time, in the format of HH:mmZ- HH:mmZ. Time setting interval is one hour. China time is 8 hours behind it.
        """
        pulumi.set(__self__, "db_cluster_id", db_cluster_id)
        pulumi.set(__self__, "preferred_backup_periods", preferred_backup_periods)
        pulumi.set(__self__, "preferred_backup_time", preferred_backup_time)

    @property
    @pulumi.getter(name="dbClusterId")
    def db_cluster_id(self) -> pulumi.Input[str]:
        """
        The Id of cluster that can run database.
        """
        return pulumi.get(self, "db_cluster_id")

    @db_cluster_id.setter
    def db_cluster_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "db_cluster_id", value)

    @property
    @pulumi.getter(name="preferredBackupPeriods")
    def preferred_backup_periods(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        ADB Cluster backup period. Valid values: [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday].
        """
        return pulumi.get(self, "preferred_backup_periods")

    @preferred_backup_periods.setter
    def preferred_backup_periods(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "preferred_backup_periods", value)

    @property
    @pulumi.getter(name="preferredBackupTime")
    def preferred_backup_time(self) -> pulumi.Input[str]:
        """
        ADB Cluster backup time, in the format of HH:mmZ- HH:mmZ. Time setting interval is one hour. China time is 8 hours behind it.
        """
        return pulumi.get(self, "preferred_backup_time")

    @preferred_backup_time.setter
    def preferred_backup_time(self, value: pulumi.Input[str]):
        pulumi.set(self, "preferred_backup_time", value)


@pulumi.input_type
class _BackupPolicyState:
    def __init__(__self__, *,
                 backup_retention_period: Optional[pulumi.Input[str]] = None,
                 db_cluster_id: Optional[pulumi.Input[str]] = None,
                 preferred_backup_periods: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 preferred_backup_time: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering BackupPolicy resources.
        :param pulumi.Input[str] backup_retention_period: Cluster backup retention days, Fixed for 7 days, not modified.
        :param pulumi.Input[str] db_cluster_id: The Id of cluster that can run database.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] preferred_backup_periods: ADB Cluster backup period. Valid values: [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday].
        :param pulumi.Input[str] preferred_backup_time: ADB Cluster backup time, in the format of HH:mmZ- HH:mmZ. Time setting interval is one hour. China time is 8 hours behind it.
        """
        if backup_retention_period is not None:
            pulumi.set(__self__, "backup_retention_period", backup_retention_period)
        if db_cluster_id is not None:
            pulumi.set(__self__, "db_cluster_id", db_cluster_id)
        if preferred_backup_periods is not None:
            pulumi.set(__self__, "preferred_backup_periods", preferred_backup_periods)
        if preferred_backup_time is not None:
            pulumi.set(__self__, "preferred_backup_time", preferred_backup_time)

    @property
    @pulumi.getter(name="backupRetentionPeriod")
    def backup_retention_period(self) -> Optional[pulumi.Input[str]]:
        """
        Cluster backup retention days, Fixed for 7 days, not modified.
        """
        return pulumi.get(self, "backup_retention_period")

    @backup_retention_period.setter
    def backup_retention_period(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "backup_retention_period", value)

    @property
    @pulumi.getter(name="dbClusterId")
    def db_cluster_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Id of cluster that can run database.
        """
        return pulumi.get(self, "db_cluster_id")

    @db_cluster_id.setter
    def db_cluster_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "db_cluster_id", value)

    @property
    @pulumi.getter(name="preferredBackupPeriods")
    def preferred_backup_periods(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        ADB Cluster backup period. Valid values: [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday].
        """
        return pulumi.get(self, "preferred_backup_periods")

    @preferred_backup_periods.setter
    def preferred_backup_periods(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "preferred_backup_periods", value)

    @property
    @pulumi.getter(name="preferredBackupTime")
    def preferred_backup_time(self) -> Optional[pulumi.Input[str]]:
        """
        ADB Cluster backup time, in the format of HH:mmZ- HH:mmZ. Time setting interval is one hour. China time is 8 hours behind it.
        """
        return pulumi.get(self, "preferred_backup_time")

    @preferred_backup_time.setter
    def preferred_backup_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "preferred_backup_time", value)


class BackupPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 db_cluster_id: Optional[pulumi.Input[str]] = None,
                 preferred_backup_periods: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 preferred_backup_time: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ## Import

        ADB backup policy can be imported using the id or cluster id, e.g.

        ```sh
        $ pulumi import alicloud:adb/backupPolicy:BackupPolicy example "am-12345678"
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] db_cluster_id: The Id of cluster that can run database.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] preferred_backup_periods: ADB Cluster backup period. Valid values: [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday].
        :param pulumi.Input[str] preferred_backup_time: ADB Cluster backup time, in the format of HH:mmZ- HH:mmZ. Time setting interval is one hour. China time is 8 hours behind it.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BackupPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Import

        ADB backup policy can be imported using the id or cluster id, e.g.

        ```sh
        $ pulumi import alicloud:adb/backupPolicy:BackupPolicy example "am-12345678"
        ```

        :param str resource_name: The name of the resource.
        :param BackupPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BackupPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 db_cluster_id: Optional[pulumi.Input[str]] = None,
                 preferred_backup_periods: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 preferred_backup_time: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BackupPolicyArgs.__new__(BackupPolicyArgs)

            if db_cluster_id is None and not opts.urn:
                raise TypeError("Missing required property 'db_cluster_id'")
            __props__.__dict__["db_cluster_id"] = db_cluster_id
            if preferred_backup_periods is None and not opts.urn:
                raise TypeError("Missing required property 'preferred_backup_periods'")
            __props__.__dict__["preferred_backup_periods"] = preferred_backup_periods
            if preferred_backup_time is None and not opts.urn:
                raise TypeError("Missing required property 'preferred_backup_time'")
            __props__.__dict__["preferred_backup_time"] = preferred_backup_time
            __props__.__dict__["backup_retention_period"] = None
        super(BackupPolicy, __self__).__init__(
            'alicloud:adb/backupPolicy:BackupPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            backup_retention_period: Optional[pulumi.Input[str]] = None,
            db_cluster_id: Optional[pulumi.Input[str]] = None,
            preferred_backup_periods: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            preferred_backup_time: Optional[pulumi.Input[str]] = None) -> 'BackupPolicy':
        """
        Get an existing BackupPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] backup_retention_period: Cluster backup retention days, Fixed for 7 days, not modified.
        :param pulumi.Input[str] db_cluster_id: The Id of cluster that can run database.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] preferred_backup_periods: ADB Cluster backup period. Valid values: [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday].
        :param pulumi.Input[str] preferred_backup_time: ADB Cluster backup time, in the format of HH:mmZ- HH:mmZ. Time setting interval is one hour. China time is 8 hours behind it.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _BackupPolicyState.__new__(_BackupPolicyState)

        __props__.__dict__["backup_retention_period"] = backup_retention_period
        __props__.__dict__["db_cluster_id"] = db_cluster_id
        __props__.__dict__["preferred_backup_periods"] = preferred_backup_periods
        __props__.__dict__["preferred_backup_time"] = preferred_backup_time
        return BackupPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="backupRetentionPeriod")
    def backup_retention_period(self) -> pulumi.Output[str]:
        """
        Cluster backup retention days, Fixed for 7 days, not modified.
        """
        return pulumi.get(self, "backup_retention_period")

    @property
    @pulumi.getter(name="dbClusterId")
    def db_cluster_id(self) -> pulumi.Output[str]:
        """
        The Id of cluster that can run database.
        """
        return pulumi.get(self, "db_cluster_id")

    @property
    @pulumi.getter(name="preferredBackupPeriods")
    def preferred_backup_periods(self) -> pulumi.Output[Sequence[str]]:
        """
        ADB Cluster backup period. Valid values: [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday].
        """
        return pulumi.get(self, "preferred_backup_periods")

    @property
    @pulumi.getter(name="preferredBackupTime")
    def preferred_backup_time(self) -> pulumi.Output[str]:
        """
        ADB Cluster backup time, in the format of HH:mmZ- HH:mmZ. Time setting interval is one hour. China time is 8 hours behind it.
        """
        return pulumi.get(self, "preferred_backup_time")

