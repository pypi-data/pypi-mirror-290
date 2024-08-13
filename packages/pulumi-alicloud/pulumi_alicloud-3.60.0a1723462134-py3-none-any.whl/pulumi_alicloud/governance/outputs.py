# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'BaselineBaselineItem',
    'GetBaselinesBaselineResult',
]

@pulumi.output_type
class BaselineBaselineItem(dict):
    def __init__(__self__, *,
                 config: Optional[str] = None,
                 name: Optional[str] = None,
                 version: Optional[str] = None):
        """
        :param str config: Baseline item configuration. The format is a JSON string.
        :param str name: The baseline item name.
        :param str version: The baseline item version.
        """
        if config is not None:
            pulumi.set(__self__, "config", config)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def config(self) -> Optional[str]:
        """
        Baseline item configuration. The format is a JSON string.
        """
        return pulumi.get(self, "config")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The baseline item name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def version(self) -> Optional[str]:
        """
        The baseline item version.
        """
        return pulumi.get(self, "version")


@pulumi.output_type
class GetBaselinesBaselineResult(dict):
    def __init__(__self__, *,
                 baseline_id: str,
                 baseline_name: str,
                 description: str):
        """
        :param str baseline_id: Baseline ID
        :param str baseline_name: Baseline Name.
        :param str description: Baseline Description.
        """
        pulumi.set(__self__, "baseline_id", baseline_id)
        pulumi.set(__self__, "baseline_name", baseline_name)
        pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter(name="baselineId")
    def baseline_id(self) -> str:
        """
        Baseline ID
        """
        return pulumi.get(self, "baseline_id")

    @property
    @pulumi.getter(name="baselineName")
    def baseline_name(self) -> str:
        """
        Baseline Name.
        """
        return pulumi.get(self, "baseline_name")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Baseline Description.
        """
        return pulumi.get(self, "description")


