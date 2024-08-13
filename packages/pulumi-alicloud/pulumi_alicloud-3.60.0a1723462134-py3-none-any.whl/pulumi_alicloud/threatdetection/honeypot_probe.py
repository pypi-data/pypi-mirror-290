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

__all__ = ['HoneypotProbeArgs', 'HoneypotProbe']

@pulumi.input_type
class HoneypotProbeArgs:
    def __init__(__self__, *,
                 control_node_id: pulumi.Input[str],
                 display_name: pulumi.Input[str],
                 probe_type: pulumi.Input[str],
                 arp: Optional[pulumi.Input[bool]] = None,
                 honeypot_bind_lists: Optional[pulumi.Input[Sequence[pulumi.Input['HoneypotProbeHoneypotBindListArgs']]]] = None,
                 ping: Optional[pulumi.Input[bool]] = None,
                 probe_version: Optional[pulumi.Input[str]] = None,
                 proxy_ip: Optional[pulumi.Input[str]] = None,
                 service_ip_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 uuid: Optional[pulumi.Input[str]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a HoneypotProbe resource.
        :param pulumi.Input[str] control_node_id: The ID of the management node.
        :param pulumi.Input[str] display_name: Probe display name.
        :param pulumi.Input[str] probe_type: Probe type, support `host_probe` and `vpc_black_hole_probe`.
        :param pulumi.Input[bool] arp: ARP spoofing detection.**true**: Enable **false**: Disabled
        :param pulumi.Input[Sequence[pulumi.Input['HoneypotProbeHoneypotBindListArgs']]] honeypot_bind_lists: Configure the service.See the following `Block HoneypotBindList`.
        :param pulumi.Input[bool] ping: Ping scan detection. Value: **true**: Enable **false**: Disabled
        :param pulumi.Input[str] probe_version: The version of the probe.
        :param pulumi.Input[str] proxy_ip: The IP address of the proxy.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] service_ip_lists: Listen to the IP address list.
        :param pulumi.Input[str] uuid: Machine uuid, **probe_type** is `host_probe`. This value cannot be empty.
        :param pulumi.Input[str] vpc_id: The ID of the VPC. **probe_type** is `vpc_black_hole_probe`. This value cannot be empty.
        """
        pulumi.set(__self__, "control_node_id", control_node_id)
        pulumi.set(__self__, "display_name", display_name)
        pulumi.set(__self__, "probe_type", probe_type)
        if arp is not None:
            pulumi.set(__self__, "arp", arp)
        if honeypot_bind_lists is not None:
            pulumi.set(__self__, "honeypot_bind_lists", honeypot_bind_lists)
        if ping is not None:
            pulumi.set(__self__, "ping", ping)
        if probe_version is not None:
            pulumi.set(__self__, "probe_version", probe_version)
        if proxy_ip is not None:
            pulumi.set(__self__, "proxy_ip", proxy_ip)
        if service_ip_lists is not None:
            pulumi.set(__self__, "service_ip_lists", service_ip_lists)
        if uuid is not None:
            pulumi.set(__self__, "uuid", uuid)
        if vpc_id is not None:
            pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter(name="controlNodeId")
    def control_node_id(self) -> pulumi.Input[str]:
        """
        The ID of the management node.
        """
        return pulumi.get(self, "control_node_id")

    @control_node_id.setter
    def control_node_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "control_node_id", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Input[str]:
        """
        Probe display name.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter(name="probeType")
    def probe_type(self) -> pulumi.Input[str]:
        """
        Probe type, support `host_probe` and `vpc_black_hole_probe`.
        """
        return pulumi.get(self, "probe_type")

    @probe_type.setter
    def probe_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "probe_type", value)

    @property
    @pulumi.getter
    def arp(self) -> Optional[pulumi.Input[bool]]:
        """
        ARP spoofing detection.**true**: Enable **false**: Disabled
        """
        return pulumi.get(self, "arp")

    @arp.setter
    def arp(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "arp", value)

    @property
    @pulumi.getter(name="honeypotBindLists")
    def honeypot_bind_lists(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['HoneypotProbeHoneypotBindListArgs']]]]:
        """
        Configure the service.See the following `Block HoneypotBindList`.
        """
        return pulumi.get(self, "honeypot_bind_lists")

    @honeypot_bind_lists.setter
    def honeypot_bind_lists(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['HoneypotProbeHoneypotBindListArgs']]]]):
        pulumi.set(self, "honeypot_bind_lists", value)

    @property
    @pulumi.getter
    def ping(self) -> Optional[pulumi.Input[bool]]:
        """
        Ping scan detection. Value: **true**: Enable **false**: Disabled
        """
        return pulumi.get(self, "ping")

    @ping.setter
    def ping(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "ping", value)

    @property
    @pulumi.getter(name="probeVersion")
    def probe_version(self) -> Optional[pulumi.Input[str]]:
        """
        The version of the probe.
        """
        return pulumi.get(self, "probe_version")

    @probe_version.setter
    def probe_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "probe_version", value)

    @property
    @pulumi.getter(name="proxyIp")
    def proxy_ip(self) -> Optional[pulumi.Input[str]]:
        """
        The IP address of the proxy.
        """
        return pulumi.get(self, "proxy_ip")

    @proxy_ip.setter
    def proxy_ip(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "proxy_ip", value)

    @property
    @pulumi.getter(name="serviceIpLists")
    def service_ip_lists(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Listen to the IP address list.
        """
        return pulumi.get(self, "service_ip_lists")

    @service_ip_lists.setter
    def service_ip_lists(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "service_ip_lists", value)

    @property
    @pulumi.getter
    def uuid(self) -> Optional[pulumi.Input[str]]:
        """
        Machine uuid, **probe_type** is `host_probe`. This value cannot be empty.
        """
        return pulumi.get(self, "uuid")

    @uuid.setter
    def uuid(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "uuid", value)

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the VPC. **probe_type** is `vpc_black_hole_probe`. This value cannot be empty.
        """
        return pulumi.get(self, "vpc_id")

    @vpc_id.setter
    def vpc_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vpc_id", value)


@pulumi.input_type
class _HoneypotProbeState:
    def __init__(__self__, *,
                 arp: Optional[pulumi.Input[bool]] = None,
                 control_node_id: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 honeypot_bind_lists: Optional[pulumi.Input[Sequence[pulumi.Input['HoneypotProbeHoneypotBindListArgs']]]] = None,
                 honeypot_probe_id: Optional[pulumi.Input[str]] = None,
                 ping: Optional[pulumi.Input[bool]] = None,
                 probe_type: Optional[pulumi.Input[str]] = None,
                 probe_version: Optional[pulumi.Input[str]] = None,
                 proxy_ip: Optional[pulumi.Input[str]] = None,
                 service_ip_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 uuid: Optional[pulumi.Input[str]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering HoneypotProbe resources.
        :param pulumi.Input[bool] arp: ARP spoofing detection.**true**: Enable **false**: Disabled
        :param pulumi.Input[str] control_node_id: The ID of the management node.
        :param pulumi.Input[str] display_name: Probe display name.
        :param pulumi.Input[Sequence[pulumi.Input['HoneypotProbeHoneypotBindListArgs']]] honeypot_bind_lists: Configure the service.See the following `Block HoneypotBindList`.
        :param pulumi.Input[str] honeypot_probe_id: The first ID of the resource
        :param pulumi.Input[bool] ping: Ping scan detection. Value: **true**: Enable **false**: Disabled
        :param pulumi.Input[str] probe_type: Probe type, support `host_probe` and `vpc_black_hole_probe`.
        :param pulumi.Input[str] probe_version: The version of the probe.
        :param pulumi.Input[str] proxy_ip: The IP address of the proxy.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] service_ip_lists: Listen to the IP address list.
        :param pulumi.Input[str] status: The status of the resource
        :param pulumi.Input[str] uuid: Machine uuid, **probe_type** is `host_probe`. This value cannot be empty.
        :param pulumi.Input[str] vpc_id: The ID of the VPC. **probe_type** is `vpc_black_hole_probe`. This value cannot be empty.
        """
        if arp is not None:
            pulumi.set(__self__, "arp", arp)
        if control_node_id is not None:
            pulumi.set(__self__, "control_node_id", control_node_id)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if honeypot_bind_lists is not None:
            pulumi.set(__self__, "honeypot_bind_lists", honeypot_bind_lists)
        if honeypot_probe_id is not None:
            pulumi.set(__self__, "honeypot_probe_id", honeypot_probe_id)
        if ping is not None:
            pulumi.set(__self__, "ping", ping)
        if probe_type is not None:
            pulumi.set(__self__, "probe_type", probe_type)
        if probe_version is not None:
            pulumi.set(__self__, "probe_version", probe_version)
        if proxy_ip is not None:
            pulumi.set(__self__, "proxy_ip", proxy_ip)
        if service_ip_lists is not None:
            pulumi.set(__self__, "service_ip_lists", service_ip_lists)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if uuid is not None:
            pulumi.set(__self__, "uuid", uuid)
        if vpc_id is not None:
            pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter
    def arp(self) -> Optional[pulumi.Input[bool]]:
        """
        ARP spoofing detection.**true**: Enable **false**: Disabled
        """
        return pulumi.get(self, "arp")

    @arp.setter
    def arp(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "arp", value)

    @property
    @pulumi.getter(name="controlNodeId")
    def control_node_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the management node.
        """
        return pulumi.get(self, "control_node_id")

    @control_node_id.setter
    def control_node_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "control_node_id", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        Probe display name.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter(name="honeypotBindLists")
    def honeypot_bind_lists(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['HoneypotProbeHoneypotBindListArgs']]]]:
        """
        Configure the service.See the following `Block HoneypotBindList`.
        """
        return pulumi.get(self, "honeypot_bind_lists")

    @honeypot_bind_lists.setter
    def honeypot_bind_lists(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['HoneypotProbeHoneypotBindListArgs']]]]):
        pulumi.set(self, "honeypot_bind_lists", value)

    @property
    @pulumi.getter(name="honeypotProbeId")
    def honeypot_probe_id(self) -> Optional[pulumi.Input[str]]:
        """
        The first ID of the resource
        """
        return pulumi.get(self, "honeypot_probe_id")

    @honeypot_probe_id.setter
    def honeypot_probe_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "honeypot_probe_id", value)

    @property
    @pulumi.getter
    def ping(self) -> Optional[pulumi.Input[bool]]:
        """
        Ping scan detection. Value: **true**: Enable **false**: Disabled
        """
        return pulumi.get(self, "ping")

    @ping.setter
    def ping(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "ping", value)

    @property
    @pulumi.getter(name="probeType")
    def probe_type(self) -> Optional[pulumi.Input[str]]:
        """
        Probe type, support `host_probe` and `vpc_black_hole_probe`.
        """
        return pulumi.get(self, "probe_type")

    @probe_type.setter
    def probe_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "probe_type", value)

    @property
    @pulumi.getter(name="probeVersion")
    def probe_version(self) -> Optional[pulumi.Input[str]]:
        """
        The version of the probe.
        """
        return pulumi.get(self, "probe_version")

    @probe_version.setter
    def probe_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "probe_version", value)

    @property
    @pulumi.getter(name="proxyIp")
    def proxy_ip(self) -> Optional[pulumi.Input[str]]:
        """
        The IP address of the proxy.
        """
        return pulumi.get(self, "proxy_ip")

    @proxy_ip.setter
    def proxy_ip(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "proxy_ip", value)

    @property
    @pulumi.getter(name="serviceIpLists")
    def service_ip_lists(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Listen to the IP address list.
        """
        return pulumi.get(self, "service_ip_lists")

    @service_ip_lists.setter
    def service_ip_lists(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "service_ip_lists", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the resource
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def uuid(self) -> Optional[pulumi.Input[str]]:
        """
        Machine uuid, **probe_type** is `host_probe`. This value cannot be empty.
        """
        return pulumi.get(self, "uuid")

    @uuid.setter
    def uuid(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "uuid", value)

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the VPC. **probe_type** is `vpc_black_hole_probe`. This value cannot be empty.
        """
        return pulumi.get(self, "vpc_id")

    @vpc_id.setter
    def vpc_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vpc_id", value)


class HoneypotProbe(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 arp: Optional[pulumi.Input[bool]] = None,
                 control_node_id: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 honeypot_bind_lists: Optional[pulumi.Input[Sequence[pulumi.Input[Union['HoneypotProbeHoneypotBindListArgs', 'HoneypotProbeHoneypotBindListArgsDict']]]]] = None,
                 ping: Optional[pulumi.Input[bool]] = None,
                 probe_type: Optional[pulumi.Input[str]] = None,
                 probe_version: Optional[pulumi.Input[str]] = None,
                 proxy_ip: Optional[pulumi.Input[str]] = None,
                 service_ip_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 uuid: Optional[pulumi.Input[str]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Threat Detection Honeypot Probe resource.

        For information about Threat Detection Honeypot Probe and how to use it, see [What is Honeypot Probe](https://www.alibabacloud.com/help/en/security-center/developer-reference/api-sas-2018-12-03-createhoneypotprobe).

        > **NOTE:** Available in v1.195.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default = alicloud.threatdetection.HoneypotProbe("default",
            uuid="032b618f-b220-4a0d-bd37-fbdc6ef58b6a",
            probe_type="host_probe",
            control_node_id="a44e1ab3-6945-444c-889d-5bacee7056e8",
            ping=True,
            honeypot_bind_lists=[{
                "bind_port_lists": [{
                    "start_port": 80,
                    "end_port": 80,
                }],
                "honeypot_id": "ede59ccdb1b7a2e21735d4593a6eb5ed31883af320c5ab63ab33818e94307be9",
            }],
            display_name="apispec",
            arp=True)
        ```

        ## Import

        Threat Detection Honeypot Probe can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:threatdetection/honeypotProbe:HoneypotProbe example <id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] arp: ARP spoofing detection.**true**: Enable **false**: Disabled
        :param pulumi.Input[str] control_node_id: The ID of the management node.
        :param pulumi.Input[str] display_name: Probe display name.
        :param pulumi.Input[Sequence[pulumi.Input[Union['HoneypotProbeHoneypotBindListArgs', 'HoneypotProbeHoneypotBindListArgsDict']]]] honeypot_bind_lists: Configure the service.See the following `Block HoneypotBindList`.
        :param pulumi.Input[bool] ping: Ping scan detection. Value: **true**: Enable **false**: Disabled
        :param pulumi.Input[str] probe_type: Probe type, support `host_probe` and `vpc_black_hole_probe`.
        :param pulumi.Input[str] probe_version: The version of the probe.
        :param pulumi.Input[str] proxy_ip: The IP address of the proxy.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] service_ip_lists: Listen to the IP address list.
        :param pulumi.Input[str] uuid: Machine uuid, **probe_type** is `host_probe`. This value cannot be empty.
        :param pulumi.Input[str] vpc_id: The ID of the VPC. **probe_type** is `vpc_black_hole_probe`. This value cannot be empty.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: HoneypotProbeArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Threat Detection Honeypot Probe resource.

        For information about Threat Detection Honeypot Probe and how to use it, see [What is Honeypot Probe](https://www.alibabacloud.com/help/en/security-center/developer-reference/api-sas-2018-12-03-createhoneypotprobe).

        > **NOTE:** Available in v1.195.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default = alicloud.threatdetection.HoneypotProbe("default",
            uuid="032b618f-b220-4a0d-bd37-fbdc6ef58b6a",
            probe_type="host_probe",
            control_node_id="a44e1ab3-6945-444c-889d-5bacee7056e8",
            ping=True,
            honeypot_bind_lists=[{
                "bind_port_lists": [{
                    "start_port": 80,
                    "end_port": 80,
                }],
                "honeypot_id": "ede59ccdb1b7a2e21735d4593a6eb5ed31883af320c5ab63ab33818e94307be9",
            }],
            display_name="apispec",
            arp=True)
        ```

        ## Import

        Threat Detection Honeypot Probe can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:threatdetection/honeypotProbe:HoneypotProbe example <id>
        ```

        :param str resource_name: The name of the resource.
        :param HoneypotProbeArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(HoneypotProbeArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 arp: Optional[pulumi.Input[bool]] = None,
                 control_node_id: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 honeypot_bind_lists: Optional[pulumi.Input[Sequence[pulumi.Input[Union['HoneypotProbeHoneypotBindListArgs', 'HoneypotProbeHoneypotBindListArgsDict']]]]] = None,
                 ping: Optional[pulumi.Input[bool]] = None,
                 probe_type: Optional[pulumi.Input[str]] = None,
                 probe_version: Optional[pulumi.Input[str]] = None,
                 proxy_ip: Optional[pulumi.Input[str]] = None,
                 service_ip_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 uuid: Optional[pulumi.Input[str]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = HoneypotProbeArgs.__new__(HoneypotProbeArgs)

            __props__.__dict__["arp"] = arp
            if control_node_id is None and not opts.urn:
                raise TypeError("Missing required property 'control_node_id'")
            __props__.__dict__["control_node_id"] = control_node_id
            if display_name is None and not opts.urn:
                raise TypeError("Missing required property 'display_name'")
            __props__.__dict__["display_name"] = display_name
            __props__.__dict__["honeypot_bind_lists"] = honeypot_bind_lists
            __props__.__dict__["ping"] = ping
            if probe_type is None and not opts.urn:
                raise TypeError("Missing required property 'probe_type'")
            __props__.__dict__["probe_type"] = probe_type
            __props__.__dict__["probe_version"] = probe_version
            __props__.__dict__["proxy_ip"] = proxy_ip
            __props__.__dict__["service_ip_lists"] = service_ip_lists
            __props__.__dict__["uuid"] = uuid
            __props__.__dict__["vpc_id"] = vpc_id
            __props__.__dict__["honeypot_probe_id"] = None
            __props__.__dict__["status"] = None
        super(HoneypotProbe, __self__).__init__(
            'alicloud:threatdetection/honeypotProbe:HoneypotProbe',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arp: Optional[pulumi.Input[bool]] = None,
            control_node_id: Optional[pulumi.Input[str]] = None,
            display_name: Optional[pulumi.Input[str]] = None,
            honeypot_bind_lists: Optional[pulumi.Input[Sequence[pulumi.Input[Union['HoneypotProbeHoneypotBindListArgs', 'HoneypotProbeHoneypotBindListArgsDict']]]]] = None,
            honeypot_probe_id: Optional[pulumi.Input[str]] = None,
            ping: Optional[pulumi.Input[bool]] = None,
            probe_type: Optional[pulumi.Input[str]] = None,
            probe_version: Optional[pulumi.Input[str]] = None,
            proxy_ip: Optional[pulumi.Input[str]] = None,
            service_ip_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            status: Optional[pulumi.Input[str]] = None,
            uuid: Optional[pulumi.Input[str]] = None,
            vpc_id: Optional[pulumi.Input[str]] = None) -> 'HoneypotProbe':
        """
        Get an existing HoneypotProbe resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] arp: ARP spoofing detection.**true**: Enable **false**: Disabled
        :param pulumi.Input[str] control_node_id: The ID of the management node.
        :param pulumi.Input[str] display_name: Probe display name.
        :param pulumi.Input[Sequence[pulumi.Input[Union['HoneypotProbeHoneypotBindListArgs', 'HoneypotProbeHoneypotBindListArgsDict']]]] honeypot_bind_lists: Configure the service.See the following `Block HoneypotBindList`.
        :param pulumi.Input[str] honeypot_probe_id: The first ID of the resource
        :param pulumi.Input[bool] ping: Ping scan detection. Value: **true**: Enable **false**: Disabled
        :param pulumi.Input[str] probe_type: Probe type, support `host_probe` and `vpc_black_hole_probe`.
        :param pulumi.Input[str] probe_version: The version of the probe.
        :param pulumi.Input[str] proxy_ip: The IP address of the proxy.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] service_ip_lists: Listen to the IP address list.
        :param pulumi.Input[str] status: The status of the resource
        :param pulumi.Input[str] uuid: Machine uuid, **probe_type** is `host_probe`. This value cannot be empty.
        :param pulumi.Input[str] vpc_id: The ID of the VPC. **probe_type** is `vpc_black_hole_probe`. This value cannot be empty.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _HoneypotProbeState.__new__(_HoneypotProbeState)

        __props__.__dict__["arp"] = arp
        __props__.__dict__["control_node_id"] = control_node_id
        __props__.__dict__["display_name"] = display_name
        __props__.__dict__["honeypot_bind_lists"] = honeypot_bind_lists
        __props__.__dict__["honeypot_probe_id"] = honeypot_probe_id
        __props__.__dict__["ping"] = ping
        __props__.__dict__["probe_type"] = probe_type
        __props__.__dict__["probe_version"] = probe_version
        __props__.__dict__["proxy_ip"] = proxy_ip
        __props__.__dict__["service_ip_lists"] = service_ip_lists
        __props__.__dict__["status"] = status
        __props__.__dict__["uuid"] = uuid
        __props__.__dict__["vpc_id"] = vpc_id
        return HoneypotProbe(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arp(self) -> pulumi.Output[Optional[bool]]:
        """
        ARP spoofing detection.**true**: Enable **false**: Disabled
        """
        return pulumi.get(self, "arp")

    @property
    @pulumi.getter(name="controlNodeId")
    def control_node_id(self) -> pulumi.Output[str]:
        """
        The ID of the management node.
        """
        return pulumi.get(self, "control_node_id")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        Probe display name.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="honeypotBindLists")
    def honeypot_bind_lists(self) -> pulumi.Output[Optional[Sequence['outputs.HoneypotProbeHoneypotBindList']]]:
        """
        Configure the service.See the following `Block HoneypotBindList`.
        """
        return pulumi.get(self, "honeypot_bind_lists")

    @property
    @pulumi.getter(name="honeypotProbeId")
    def honeypot_probe_id(self) -> pulumi.Output[str]:
        """
        The first ID of the resource
        """
        return pulumi.get(self, "honeypot_probe_id")

    @property
    @pulumi.getter
    def ping(self) -> pulumi.Output[Optional[bool]]:
        """
        Ping scan detection. Value: **true**: Enable **false**: Disabled
        """
        return pulumi.get(self, "ping")

    @property
    @pulumi.getter(name="probeType")
    def probe_type(self) -> pulumi.Output[str]:
        """
        Probe type, support `host_probe` and `vpc_black_hole_probe`.
        """
        return pulumi.get(self, "probe_type")

    @property
    @pulumi.getter(name="probeVersion")
    def probe_version(self) -> pulumi.Output[str]:
        """
        The version of the probe.
        """
        return pulumi.get(self, "probe_version")

    @property
    @pulumi.getter(name="proxyIp")
    def proxy_ip(self) -> pulumi.Output[Optional[str]]:
        """
        The IP address of the proxy.
        """
        return pulumi.get(self, "proxy_ip")

    @property
    @pulumi.getter(name="serviceIpLists")
    def service_ip_lists(self) -> pulumi.Output[Sequence[str]]:
        """
        Listen to the IP address list.
        """
        return pulumi.get(self, "service_ip_lists")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The status of the resource
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def uuid(self) -> pulumi.Output[Optional[str]]:
        """
        Machine uuid, **probe_type** is `host_probe`. This value cannot be empty.
        """
        return pulumi.get(self, "uuid")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the VPC. **probe_type** is `vpc_black_hole_probe`. This value cannot be empty.
        """
        return pulumi.get(self, "vpc_id")

