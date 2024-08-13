# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['BucketUserDefinedLogFieldsArgs', 'BucketUserDefinedLogFields']

@pulumi.input_type
class BucketUserDefinedLogFieldsArgs:
    def __init__(__self__, *,
                 bucket: pulumi.Input[str],
                 header_sets: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 param_sets: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a BucketUserDefinedLogFields resource.
        :param pulumi.Input[str] bucket: The name of the bucket.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] header_sets: Container for custom request header configuration information.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] param_sets: Container for custom request parameters configuration information.
        """
        pulumi.set(__self__, "bucket", bucket)
        if header_sets is not None:
            pulumi.set(__self__, "header_sets", header_sets)
        if param_sets is not None:
            pulumi.set(__self__, "param_sets", param_sets)

    @property
    @pulumi.getter
    def bucket(self) -> pulumi.Input[str]:
        """
        The name of the bucket.
        """
        return pulumi.get(self, "bucket")

    @bucket.setter
    def bucket(self, value: pulumi.Input[str]):
        pulumi.set(self, "bucket", value)

    @property
    @pulumi.getter(name="headerSets")
    def header_sets(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Container for custom request header configuration information.
        """
        return pulumi.get(self, "header_sets")

    @header_sets.setter
    def header_sets(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "header_sets", value)

    @property
    @pulumi.getter(name="paramSets")
    def param_sets(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Container for custom request parameters configuration information.
        """
        return pulumi.get(self, "param_sets")

    @param_sets.setter
    def param_sets(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "param_sets", value)


@pulumi.input_type
class _BucketUserDefinedLogFieldsState:
    def __init__(__self__, *,
                 bucket: Optional[pulumi.Input[str]] = None,
                 header_sets: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 param_sets: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering BucketUserDefinedLogFields resources.
        :param pulumi.Input[str] bucket: The name of the bucket.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] header_sets: Container for custom request header configuration information.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] param_sets: Container for custom request parameters configuration information.
        """
        if bucket is not None:
            pulumi.set(__self__, "bucket", bucket)
        if header_sets is not None:
            pulumi.set(__self__, "header_sets", header_sets)
        if param_sets is not None:
            pulumi.set(__self__, "param_sets", param_sets)

    @property
    @pulumi.getter
    def bucket(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the bucket.
        """
        return pulumi.get(self, "bucket")

    @bucket.setter
    def bucket(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bucket", value)

    @property
    @pulumi.getter(name="headerSets")
    def header_sets(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Container for custom request header configuration information.
        """
        return pulumi.get(self, "header_sets")

    @header_sets.setter
    def header_sets(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "header_sets", value)

    @property
    @pulumi.getter(name="paramSets")
    def param_sets(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Container for custom request parameters configuration information.
        """
        return pulumi.get(self, "param_sets")

    @param_sets.setter
    def param_sets(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "param_sets", value)


class BucketUserDefinedLogFields(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bucket: Optional[pulumi.Input[str]] = None,
                 header_sets: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 param_sets: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides a OSS Bucket User Defined Log Fields resource. Used to personalize the user_defined_log_fields field in the Bucket real-time log.

        For information about OSS Bucket User Defined Log Fields and how to use it, see [What is Bucket User Defined Log Fields](https://www.alibabacloud.com/help/en/oss/developer-reference/putuserdefinedlogfieldsconfig).

        > **NOTE:** Available since v1.224.0.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud
        import pulumi_random as random

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "terraform-example"
        default = random.index.Integer("default",
            min=10000,
            max=99999)
        create_bucket = alicloud.oss.Bucket("CreateBucket",
            storage_class="Standard",
            bucket=f"{name}-{default['result']}")
        default_bucket_user_defined_log_fields = alicloud.oss.BucketUserDefinedLogFields("default",
            bucket=create_bucket.bucket,
            param_sets=[
                "oss-example",
                "example-para",
                "abc",
            ],
            header_sets=[
                "def",
                "example-header",
            ])
        ```

        ## Import

        OSS Bucket User Defined Log Fields can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:oss/bucketUserDefinedLogFields:BucketUserDefinedLogFields example <id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: The name of the bucket.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] header_sets: Container for custom request header configuration information.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] param_sets: Container for custom request parameters configuration information.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BucketUserDefinedLogFieldsArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a OSS Bucket User Defined Log Fields resource. Used to personalize the user_defined_log_fields field in the Bucket real-time log.

        For information about OSS Bucket User Defined Log Fields and how to use it, see [What is Bucket User Defined Log Fields](https://www.alibabacloud.com/help/en/oss/developer-reference/putuserdefinedlogfieldsconfig).

        > **NOTE:** Available since v1.224.0.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud
        import pulumi_random as random

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "terraform-example"
        default = random.index.Integer("default",
            min=10000,
            max=99999)
        create_bucket = alicloud.oss.Bucket("CreateBucket",
            storage_class="Standard",
            bucket=f"{name}-{default['result']}")
        default_bucket_user_defined_log_fields = alicloud.oss.BucketUserDefinedLogFields("default",
            bucket=create_bucket.bucket,
            param_sets=[
                "oss-example",
                "example-para",
                "abc",
            ],
            header_sets=[
                "def",
                "example-header",
            ])
        ```

        ## Import

        OSS Bucket User Defined Log Fields can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:oss/bucketUserDefinedLogFields:BucketUserDefinedLogFields example <id>
        ```

        :param str resource_name: The name of the resource.
        :param BucketUserDefinedLogFieldsArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BucketUserDefinedLogFieldsArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bucket: Optional[pulumi.Input[str]] = None,
                 header_sets: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 param_sets: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BucketUserDefinedLogFieldsArgs.__new__(BucketUserDefinedLogFieldsArgs)

            if bucket is None and not opts.urn:
                raise TypeError("Missing required property 'bucket'")
            __props__.__dict__["bucket"] = bucket
            __props__.__dict__["header_sets"] = header_sets
            __props__.__dict__["param_sets"] = param_sets
        super(BucketUserDefinedLogFields, __self__).__init__(
            'alicloud:oss/bucketUserDefinedLogFields:BucketUserDefinedLogFields',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            bucket: Optional[pulumi.Input[str]] = None,
            header_sets: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            param_sets: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None) -> 'BucketUserDefinedLogFields':
        """
        Get an existing BucketUserDefinedLogFields resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: The name of the bucket.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] header_sets: Container for custom request header configuration information.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] param_sets: Container for custom request parameters configuration information.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _BucketUserDefinedLogFieldsState.__new__(_BucketUserDefinedLogFieldsState)

        __props__.__dict__["bucket"] = bucket
        __props__.__dict__["header_sets"] = header_sets
        __props__.__dict__["param_sets"] = param_sets
        return BucketUserDefinedLogFields(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def bucket(self) -> pulumi.Output[str]:
        """
        The name of the bucket.
        """
        return pulumi.get(self, "bucket")

    @property
    @pulumi.getter(name="headerSets")
    def header_sets(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Container for custom request header configuration information.
        """
        return pulumi.get(self, "header_sets")

    @property
    @pulumi.getter(name="paramSets")
    def param_sets(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Container for custom request parameters configuration information.
        """
        return pulumi.get(self, "param_sets")

