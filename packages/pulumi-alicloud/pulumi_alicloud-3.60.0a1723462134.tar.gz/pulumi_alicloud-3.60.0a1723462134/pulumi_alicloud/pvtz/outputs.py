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

__all__ = [
    'EndpointIpConfig',
    'RuleAttachmentVpc',
    'RuleForwardIp',
    'ZoneAttachmentVpc',
    'ZoneUserInfo',
    'GetEndpointsEndpointResult',
    'GetEndpointsEndpointIpConfigResult',
    'GetResolverZonesZoneResult',
    'GetRulesRuleResult',
    'GetRulesRuleBindVpcResult',
    'GetRulesRuleForwardIpResult',
    'GetZoneRecordsRecordResult',
    'GetZonesZoneResult',
    'GetZonesZoneBindVpcResult',
]

@pulumi.output_type
class EndpointIpConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "cidrBlock":
            suggest = "cidr_block"
        elif key == "vswitchId":
            suggest = "vswitch_id"
        elif key == "zoneId":
            suggest = "zone_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EndpointIpConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EndpointIpConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EndpointIpConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cidr_block: str,
                 vswitch_id: str,
                 zone_id: str,
                 ip: Optional[str] = None):
        """
        :param str cidr_block: The Subnet mask.
        :param str vswitch_id: The Vswitch id.
        :param str zone_id: The Zone ID.
        :param str ip: The IP address within the parameter range of the subnet mask.  It is recommended to use the IP address assigned by the system.
        """
        pulumi.set(__self__, "cidr_block", cidr_block)
        pulumi.set(__self__, "vswitch_id", vswitch_id)
        pulumi.set(__self__, "zone_id", zone_id)
        if ip is not None:
            pulumi.set(__self__, "ip", ip)

    @property
    @pulumi.getter(name="cidrBlock")
    def cidr_block(self) -> str:
        """
        The Subnet mask.
        """
        return pulumi.get(self, "cidr_block")

    @property
    @pulumi.getter(name="vswitchId")
    def vswitch_id(self) -> str:
        """
        The Vswitch id.
        """
        return pulumi.get(self, "vswitch_id")

    @property
    @pulumi.getter(name="zoneId")
    def zone_id(self) -> str:
        """
        The Zone ID.
        """
        return pulumi.get(self, "zone_id")

    @property
    @pulumi.getter
    def ip(self) -> Optional[str]:
        """
        The IP address within the parameter range of the subnet mask.  It is recommended to use the IP address assigned by the system.
        """
        return pulumi.get(self, "ip")


@pulumi.output_type
class RuleAttachmentVpc(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "regionId":
            suggest = "region_id"
        elif key == "vpcId":
            suggest = "vpc_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in RuleAttachmentVpc. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        RuleAttachmentVpc.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        RuleAttachmentVpc.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 region_id: str,
                 vpc_id: str):
        """
        :param str region_id: The region of the vpc. If not set, the current region will instead of.
        :param str vpc_id: The ID of the VPC.  **NOTE:** The VPC that can be associated with the forwarding rule must belong to the same region as the Endpoint.
        """
        pulumi.set(__self__, "region_id", region_id)
        pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter(name="regionId")
    def region_id(self) -> str:
        """
        The region of the vpc. If not set, the current region will instead of.
        """
        return pulumi.get(self, "region_id")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> str:
        """
        The ID of the VPC.  **NOTE:** The VPC that can be associated with the forwarding rule must belong to the same region as the Endpoint.
        """
        return pulumi.get(self, "vpc_id")


@pulumi.output_type
class RuleForwardIp(dict):
    def __init__(__self__, *,
                 ip: str,
                 port: int):
        """
        :param str ip: The ip of the forwarding destination.
        :param int port: The port of the forwarding destination.
        """
        pulumi.set(__self__, "ip", ip)
        pulumi.set(__self__, "port", port)

    @property
    @pulumi.getter
    def ip(self) -> str:
        """
        The ip of the forwarding destination.
        """
        return pulumi.get(self, "ip")

    @property
    @pulumi.getter
    def port(self) -> int:
        """
        The port of the forwarding destination.
        """
        return pulumi.get(self, "port")


@pulumi.output_type
class ZoneAttachmentVpc(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "vpcId":
            suggest = "vpc_id"
        elif key == "regionId":
            suggest = "region_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ZoneAttachmentVpc. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ZoneAttachmentVpc.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ZoneAttachmentVpc.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 vpc_id: str,
                 region_id: Optional[str] = None):
        """
        :param str vpc_id: The Id of the vpc.
        :param str region_id: The region of the vpc. If not set, the current region will instead of.
        """
        pulumi.set(__self__, "vpc_id", vpc_id)
        if region_id is not None:
            pulumi.set(__self__, "region_id", region_id)

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> str:
        """
        The Id of the vpc.
        """
        return pulumi.get(self, "vpc_id")

    @property
    @pulumi.getter(name="regionId")
    def region_id(self) -> Optional[str]:
        """
        The region of the vpc. If not set, the current region will instead of.
        """
        return pulumi.get(self, "region_id")


@pulumi.output_type
class ZoneUserInfo(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "regionIds":
            suggest = "region_ids"
        elif key == "userId":
            suggest = "user_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ZoneUserInfo. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ZoneUserInfo.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ZoneUserInfo.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 region_ids: Optional[Sequence[str]] = None,
                 user_id: Optional[str] = None):
        """
        :param Sequence[str] region_ids: The list of the region IDs.
        :param str user_id: The user ID belonging to the region is used for cross-account synchronization scenarios.
        """
        if region_ids is not None:
            pulumi.set(__self__, "region_ids", region_ids)
        if user_id is not None:
            pulumi.set(__self__, "user_id", user_id)

    @property
    @pulumi.getter(name="regionIds")
    def region_ids(self) -> Optional[Sequence[str]]:
        """
        The list of the region IDs.
        """
        return pulumi.get(self, "region_ids")

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> Optional[str]:
        """
        The user ID belonging to the region is used for cross-account synchronization scenarios.
        """
        return pulumi.get(self, "user_id")


@pulumi.output_type
class GetEndpointsEndpointResult(dict):
    def __init__(__self__, *,
                 create_time: str,
                 endpoint_name: str,
                 id: str,
                 ip_configs: Sequence['outputs.GetEndpointsEndpointIpConfigResult'],
                 security_group_id: str,
                 status: str,
                 vpc_id: str,
                 vpc_name: str,
                 vpc_region_id: str):
        """
        :param str create_time: The creation time of the resource.
        :param str endpoint_name: The name of the resource.
        :param Sequence['GetEndpointsEndpointIpConfigArgs'] ip_configs: The Ip Configs.
        :param str security_group_id: The ID of the Security Group.
        :param str status: The status of the resource. Valid values: `CHANGE_FAILED`, `CHANGE_INIT`, `EXCEPTION`, `FAILED`, `INIT`, `SUCCESS`.
        :param str vpc_id: The VPC ID.
        :param str vpc_name: The name of the VPC.
        :param str vpc_region_id: The Region of the VPC.
        """
        pulumi.set(__self__, "create_time", create_time)
        pulumi.set(__self__, "endpoint_name", endpoint_name)
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "ip_configs", ip_configs)
        pulumi.set(__self__, "security_group_id", security_group_id)
        pulumi.set(__self__, "status", status)
        pulumi.set(__self__, "vpc_id", vpc_id)
        pulumi.set(__self__, "vpc_name", vpc_name)
        pulumi.set(__self__, "vpc_region_id", vpc_region_id)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> str:
        """
        The creation time of the resource.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="endpointName")
    def endpoint_name(self) -> str:
        """
        The name of the resource.
        """
        return pulumi.get(self, "endpoint_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="ipConfigs")
    def ip_configs(self) -> Sequence['outputs.GetEndpointsEndpointIpConfigResult']:
        """
        The Ip Configs.
        """
        return pulumi.get(self, "ip_configs")

    @property
    @pulumi.getter(name="securityGroupId")
    def security_group_id(self) -> str:
        """
        The ID of the Security Group.
        """
        return pulumi.get(self, "security_group_id")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        The status of the resource. Valid values: `CHANGE_FAILED`, `CHANGE_INIT`, `EXCEPTION`, `FAILED`, `INIT`, `SUCCESS`.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> str:
        """
        The VPC ID.
        """
        return pulumi.get(self, "vpc_id")

    @property
    @pulumi.getter(name="vpcName")
    def vpc_name(self) -> str:
        """
        The name of the VPC.
        """
        return pulumi.get(self, "vpc_name")

    @property
    @pulumi.getter(name="vpcRegionId")
    def vpc_region_id(self) -> str:
        """
        The Region of the VPC.
        """
        return pulumi.get(self, "vpc_region_id")


@pulumi.output_type
class GetEndpointsEndpointIpConfigResult(dict):
    def __init__(__self__, *,
                 cidr_block: str,
                 ip: str,
                 vswitch_id: str,
                 zone_id: str):
        """
        :param str cidr_block: The Subnet mask.
        :param str ip: The IP address within the parameter range of the subnet mask. **NOTE:** It is recommended to use the IP address assigned by the system.
        :param str vswitch_id: The Vswitch id.
        :param str zone_id: The Zone ID.
        """
        pulumi.set(__self__, "cidr_block", cidr_block)
        pulumi.set(__self__, "ip", ip)
        pulumi.set(__self__, "vswitch_id", vswitch_id)
        pulumi.set(__self__, "zone_id", zone_id)

    @property
    @pulumi.getter(name="cidrBlock")
    def cidr_block(self) -> str:
        """
        The Subnet mask.
        """
        return pulumi.get(self, "cidr_block")

    @property
    @pulumi.getter
    def ip(self) -> str:
        """
        The IP address within the parameter range of the subnet mask. **NOTE:** It is recommended to use the IP address assigned by the system.
        """
        return pulumi.get(self, "ip")

    @property
    @pulumi.getter(name="vswitchId")
    def vswitch_id(self) -> str:
        """
        The Vswitch id.
        """
        return pulumi.get(self, "vswitch_id")

    @property
    @pulumi.getter(name="zoneId")
    def zone_id(self) -> str:
        """
        The Zone ID.
        """
        return pulumi.get(self, "zone_id")


@pulumi.output_type
class GetResolverZonesZoneResult(dict):
    def __init__(__self__, *,
                 status: str,
                 zone_id: str):
        """
        :param str status: The status of the Zone.
        :param str zone_id: The zone ID.
        """
        pulumi.set(__self__, "status", status)
        pulumi.set(__self__, "zone_id", zone_id)

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        The status of the Zone.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="zoneId")
    def zone_id(self) -> str:
        """
        The zone ID.
        """
        return pulumi.get(self, "zone_id")


@pulumi.output_type
class GetRulesRuleResult(dict):
    def __init__(__self__, *,
                 bind_vpcs: Sequence['outputs.GetRulesRuleBindVpcResult'],
                 create_time: str,
                 endpoint_id: str,
                 endpoint_name: str,
                 forward_ips: Sequence['outputs.GetRulesRuleForwardIpResult'],
                 id: str,
                 rule_id: str,
                 rule_name: str,
                 type: str,
                 zone_name: str):
        """
        :param Sequence['GetRulesRuleBindVpcArgs'] bind_vpcs: The List of the VPC. See the following `Block bind_vpcs`. **NOTE:** Available in v1.158.0+.
        :param str create_time: The creation time of the resource.
        :param str endpoint_id: The ID of the Endpoint.
        :param str endpoint_name: The Name of the Endpoint.
        :param str id: The ID of the Rule.
        :param str rule_id: The first ID of the resource.
        :param str rule_name: The name of the resource.
        :param str type: The type of the rule.
        :param str zone_name: The name of the forwarding zone.
        """
        pulumi.set(__self__, "bind_vpcs", bind_vpcs)
        pulumi.set(__self__, "create_time", create_time)
        pulumi.set(__self__, "endpoint_id", endpoint_id)
        pulumi.set(__self__, "endpoint_name", endpoint_name)
        pulumi.set(__self__, "forward_ips", forward_ips)
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "rule_id", rule_id)
        pulumi.set(__self__, "rule_name", rule_name)
        pulumi.set(__self__, "type", type)
        pulumi.set(__self__, "zone_name", zone_name)

    @property
    @pulumi.getter(name="bindVpcs")
    def bind_vpcs(self) -> Sequence['outputs.GetRulesRuleBindVpcResult']:
        """
        The List of the VPC. See the following `Block bind_vpcs`. **NOTE:** Available in v1.158.0+.
        """
        return pulumi.get(self, "bind_vpcs")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> str:
        """
        The creation time of the resource.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="endpointId")
    def endpoint_id(self) -> str:
        """
        The ID of the Endpoint.
        """
        return pulumi.get(self, "endpoint_id")

    @property
    @pulumi.getter(name="endpointName")
    def endpoint_name(self) -> str:
        """
        The Name of the Endpoint.
        """
        return pulumi.get(self, "endpoint_name")

    @property
    @pulumi.getter(name="forwardIps")
    def forward_ips(self) -> Sequence['outputs.GetRulesRuleForwardIpResult']:
        return pulumi.get(self, "forward_ips")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of the Rule.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="ruleId")
    def rule_id(self) -> str:
        """
        The first ID of the resource.
        """
        return pulumi.get(self, "rule_id")

    @property
    @pulumi.getter(name="ruleName")
    def rule_name(self) -> str:
        """
        The name of the resource.
        """
        return pulumi.get(self, "rule_name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the rule.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="zoneName")
    def zone_name(self) -> str:
        """
        The name of the forwarding zone.
        """
        return pulumi.get(self, "zone_name")


@pulumi.output_type
class GetRulesRuleBindVpcResult(dict):
    def __init__(__self__, *,
                 region_id: str,
                 region_name: str,
                 vpc_id: str,
                 vpc_name: str):
        """
        :param str region_id: The region ID of the vpc.
        :param str region_name: The Region Name of the vpc.
        :param str vpc_id: The ID of the VPC.
        :param str vpc_name: The Name of the VPC.
        """
        pulumi.set(__self__, "region_id", region_id)
        pulumi.set(__self__, "region_name", region_name)
        pulumi.set(__self__, "vpc_id", vpc_id)
        pulumi.set(__self__, "vpc_name", vpc_name)

    @property
    @pulumi.getter(name="regionId")
    def region_id(self) -> str:
        """
        The region ID of the vpc.
        """
        return pulumi.get(self, "region_id")

    @property
    @pulumi.getter(name="regionName")
    def region_name(self) -> str:
        """
        The Region Name of the vpc.
        """
        return pulumi.get(self, "region_name")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> str:
        """
        The ID of the VPC.
        """
        return pulumi.get(self, "vpc_id")

    @property
    @pulumi.getter(name="vpcName")
    def vpc_name(self) -> str:
        """
        The Name of the VPC.
        """
        return pulumi.get(self, "vpc_name")


@pulumi.output_type
class GetRulesRuleForwardIpResult(dict):
    def __init__(__self__, *,
                 ip: str,
                 port: int):
        pulumi.set(__self__, "ip", ip)
        pulumi.set(__self__, "port", port)

    @property
    @pulumi.getter
    def ip(self) -> str:
        return pulumi.get(self, "ip")

    @property
    @pulumi.getter
    def port(self) -> int:
        return pulumi.get(self, "port")


@pulumi.output_type
class GetZoneRecordsRecordResult(dict):
    def __init__(__self__, *,
                 id: str,
                 priority: int,
                 record_id: str,
                 remark: str,
                 resource_record: str,
                 rr: str,
                 status: str,
                 ttl: int,
                 type: str,
                 value: str):
        """
        :param str id: ID of the Private Zone Record.
        :param int priority: Priority of the Private Zone Record.
        :param str record_id: RecordId of the Private Zone Record.
        :param str remark: Remark of the Private Zone Record.
        :param str resource_record: Resource record of the Private Zone Record.
        :param str rr: Rr of the Private Zone Record.
        :param str status: Resolve record status. Value:
               - ENABLE: enable resolution.
               - DISABLE: pause parsing.
        :param int ttl: Ttl of the Private Zone Record.
        :param str type: Type of the Private Zone Record.
        :param str value: Value of the Private Zone Record.
        """
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "priority", priority)
        pulumi.set(__self__, "record_id", record_id)
        pulumi.set(__self__, "remark", remark)
        pulumi.set(__self__, "resource_record", resource_record)
        pulumi.set(__self__, "rr", rr)
        pulumi.set(__self__, "status", status)
        pulumi.set(__self__, "ttl", ttl)
        pulumi.set(__self__, "type", type)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        ID of the Private Zone Record.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def priority(self) -> int:
        """
        Priority of the Private Zone Record.
        """
        return pulumi.get(self, "priority")

    @property
    @pulumi.getter(name="recordId")
    def record_id(self) -> str:
        """
        RecordId of the Private Zone Record.
        """
        return pulumi.get(self, "record_id")

    @property
    @pulumi.getter
    def remark(self) -> str:
        """
        Remark of the Private Zone Record.
        """
        return pulumi.get(self, "remark")

    @property
    @pulumi.getter(name="resourceRecord")
    def resource_record(self) -> str:
        """
        Resource record of the Private Zone Record.
        """
        return pulumi.get(self, "resource_record")

    @property
    @pulumi.getter
    def rr(self) -> str:
        """
        Rr of the Private Zone Record.
        """
        return pulumi.get(self, "rr")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Resolve record status. Value:
        - ENABLE: enable resolution.
        - DISABLE: pause parsing.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def ttl(self) -> int:
        """
        Ttl of the Private Zone Record.
        """
        return pulumi.get(self, "ttl")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of the Private Zone Record.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        Value of the Private Zone Record.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class GetZonesZoneResult(dict):
    def __init__(__self__, *,
                 bind_vpcs: Sequence['outputs.GetZonesZoneBindVpcResult'],
                 create_timestamp: int,
                 creation_time: str,
                 id: str,
                 is_ptr: bool,
                 name: str,
                 proxy_pattern: str,
                 record_count: int,
                 remark: str,
                 resource_group_id: str,
                 slave_dns: bool,
                 update_time: str,
                 update_timestamp: int,
                 zone_id: str,
                 zone_name: str):
        """
        :param Sequence['GetZonesZoneBindVpcArgs'] bind_vpcs: List of the VPCs is bound to the Private Zone:
        :param int create_timestamp: Time of create of the Private Zone.
        :param str id: ID of the Private Zone.
        :param bool is_ptr: Whether the Private Zone is ptr.
        :param str name: Name of the Private Zone.
        :param str proxy_pattern: The recursive DNS proxy.
        :param int record_count: Count of the Private Zone Record.
        :param str remark: Remark of the Private Zone.
        :param str resource_group_id: resource_group_id for zone resourceGroupId.
        :param bool slave_dns: Whether to turn on secondary DNS.
        :param int update_timestamp: Time of update of the Private Zone.
        :param str zone_id: ZoneId of the Private Zone.
        :param str zone_name: ZoneName of the Private Zone.
        """
        pulumi.set(__self__, "bind_vpcs", bind_vpcs)
        pulumi.set(__self__, "create_timestamp", create_timestamp)
        pulumi.set(__self__, "creation_time", creation_time)
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "is_ptr", is_ptr)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "proxy_pattern", proxy_pattern)
        pulumi.set(__self__, "record_count", record_count)
        pulumi.set(__self__, "remark", remark)
        pulumi.set(__self__, "resource_group_id", resource_group_id)
        pulumi.set(__self__, "slave_dns", slave_dns)
        pulumi.set(__self__, "update_time", update_time)
        pulumi.set(__self__, "update_timestamp", update_timestamp)
        pulumi.set(__self__, "zone_id", zone_id)
        pulumi.set(__self__, "zone_name", zone_name)

    @property
    @pulumi.getter(name="bindVpcs")
    def bind_vpcs(self) -> Sequence['outputs.GetZonesZoneBindVpcResult']:
        """
        List of the VPCs is bound to the Private Zone:
        """
        return pulumi.get(self, "bind_vpcs")

    @property
    @pulumi.getter(name="createTimestamp")
    def create_timestamp(self) -> int:
        """
        Time of create of the Private Zone.
        """
        return pulumi.get(self, "create_timestamp")

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> str:
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        ID of the Private Zone.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="isPtr")
    def is_ptr(self) -> bool:
        """
        Whether the Private Zone is ptr.
        """
        return pulumi.get(self, "is_ptr")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the Private Zone.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="proxyPattern")
    def proxy_pattern(self) -> str:
        """
        The recursive DNS proxy.
        """
        return pulumi.get(self, "proxy_pattern")

    @property
    @pulumi.getter(name="recordCount")
    def record_count(self) -> int:
        """
        Count of the Private Zone Record.
        """
        return pulumi.get(self, "record_count")

    @property
    @pulumi.getter
    def remark(self) -> str:
        """
        Remark of the Private Zone.
        """
        return pulumi.get(self, "remark")

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> str:
        """
        resource_group_id for zone resourceGroupId.
        """
        return pulumi.get(self, "resource_group_id")

    @property
    @pulumi.getter(name="slaveDns")
    def slave_dns(self) -> bool:
        """
        Whether to turn on secondary DNS.
        """
        return pulumi.get(self, "slave_dns")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> str:
        return pulumi.get(self, "update_time")

    @property
    @pulumi.getter(name="updateTimestamp")
    def update_timestamp(self) -> int:
        """
        Time of update of the Private Zone.
        """
        return pulumi.get(self, "update_timestamp")

    @property
    @pulumi.getter(name="zoneId")
    def zone_id(self) -> str:
        """
        ZoneId of the Private Zone.
        """
        return pulumi.get(self, "zone_id")

    @property
    @pulumi.getter(name="zoneName")
    def zone_name(self) -> str:
        """
        ZoneName of the Private Zone.
        """
        return pulumi.get(self, "zone_name")


@pulumi.output_type
class GetZonesZoneBindVpcResult(dict):
    def __init__(__self__, *,
                 region_id: str,
                 region_name: str,
                 vpc_id: str,
                 vpc_name: str):
        """
        :param str region_id: Binding the regionId of VPC.
        :param str region_name: Binding the regionName of VPC.
        :param str vpc_id: Binding the vpcId of VPC.
        """
        pulumi.set(__self__, "region_id", region_id)
        pulumi.set(__self__, "region_name", region_name)
        pulumi.set(__self__, "vpc_id", vpc_id)
        pulumi.set(__self__, "vpc_name", vpc_name)

    @property
    @pulumi.getter(name="regionId")
    def region_id(self) -> str:
        """
        Binding the regionId of VPC.
        """
        return pulumi.get(self, "region_id")

    @property
    @pulumi.getter(name="regionName")
    def region_name(self) -> str:
        """
        Binding the regionName of VPC.
        """
        return pulumi.get(self, "region_name")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> str:
        """
        Binding the vpcId of VPC.
        """
        return pulumi.get(self, "vpc_id")

    @property
    @pulumi.getter(name="vpcName")
    def vpc_name(self) -> str:
        return pulumi.get(self, "vpc_name")


