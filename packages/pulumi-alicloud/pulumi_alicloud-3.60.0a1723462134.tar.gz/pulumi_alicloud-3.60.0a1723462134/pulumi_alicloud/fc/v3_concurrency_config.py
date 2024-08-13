# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['V3ConcurrencyConfigArgs', 'V3ConcurrencyConfig']

@pulumi.input_type
class V3ConcurrencyConfigArgs:
    def __init__(__self__, *,
                 function_name: pulumi.Input[str],
                 reserved_concurrency: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a V3ConcurrencyConfig resource.
        :param pulumi.Input[str] function_name: Function Name
        :param pulumi.Input[int] reserved_concurrency: Reserved Concurrency. Functions reserve a part of account concurrency. Other functions cannot use this part of concurrency. Reserved concurrency includes the total concurrency of Reserved Instances and As-You-go instances.
        """
        pulumi.set(__self__, "function_name", function_name)
        if reserved_concurrency is not None:
            pulumi.set(__self__, "reserved_concurrency", reserved_concurrency)

    @property
    @pulumi.getter(name="functionName")
    def function_name(self) -> pulumi.Input[str]:
        """
        Function Name
        """
        return pulumi.get(self, "function_name")

    @function_name.setter
    def function_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "function_name", value)

    @property
    @pulumi.getter(name="reservedConcurrency")
    def reserved_concurrency(self) -> Optional[pulumi.Input[int]]:
        """
        Reserved Concurrency. Functions reserve a part of account concurrency. Other functions cannot use this part of concurrency. Reserved concurrency includes the total concurrency of Reserved Instances and As-You-go instances.
        """
        return pulumi.get(self, "reserved_concurrency")

    @reserved_concurrency.setter
    def reserved_concurrency(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "reserved_concurrency", value)


@pulumi.input_type
class _V3ConcurrencyConfigState:
    def __init__(__self__, *,
                 function_name: Optional[pulumi.Input[str]] = None,
                 reserved_concurrency: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering V3ConcurrencyConfig resources.
        :param pulumi.Input[str] function_name: Function Name
        :param pulumi.Input[int] reserved_concurrency: Reserved Concurrency. Functions reserve a part of account concurrency. Other functions cannot use this part of concurrency. Reserved concurrency includes the total concurrency of Reserved Instances and As-You-go instances.
        """
        if function_name is not None:
            pulumi.set(__self__, "function_name", function_name)
        if reserved_concurrency is not None:
            pulumi.set(__self__, "reserved_concurrency", reserved_concurrency)

    @property
    @pulumi.getter(name="functionName")
    def function_name(self) -> Optional[pulumi.Input[str]]:
        """
        Function Name
        """
        return pulumi.get(self, "function_name")

    @function_name.setter
    def function_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "function_name", value)

    @property
    @pulumi.getter(name="reservedConcurrency")
    def reserved_concurrency(self) -> Optional[pulumi.Input[int]]:
        """
        Reserved Concurrency. Functions reserve a part of account concurrency. Other functions cannot use this part of concurrency. Reserved concurrency includes the total concurrency of Reserved Instances and As-You-go instances.
        """
        return pulumi.get(self, "reserved_concurrency")

    @reserved_concurrency.setter
    def reserved_concurrency(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "reserved_concurrency", value)


class V3ConcurrencyConfig(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 function_name: Optional[pulumi.Input[str]] = None,
                 reserved_concurrency: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        Provides a FCV3 Concurrency Config resource.

        Function concurrency configuration.

        For information about FCV3 Concurrency Config and how to use it, see [What is Concurrency Config](https://www.alibabacloud.com/help/en/functioncompute/developer-reference/api-fc-2023-03-30-putconcurrencyconfig).

        > **NOTE:** Available since v1.228.0.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "terraform-example"
        function = alicloud.fc.V3Function("function",
            memory_size=512,
            cpu=0.5,
            handler="index.Handler",
            code={
                "zip_file": "UEsDBBQACAAIAAAAAAAAAAAAAAAAAAAAAAAIAAAAaW5kZXgucHmEkEFKxEAQRfd9ig9ZTCJOooIwDMwNXLqXnnQlaalUhU5lRj2KZ/FOXkESGR114bJ/P/7jV4b1xRq1hijtFpM1682cuNgPmgysbRulPT0fRxXnMtwrSPyeCdYRokSLnuMLJTTkbUqEvDMbxm1VdcRD6Tk+T1LW2ldB66knsYdA5iNX17ebm6tN2VnPhcswMPmREPuBacb+CiapLarAj9gT6/H97dVlCNScY3mtYvRkxdZlwDKDEnanPWVLdrdkeXEGlFEazVdfPVHaVeHc3N15CUwppwOJXeK7HshAB8NuOU7J6sP4SRXuH/EvbUfMiqMmDqv5M5FNSfAj/wgAAP//UEsHCPl//NYAAQAArwEAAFBLAQIUABQACAAIAAAAAAD5f/zWAAEAAK8BAAAIAAAAAAAAAAAAAAAAAAAAAABpbmRleC5weVBLBQYAAAAAAQABADYAAAA2AQAAAAA=",
            },
            function_name=name,
            runtime="python3.9",
            disk_size=512,
            log_config={
                "log_begin_rule": "None",
            })
        default = alicloud.fc.V3ConcurrencyConfig("default",
            function_name=function.function_name,
            reserved_concurrency=100)
        ```

        ## Import

        FCV3 Concurrency Config can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:fc/v3ConcurrencyConfig:V3ConcurrencyConfig example <id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] function_name: Function Name
        :param pulumi.Input[int] reserved_concurrency: Reserved Concurrency. Functions reserve a part of account concurrency. Other functions cannot use this part of concurrency. Reserved concurrency includes the total concurrency of Reserved Instances and As-You-go instances.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: V3ConcurrencyConfigArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a FCV3 Concurrency Config resource.

        Function concurrency configuration.

        For information about FCV3 Concurrency Config and how to use it, see [What is Concurrency Config](https://www.alibabacloud.com/help/en/functioncompute/developer-reference/api-fc-2023-03-30-putconcurrencyconfig).

        > **NOTE:** Available since v1.228.0.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "terraform-example"
        function = alicloud.fc.V3Function("function",
            memory_size=512,
            cpu=0.5,
            handler="index.Handler",
            code={
                "zip_file": "UEsDBBQACAAIAAAAAAAAAAAAAAAAAAAAAAAIAAAAaW5kZXgucHmEkEFKxEAQRfd9ig9ZTCJOooIwDMwNXLqXnnQlaalUhU5lRj2KZ/FOXkESGR114bJ/P/7jV4b1xRq1hijtFpM1682cuNgPmgysbRulPT0fRxXnMtwrSPyeCdYRokSLnuMLJTTkbUqEvDMbxm1VdcRD6Tk+T1LW2ldB66knsYdA5iNX17ebm6tN2VnPhcswMPmREPuBacb+CiapLarAj9gT6/H97dVlCNScY3mtYvRkxdZlwDKDEnanPWVLdrdkeXEGlFEazVdfPVHaVeHc3N15CUwppwOJXeK7HshAB8NuOU7J6sP4SRXuH/EvbUfMiqMmDqv5M5FNSfAj/wgAAP//UEsHCPl//NYAAQAArwEAAFBLAQIUABQACAAIAAAAAAD5f/zWAAEAAK8BAAAIAAAAAAAAAAAAAAAAAAAAAABpbmRleC5weVBLBQYAAAAAAQABADYAAAA2AQAAAAA=",
            },
            function_name=name,
            runtime="python3.9",
            disk_size=512,
            log_config={
                "log_begin_rule": "None",
            })
        default = alicloud.fc.V3ConcurrencyConfig("default",
            function_name=function.function_name,
            reserved_concurrency=100)
        ```

        ## Import

        FCV3 Concurrency Config can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:fc/v3ConcurrencyConfig:V3ConcurrencyConfig example <id>
        ```

        :param str resource_name: The name of the resource.
        :param V3ConcurrencyConfigArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(V3ConcurrencyConfigArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 function_name: Optional[pulumi.Input[str]] = None,
                 reserved_concurrency: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = V3ConcurrencyConfigArgs.__new__(V3ConcurrencyConfigArgs)

            if function_name is None and not opts.urn:
                raise TypeError("Missing required property 'function_name'")
            __props__.__dict__["function_name"] = function_name
            __props__.__dict__["reserved_concurrency"] = reserved_concurrency
        super(V3ConcurrencyConfig, __self__).__init__(
            'alicloud:fc/v3ConcurrencyConfig:V3ConcurrencyConfig',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            function_name: Optional[pulumi.Input[str]] = None,
            reserved_concurrency: Optional[pulumi.Input[int]] = None) -> 'V3ConcurrencyConfig':
        """
        Get an existing V3ConcurrencyConfig resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] function_name: Function Name
        :param pulumi.Input[int] reserved_concurrency: Reserved Concurrency. Functions reserve a part of account concurrency. Other functions cannot use this part of concurrency. Reserved concurrency includes the total concurrency of Reserved Instances and As-You-go instances.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _V3ConcurrencyConfigState.__new__(_V3ConcurrencyConfigState)

        __props__.__dict__["function_name"] = function_name
        __props__.__dict__["reserved_concurrency"] = reserved_concurrency
        return V3ConcurrencyConfig(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="functionName")
    def function_name(self) -> pulumi.Output[str]:
        """
        Function Name
        """
        return pulumi.get(self, "function_name")

    @property
    @pulumi.getter(name="reservedConcurrency")
    def reserved_concurrency(self) -> pulumi.Output[Optional[int]]:
        """
        Reserved Concurrency. Functions reserve a part of account concurrency. Other functions cannot use this part of concurrency. Reserved concurrency includes the total concurrency of Reserved Instances and As-You-go instances.
        """
        return pulumi.get(self, "reserved_concurrency")

