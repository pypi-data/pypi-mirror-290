# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['AcceleratorSpareIpAttachmentArgs', 'AcceleratorSpareIpAttachment']

@pulumi.input_type
class AcceleratorSpareIpAttachmentArgs:
    def __init__(__self__, *,
                 accelerator_id: pulumi.Input[str],
                 spare_ip: pulumi.Input[str],
                 dry_run: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a AcceleratorSpareIpAttachment resource.
        :param pulumi.Input[str] accelerator_id: The ID of the global acceleration instance.
        :param pulumi.Input[str] spare_ip: The standby IP address of CNAME. When the acceleration area is abnormal, the traffic is switched to the standby IP address.
        :param pulumi.Input[bool] dry_run: The dry run.
        """
        pulumi.set(__self__, "accelerator_id", accelerator_id)
        pulumi.set(__self__, "spare_ip", spare_ip)
        if dry_run is not None:
            pulumi.set(__self__, "dry_run", dry_run)

    @property
    @pulumi.getter(name="acceleratorId")
    def accelerator_id(self) -> pulumi.Input[str]:
        """
        The ID of the global acceleration instance.
        """
        return pulumi.get(self, "accelerator_id")

    @accelerator_id.setter
    def accelerator_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "accelerator_id", value)

    @property
    @pulumi.getter(name="spareIp")
    def spare_ip(self) -> pulumi.Input[str]:
        """
        The standby IP address of CNAME. When the acceleration area is abnormal, the traffic is switched to the standby IP address.
        """
        return pulumi.get(self, "spare_ip")

    @spare_ip.setter
    def spare_ip(self, value: pulumi.Input[str]):
        pulumi.set(self, "spare_ip", value)

    @property
    @pulumi.getter(name="dryRun")
    def dry_run(self) -> Optional[pulumi.Input[bool]]:
        """
        The dry run.
        """
        return pulumi.get(self, "dry_run")

    @dry_run.setter
    def dry_run(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "dry_run", value)


@pulumi.input_type
class _AcceleratorSpareIpAttachmentState:
    def __init__(__self__, *,
                 accelerator_id: Optional[pulumi.Input[str]] = None,
                 dry_run: Optional[pulumi.Input[bool]] = None,
                 spare_ip: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AcceleratorSpareIpAttachment resources.
        :param pulumi.Input[str] accelerator_id: The ID of the global acceleration instance.
        :param pulumi.Input[bool] dry_run: The dry run.
        :param pulumi.Input[str] spare_ip: The standby IP address of CNAME. When the acceleration area is abnormal, the traffic is switched to the standby IP address.
        :param pulumi.Input[str] status: The status of the standby CNAME IP address.
        """
        if accelerator_id is not None:
            pulumi.set(__self__, "accelerator_id", accelerator_id)
        if dry_run is not None:
            pulumi.set(__self__, "dry_run", dry_run)
        if spare_ip is not None:
            pulumi.set(__self__, "spare_ip", spare_ip)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="acceleratorId")
    def accelerator_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the global acceleration instance.
        """
        return pulumi.get(self, "accelerator_id")

    @accelerator_id.setter
    def accelerator_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "accelerator_id", value)

    @property
    @pulumi.getter(name="dryRun")
    def dry_run(self) -> Optional[pulumi.Input[bool]]:
        """
        The dry run.
        """
        return pulumi.get(self, "dry_run")

    @dry_run.setter
    def dry_run(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "dry_run", value)

    @property
    @pulumi.getter(name="spareIp")
    def spare_ip(self) -> Optional[pulumi.Input[str]]:
        """
        The standby IP address of CNAME. When the acceleration area is abnormal, the traffic is switched to the standby IP address.
        """
        return pulumi.get(self, "spare_ip")

    @spare_ip.setter
    def spare_ip(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "spare_ip", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the standby CNAME IP address.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


class AcceleratorSpareIpAttachment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 accelerator_id: Optional[pulumi.Input[str]] = None,
                 dry_run: Optional[pulumi.Input[bool]] = None,
                 spare_ip: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Global Accelerator (GA) Accelerator Spare Ip Attachment resource.

        For information about Global Accelerator (GA) Accelerator Spare Ip Attachment and how to use it, see [What is Accelerator Spare Ip Attachment](https://www.alibabacloud.com/help/en/global-accelerator/latest/api-ga-2019-11-20-createspareips).

        > **NOTE:** Available since v1.167.0.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default = alicloud.ga.Accelerator("default",
            duration=1,
            spec="1",
            accelerator_name="terraform-example",
            auto_use_coupon=True,
            description="terraform-example")
        default_bandwidth_package = alicloud.ga.BandwidthPackage("default",
            bandwidth=100,
            type="Basic",
            bandwidth_type="Basic",
            payment_type="PayAsYouGo",
            billing_type="PayBy95",
            ratio=30,
            bandwidth_package_name="terraform-example",
            auto_pay=True,
            auto_use_coupon=True)
        default_bandwidth_package_attachment = alicloud.ga.BandwidthPackageAttachment("default",
            accelerator_id=default.id,
            bandwidth_package_id=default_bandwidth_package.id)
        default_accelerator_spare_ip_attachment = alicloud.ga.AcceleratorSpareIpAttachment("default",
            accelerator_id=default_bandwidth_package_attachment.accelerator_id,
            spare_ip="127.0.0.1")
        ```

        ## Import

        Global Accelerator (GA) Accelerator Spare Ip Attachment can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:ga/acceleratorSpareIpAttachment:AcceleratorSpareIpAttachment example <accelerator_id>:<spare_ip>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] accelerator_id: The ID of the global acceleration instance.
        :param pulumi.Input[bool] dry_run: The dry run.
        :param pulumi.Input[str] spare_ip: The standby IP address of CNAME. When the acceleration area is abnormal, the traffic is switched to the standby IP address.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AcceleratorSpareIpAttachmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Global Accelerator (GA) Accelerator Spare Ip Attachment resource.

        For information about Global Accelerator (GA) Accelerator Spare Ip Attachment and how to use it, see [What is Accelerator Spare Ip Attachment](https://www.alibabacloud.com/help/en/global-accelerator/latest/api-ga-2019-11-20-createspareips).

        > **NOTE:** Available since v1.167.0.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default = alicloud.ga.Accelerator("default",
            duration=1,
            spec="1",
            accelerator_name="terraform-example",
            auto_use_coupon=True,
            description="terraform-example")
        default_bandwidth_package = alicloud.ga.BandwidthPackage("default",
            bandwidth=100,
            type="Basic",
            bandwidth_type="Basic",
            payment_type="PayAsYouGo",
            billing_type="PayBy95",
            ratio=30,
            bandwidth_package_name="terraform-example",
            auto_pay=True,
            auto_use_coupon=True)
        default_bandwidth_package_attachment = alicloud.ga.BandwidthPackageAttachment("default",
            accelerator_id=default.id,
            bandwidth_package_id=default_bandwidth_package.id)
        default_accelerator_spare_ip_attachment = alicloud.ga.AcceleratorSpareIpAttachment("default",
            accelerator_id=default_bandwidth_package_attachment.accelerator_id,
            spare_ip="127.0.0.1")
        ```

        ## Import

        Global Accelerator (GA) Accelerator Spare Ip Attachment can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:ga/acceleratorSpareIpAttachment:AcceleratorSpareIpAttachment example <accelerator_id>:<spare_ip>
        ```

        :param str resource_name: The name of the resource.
        :param AcceleratorSpareIpAttachmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AcceleratorSpareIpAttachmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 accelerator_id: Optional[pulumi.Input[str]] = None,
                 dry_run: Optional[pulumi.Input[bool]] = None,
                 spare_ip: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AcceleratorSpareIpAttachmentArgs.__new__(AcceleratorSpareIpAttachmentArgs)

            if accelerator_id is None and not opts.urn:
                raise TypeError("Missing required property 'accelerator_id'")
            __props__.__dict__["accelerator_id"] = accelerator_id
            __props__.__dict__["dry_run"] = dry_run
            if spare_ip is None and not opts.urn:
                raise TypeError("Missing required property 'spare_ip'")
            __props__.__dict__["spare_ip"] = spare_ip
            __props__.__dict__["status"] = None
        super(AcceleratorSpareIpAttachment, __self__).__init__(
            'alicloud:ga/acceleratorSpareIpAttachment:AcceleratorSpareIpAttachment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            accelerator_id: Optional[pulumi.Input[str]] = None,
            dry_run: Optional[pulumi.Input[bool]] = None,
            spare_ip: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None) -> 'AcceleratorSpareIpAttachment':
        """
        Get an existing AcceleratorSpareIpAttachment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] accelerator_id: The ID of the global acceleration instance.
        :param pulumi.Input[bool] dry_run: The dry run.
        :param pulumi.Input[str] spare_ip: The standby IP address of CNAME. When the acceleration area is abnormal, the traffic is switched to the standby IP address.
        :param pulumi.Input[str] status: The status of the standby CNAME IP address.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AcceleratorSpareIpAttachmentState.__new__(_AcceleratorSpareIpAttachmentState)

        __props__.__dict__["accelerator_id"] = accelerator_id
        __props__.__dict__["dry_run"] = dry_run
        __props__.__dict__["spare_ip"] = spare_ip
        __props__.__dict__["status"] = status
        return AcceleratorSpareIpAttachment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="acceleratorId")
    def accelerator_id(self) -> pulumi.Output[str]:
        """
        The ID of the global acceleration instance.
        """
        return pulumi.get(self, "accelerator_id")

    @property
    @pulumi.getter(name="dryRun")
    def dry_run(self) -> pulumi.Output[Optional[bool]]:
        """
        The dry run.
        """
        return pulumi.get(self, "dry_run")

    @property
    @pulumi.getter(name="spareIp")
    def spare_ip(self) -> pulumi.Output[str]:
        """
        The standby IP address of CNAME. When the acceleration area is abnormal, the traffic is switched to the standby IP address.
        """
        return pulumi.get(self, "spare_ip")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The status of the standby CNAME IP address.
        """
        return pulumi.get(self, "status")

