# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['AclEntryAttachmentArgs', 'AclEntryAttachment']

@pulumi.input_type
class AclEntryAttachmentArgs:
    def __init__(__self__, *,
                 acl_id: pulumi.Input[str],
                 entry: pulumi.Input[str],
                 entry_description: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a AclEntryAttachment resource.
        :param pulumi.Input[str] acl_id: The ID of the global acceleration instance.
        :param pulumi.Input[str] entry: The IP address(192.168.XX.XX) or CIDR(10.0.XX.XX/24) block that you want to add to the network ACL.
        :param pulumi.Input[str] entry_description: The description of the entry. The description must be 1 to 256 characters in length, and can contain letters, digits, hyphens (-), forward slashes (/), periods (.), and underscores (_).
        """
        pulumi.set(__self__, "acl_id", acl_id)
        pulumi.set(__self__, "entry", entry)
        if entry_description is not None:
            pulumi.set(__self__, "entry_description", entry_description)

    @property
    @pulumi.getter(name="aclId")
    def acl_id(self) -> pulumi.Input[str]:
        """
        The ID of the global acceleration instance.
        """
        return pulumi.get(self, "acl_id")

    @acl_id.setter
    def acl_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "acl_id", value)

    @property
    @pulumi.getter
    def entry(self) -> pulumi.Input[str]:
        """
        The IP address(192.168.XX.XX) or CIDR(10.0.XX.XX/24) block that you want to add to the network ACL.
        """
        return pulumi.get(self, "entry")

    @entry.setter
    def entry(self, value: pulumi.Input[str]):
        pulumi.set(self, "entry", value)

    @property
    @pulumi.getter(name="entryDescription")
    def entry_description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the entry. The description must be 1 to 256 characters in length, and can contain letters, digits, hyphens (-), forward slashes (/), periods (.), and underscores (_).
        """
        return pulumi.get(self, "entry_description")

    @entry_description.setter
    def entry_description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "entry_description", value)


@pulumi.input_type
class _AclEntryAttachmentState:
    def __init__(__self__, *,
                 acl_id: Optional[pulumi.Input[str]] = None,
                 entry: Optional[pulumi.Input[str]] = None,
                 entry_description: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AclEntryAttachment resources.
        :param pulumi.Input[str] acl_id: The ID of the global acceleration instance.
        :param pulumi.Input[str] entry: The IP address(192.168.XX.XX) or CIDR(10.0.XX.XX/24) block that you want to add to the network ACL.
        :param pulumi.Input[str] entry_description: The description of the entry. The description must be 1 to 256 characters in length, and can contain letters, digits, hyphens (-), forward slashes (/), periods (.), and underscores (_).
        :param pulumi.Input[str] status: The status of the network ACL.
        """
        if acl_id is not None:
            pulumi.set(__self__, "acl_id", acl_id)
        if entry is not None:
            pulumi.set(__self__, "entry", entry)
        if entry_description is not None:
            pulumi.set(__self__, "entry_description", entry_description)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="aclId")
    def acl_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the global acceleration instance.
        """
        return pulumi.get(self, "acl_id")

    @acl_id.setter
    def acl_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "acl_id", value)

    @property
    @pulumi.getter
    def entry(self) -> Optional[pulumi.Input[str]]:
        """
        The IP address(192.168.XX.XX) or CIDR(10.0.XX.XX/24) block that you want to add to the network ACL.
        """
        return pulumi.get(self, "entry")

    @entry.setter
    def entry(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "entry", value)

    @property
    @pulumi.getter(name="entryDescription")
    def entry_description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the entry. The description must be 1 to 256 characters in length, and can contain letters, digits, hyphens (-), forward slashes (/), periods (.), and underscores (_).
        """
        return pulumi.get(self, "entry_description")

    @entry_description.setter
    def entry_description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "entry_description", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the network ACL.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


class AclEntryAttachment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 acl_id: Optional[pulumi.Input[str]] = None,
                 entry: Optional[pulumi.Input[str]] = None,
                 entry_description: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Global Accelerator (GA) Acl entry attachment resource.

        For information about Global Accelerator (GA) Acl entry attachment and how to use it, see [What is Acl entry attachment](https://www.alibabacloud.com/help/en/global-accelerator/latest/api-ga-2019-11-20-addentriestoacl).

        > **NOTE:** Available since v1.190.0.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default = alicloud.ga.Acl("default",
            acl_name="tf-example-value",
            address_ip_version="IPv4")
        default_acl_entry_attachment = alicloud.ga.AclEntryAttachment("default",
            acl_id=default.id,
            entry="192.168.1.1/32",
            entry_description="tf-example-value")
        ```

        ## Import

        Global Accelerator (GA) Acl entry attachment can be imported using the id.Format to `<acl_id>:<entry>`, e.g.

        ```sh
        $ pulumi import alicloud:ga/aclEntryAttachment:AclEntryAttachment example your_acl_id:your_entry
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] acl_id: The ID of the global acceleration instance.
        :param pulumi.Input[str] entry: The IP address(192.168.XX.XX) or CIDR(10.0.XX.XX/24) block that you want to add to the network ACL.
        :param pulumi.Input[str] entry_description: The description of the entry. The description must be 1 to 256 characters in length, and can contain letters, digits, hyphens (-), forward slashes (/), periods (.), and underscores (_).
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AclEntryAttachmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Global Accelerator (GA) Acl entry attachment resource.

        For information about Global Accelerator (GA) Acl entry attachment and how to use it, see [What is Acl entry attachment](https://www.alibabacloud.com/help/en/global-accelerator/latest/api-ga-2019-11-20-addentriestoacl).

        > **NOTE:** Available since v1.190.0.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default = alicloud.ga.Acl("default",
            acl_name="tf-example-value",
            address_ip_version="IPv4")
        default_acl_entry_attachment = alicloud.ga.AclEntryAttachment("default",
            acl_id=default.id,
            entry="192.168.1.1/32",
            entry_description="tf-example-value")
        ```

        ## Import

        Global Accelerator (GA) Acl entry attachment can be imported using the id.Format to `<acl_id>:<entry>`, e.g.

        ```sh
        $ pulumi import alicloud:ga/aclEntryAttachment:AclEntryAttachment example your_acl_id:your_entry
        ```

        :param str resource_name: The name of the resource.
        :param AclEntryAttachmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AclEntryAttachmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 acl_id: Optional[pulumi.Input[str]] = None,
                 entry: Optional[pulumi.Input[str]] = None,
                 entry_description: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AclEntryAttachmentArgs.__new__(AclEntryAttachmentArgs)

            if acl_id is None and not opts.urn:
                raise TypeError("Missing required property 'acl_id'")
            __props__.__dict__["acl_id"] = acl_id
            if entry is None and not opts.urn:
                raise TypeError("Missing required property 'entry'")
            __props__.__dict__["entry"] = entry
            __props__.__dict__["entry_description"] = entry_description
            __props__.__dict__["status"] = None
        super(AclEntryAttachment, __self__).__init__(
            'alicloud:ga/aclEntryAttachment:AclEntryAttachment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            acl_id: Optional[pulumi.Input[str]] = None,
            entry: Optional[pulumi.Input[str]] = None,
            entry_description: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None) -> 'AclEntryAttachment':
        """
        Get an existing AclEntryAttachment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] acl_id: The ID of the global acceleration instance.
        :param pulumi.Input[str] entry: The IP address(192.168.XX.XX) or CIDR(10.0.XX.XX/24) block that you want to add to the network ACL.
        :param pulumi.Input[str] entry_description: The description of the entry. The description must be 1 to 256 characters in length, and can contain letters, digits, hyphens (-), forward slashes (/), periods (.), and underscores (_).
        :param pulumi.Input[str] status: The status of the network ACL.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AclEntryAttachmentState.__new__(_AclEntryAttachmentState)

        __props__.__dict__["acl_id"] = acl_id
        __props__.__dict__["entry"] = entry
        __props__.__dict__["entry_description"] = entry_description
        __props__.__dict__["status"] = status
        return AclEntryAttachment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="aclId")
    def acl_id(self) -> pulumi.Output[str]:
        """
        The ID of the global acceleration instance.
        """
        return pulumi.get(self, "acl_id")

    @property
    @pulumi.getter
    def entry(self) -> pulumi.Output[str]:
        """
        The IP address(192.168.XX.XX) or CIDR(10.0.XX.XX/24) block that you want to add to the network ACL.
        """
        return pulumi.get(self, "entry")

    @property
    @pulumi.getter(name="entryDescription")
    def entry_description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the entry. The description must be 1 to 256 characters in length, and can contain letters, digits, hyphens (-), forward slashes (/), periods (.), and underscores (_).
        """
        return pulumi.get(self, "entry_description")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The status of the network ACL.
        """
        return pulumi.get(self, "status")

