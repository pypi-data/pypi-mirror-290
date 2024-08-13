# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['FaceConfigArgs', 'FaceConfig']

@pulumi.input_type
class FaceConfigArgs:
    def __init__(__self__, *,
                 biz_name: pulumi.Input[str],
                 biz_type: pulumi.Input[str]):
        """
        The set of arguments for constructing a FaceConfig resource.
        :param pulumi.Input[str] biz_name: Scene name.
        :param pulumi.Input[str] biz_type: Scene type. **NOTE:** The biz_type cannot exceed 32 characters and can only use English letters, numbers and dashes (-).
        """
        pulumi.set(__self__, "biz_name", biz_name)
        pulumi.set(__self__, "biz_type", biz_type)

    @property
    @pulumi.getter(name="bizName")
    def biz_name(self) -> pulumi.Input[str]:
        """
        Scene name.
        """
        return pulumi.get(self, "biz_name")

    @biz_name.setter
    def biz_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "biz_name", value)

    @property
    @pulumi.getter(name="bizType")
    def biz_type(self) -> pulumi.Input[str]:
        """
        Scene type. **NOTE:** The biz_type cannot exceed 32 characters and can only use English letters, numbers and dashes (-).
        """
        return pulumi.get(self, "biz_type")

    @biz_type.setter
    def biz_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "biz_type", value)


@pulumi.input_type
class _FaceConfigState:
    def __init__(__self__, *,
                 biz_name: Optional[pulumi.Input[str]] = None,
                 biz_type: Optional[pulumi.Input[str]] = None,
                 gmt_modified: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering FaceConfig resources.
        :param pulumi.Input[str] biz_name: Scene name.
        :param pulumi.Input[str] biz_type: Scene type. **NOTE:** The biz_type cannot exceed 32 characters and can only use English letters, numbers and dashes (-).
        :param pulumi.Input[str] gmt_modified: Last Modified Date.
        """
        if biz_name is not None:
            pulumi.set(__self__, "biz_name", biz_name)
        if biz_type is not None:
            pulumi.set(__self__, "biz_type", biz_type)
        if gmt_modified is not None:
            pulumi.set(__self__, "gmt_modified", gmt_modified)

    @property
    @pulumi.getter(name="bizName")
    def biz_name(self) -> Optional[pulumi.Input[str]]:
        """
        Scene name.
        """
        return pulumi.get(self, "biz_name")

    @biz_name.setter
    def biz_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "biz_name", value)

    @property
    @pulumi.getter(name="bizType")
    def biz_type(self) -> Optional[pulumi.Input[str]]:
        """
        Scene type. **NOTE:** The biz_type cannot exceed 32 characters and can only use English letters, numbers and dashes (-).
        """
        return pulumi.get(self, "biz_type")

    @biz_type.setter
    def biz_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "biz_type", value)

    @property
    @pulumi.getter(name="gmtModified")
    def gmt_modified(self) -> Optional[pulumi.Input[str]]:
        """
        Last Modified Date.
        """
        return pulumi.get(self, "gmt_modified")

    @gmt_modified.setter
    def gmt_modified(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "gmt_modified", value)


class FaceConfig(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 biz_name: Optional[pulumi.Input[str]] = None,
                 biz_type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Cloudauth Face Config resource.

        For information about Cloudauth Face Config and how to use it, see [What is Face Config](https://help.aliyun.com/zh/id-verification/cloudauth/product-overview/end-of-integration-announcement-on-id-verification).

        > **NOTE:** Available since v1.137.0.

        > **NOTE:** In order to provide you with more perfect product capabilities, the real person certification service has stopped access, it is recommended that you use the upgraded version of the [real person certification financial real person certification service](https://help.aliyun.com/zh/id-verification/product-overview/what-is-id-verification-for-financial-services). Users that have access to real person authentication are not affected.

        ## Import

        Cloudauth Face Config can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:cloudauth/faceConfig:FaceConfig example <lang>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] biz_name: Scene name.
        :param pulumi.Input[str] biz_type: Scene type. **NOTE:** The biz_type cannot exceed 32 characters and can only use English letters, numbers and dashes (-).
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: FaceConfigArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Cloudauth Face Config resource.

        For information about Cloudauth Face Config and how to use it, see [What is Face Config](https://help.aliyun.com/zh/id-verification/cloudauth/product-overview/end-of-integration-announcement-on-id-verification).

        > **NOTE:** Available since v1.137.0.

        > **NOTE:** In order to provide you with more perfect product capabilities, the real person certification service has stopped access, it is recommended that you use the upgraded version of the [real person certification financial real person certification service](https://help.aliyun.com/zh/id-verification/product-overview/what-is-id-verification-for-financial-services). Users that have access to real person authentication are not affected.

        ## Import

        Cloudauth Face Config can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:cloudauth/faceConfig:FaceConfig example <lang>
        ```

        :param str resource_name: The name of the resource.
        :param FaceConfigArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(FaceConfigArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 biz_name: Optional[pulumi.Input[str]] = None,
                 biz_type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = FaceConfigArgs.__new__(FaceConfigArgs)

            if biz_name is None and not opts.urn:
                raise TypeError("Missing required property 'biz_name'")
            __props__.__dict__["biz_name"] = biz_name
            if biz_type is None and not opts.urn:
                raise TypeError("Missing required property 'biz_type'")
            __props__.__dict__["biz_type"] = biz_type
            __props__.__dict__["gmt_modified"] = None
        super(FaceConfig, __self__).__init__(
            'alicloud:cloudauth/faceConfig:FaceConfig',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            biz_name: Optional[pulumi.Input[str]] = None,
            biz_type: Optional[pulumi.Input[str]] = None,
            gmt_modified: Optional[pulumi.Input[str]] = None) -> 'FaceConfig':
        """
        Get an existing FaceConfig resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] biz_name: Scene name.
        :param pulumi.Input[str] biz_type: Scene type. **NOTE:** The biz_type cannot exceed 32 characters and can only use English letters, numbers and dashes (-).
        :param pulumi.Input[str] gmt_modified: Last Modified Date.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _FaceConfigState.__new__(_FaceConfigState)

        __props__.__dict__["biz_name"] = biz_name
        __props__.__dict__["biz_type"] = biz_type
        __props__.__dict__["gmt_modified"] = gmt_modified
        return FaceConfig(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="bizName")
    def biz_name(self) -> pulumi.Output[str]:
        """
        Scene name.
        """
        return pulumi.get(self, "biz_name")

    @property
    @pulumi.getter(name="bizType")
    def biz_type(self) -> pulumi.Output[str]:
        """
        Scene type. **NOTE:** The biz_type cannot exceed 32 characters and can only use English letters, numbers and dashes (-).
        """
        return pulumi.get(self, "biz_type")

    @property
    @pulumi.getter(name="gmtModified")
    def gmt_modified(self) -> pulumi.Output[str]:
        """
        Last Modified Date.
        """
        return pulumi.get(self, "gmt_modified")

