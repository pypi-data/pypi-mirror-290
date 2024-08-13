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
    'GetOpenApiPricingModulesResult',
    'AwaitableGetOpenApiPricingModulesResult',
    'get_open_api_pricing_modules',
    'get_open_api_pricing_modules_output',
]

@pulumi.output_type
class GetOpenApiPricingModulesResult:
    """
    A collection of values returned by getOpenApiPricingModules.
    """
    def __init__(__self__, id=None, ids=None, modules=None, name_regex=None, names=None, output_file=None, product_code=None, product_type=None, subscription_type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if modules and not isinstance(modules, list):
            raise TypeError("Expected argument 'modules' to be a list")
        pulumi.set(__self__, "modules", modules)
        if name_regex and not isinstance(name_regex, str):
            raise TypeError("Expected argument 'name_regex' to be a str")
        pulumi.set(__self__, "name_regex", name_regex)
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        pulumi.set(__self__, "names", names)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if product_code and not isinstance(product_code, str):
            raise TypeError("Expected argument 'product_code' to be a str")
        pulumi.set(__self__, "product_code", product_code)
        if product_type and not isinstance(product_type, str):
            raise TypeError("Expected argument 'product_type' to be a str")
        pulumi.set(__self__, "product_type", product_type)
        if subscription_type and not isinstance(subscription_type, str):
            raise TypeError("Expected argument 'subscription_type' to be a str")
        pulumi.set(__self__, "subscription_type", subscription_type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def ids(self) -> Sequence[str]:
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter
    def modules(self) -> Sequence['outputs.GetOpenApiPricingModulesModuleResult']:
        """
        A list of Pricing Module Entries. Each element contains the following attributes:
        """
        return pulumi.get(self, "modules")

    @property
    @pulumi.getter(name="nameRegex")
    def name_regex(self) -> Optional[str]:
        return pulumi.get(self, "name_regex")

    @property
    @pulumi.getter
    def names(self) -> Sequence[str]:
        """
        A list of name of Pricing Modules.
        """
        return pulumi.get(self, "names")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter(name="productCode")
    def product_code(self) -> str:
        return pulumi.get(self, "product_code")

    @property
    @pulumi.getter(name="productType")
    def product_type(self) -> Optional[str]:
        return pulumi.get(self, "product_type")

    @property
    @pulumi.getter(name="subscriptionType")
    def subscription_type(self) -> str:
        return pulumi.get(self, "subscription_type")


class AwaitableGetOpenApiPricingModulesResult(GetOpenApiPricingModulesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetOpenApiPricingModulesResult(
            id=self.id,
            ids=self.ids,
            modules=self.modules,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file,
            product_code=self.product_code,
            product_type=self.product_type,
            subscription_type=self.subscription_type)


def get_open_api_pricing_modules(ids: Optional[Sequence[str]] = None,
                                 name_regex: Optional[str] = None,
                                 output_file: Optional[str] = None,
                                 product_code: Optional[str] = None,
                                 product_type: Optional[str] = None,
                                 subscription_type: Optional[str] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetOpenApiPricingModulesResult:
    """
    This data source provides Bss Open Api Pricing Module available to the user.[What is Pricing Module](https://www.alibabacloud.com/help/en/bss-openapi/latest/describepricingmodule#doc-api-BssOpenApi-DescribePricingModule)

    > **NOTE:** Available in 1.195.0+

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    default = alicloud.bss.get_open_api_pricing_modules(name_regex="国内月均日峰值带宽",
        product_code="cdn",
        product_type="CDN",
        subscription_type="PayAsYouGo")
    pulumi.export("alicloudBssOpenapiPricingModuleExampleId", default.modules[0].code)
    ```


    :param str name_regex: A regex string to filter results by Property name.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str product_code: The product code.
    :param str product_type: The product type.
    :param str subscription_type: Subscription type. Value:
           * Subscription: Prepaid.
           * PayAsYouGo: postpaid.
    """
    __args__ = dict()
    __args__['ids'] = ids
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    __args__['productCode'] = product_code
    __args__['productType'] = product_type
    __args__['subscriptionType'] = subscription_type
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:bss/getOpenApiPricingModules:getOpenApiPricingModules', __args__, opts=opts, typ=GetOpenApiPricingModulesResult).value

    return AwaitableGetOpenApiPricingModulesResult(
        id=pulumi.get(__ret__, 'id'),
        ids=pulumi.get(__ret__, 'ids'),
        modules=pulumi.get(__ret__, 'modules'),
        name_regex=pulumi.get(__ret__, 'name_regex'),
        names=pulumi.get(__ret__, 'names'),
        output_file=pulumi.get(__ret__, 'output_file'),
        product_code=pulumi.get(__ret__, 'product_code'),
        product_type=pulumi.get(__ret__, 'product_type'),
        subscription_type=pulumi.get(__ret__, 'subscription_type'))


@_utilities.lift_output_func(get_open_api_pricing_modules)
def get_open_api_pricing_modules_output(ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                                        name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                                        output_file: Optional[pulumi.Input[Optional[str]]] = None,
                                        product_code: Optional[pulumi.Input[str]] = None,
                                        product_type: Optional[pulumi.Input[Optional[str]]] = None,
                                        subscription_type: Optional[pulumi.Input[str]] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetOpenApiPricingModulesResult]:
    """
    This data source provides Bss Open Api Pricing Module available to the user.[What is Pricing Module](https://www.alibabacloud.com/help/en/bss-openapi/latest/describepricingmodule#doc-api-BssOpenApi-DescribePricingModule)

    > **NOTE:** Available in 1.195.0+

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    default = alicloud.bss.get_open_api_pricing_modules(name_regex="国内月均日峰值带宽",
        product_code="cdn",
        product_type="CDN",
        subscription_type="PayAsYouGo")
    pulumi.export("alicloudBssOpenapiPricingModuleExampleId", default.modules[0].code)
    ```


    :param str name_regex: A regex string to filter results by Property name.
    :param str output_file: File name where to save data source results (after running `pulumi preview`).
    :param str product_code: The product code.
    :param str product_type: The product type.
    :param str subscription_type: Subscription type. Value:
           * Subscription: Prepaid.
           * PayAsYouGo: postpaid.
    """
    ...
