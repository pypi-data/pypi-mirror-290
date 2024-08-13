# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['DataFlowArgs', 'DataFlow']

@pulumi.input_type
class DataFlowArgs:
    def __init__(__self__, *,
                 file_system_id: pulumi.Input[str],
                 fset_id: pulumi.Input[str],
                 source_storage: pulumi.Input[str],
                 throughput: pulumi.Input[int],
                 description: Optional[pulumi.Input[str]] = None,
                 dry_run: Optional[pulumi.Input[bool]] = None,
                 source_security_type: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a DataFlow resource.
        :param pulumi.Input[str] file_system_id: The ID of the file system.
        :param pulumi.Input[str] fset_id: The ID of the Fileset.
        :param pulumi.Input[str] source_storage: The access path of the source store. Format: `<storage type>://<path>`. Among them:
               - storage type: currently only OSS is supported.
               - path: the bucket name of OSS.
               - Only lowercase letters, numbers, and dashes (-) are supported and must start and end with lowercase letters or numbers.
        :param pulumi.Input[int] throughput: The maximum transmission bandwidth of data flow, unit: `MB/s`. Valid values: `1200`, `1500`, `600`. **NOTE:** The transmission bandwidth of data flow must be less than the IO bandwidth of the file system.
        :param pulumi.Input[str] description: The Description of the data flow. Restrictions:
        :param pulumi.Input[bool] dry_run: The dry run.
        :param pulumi.Input[str] source_security_type: The security protection type of the source storage. If the source storage must be accessed through security protection, specify the security protection type of the source storage. Value:
               - `NONE` (default): Indicates that the source storage does not need to be accessed through security protection.
               - `SSL`: Protects access through SSL certificates.
        :param pulumi.Input[str] status: The status of the Data flow. Valid values: `Running`, `Stopped`.
        """
        pulumi.set(__self__, "file_system_id", file_system_id)
        pulumi.set(__self__, "fset_id", fset_id)
        pulumi.set(__self__, "source_storage", source_storage)
        pulumi.set(__self__, "throughput", throughput)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if dry_run is not None:
            pulumi.set(__self__, "dry_run", dry_run)
        if source_security_type is not None:
            pulumi.set(__self__, "source_security_type", source_security_type)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="fileSystemId")
    def file_system_id(self) -> pulumi.Input[str]:
        """
        The ID of the file system.
        """
        return pulumi.get(self, "file_system_id")

    @file_system_id.setter
    def file_system_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "file_system_id", value)

    @property
    @pulumi.getter(name="fsetId")
    def fset_id(self) -> pulumi.Input[str]:
        """
        The ID of the Fileset.
        """
        return pulumi.get(self, "fset_id")

    @fset_id.setter
    def fset_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "fset_id", value)

    @property
    @pulumi.getter(name="sourceStorage")
    def source_storage(self) -> pulumi.Input[str]:
        """
        The access path of the source store. Format: `<storage type>://<path>`. Among them:
        - storage type: currently only OSS is supported.
        - path: the bucket name of OSS.
        - Only lowercase letters, numbers, and dashes (-) are supported and must start and end with lowercase letters or numbers.
        """
        return pulumi.get(self, "source_storage")

    @source_storage.setter
    def source_storage(self, value: pulumi.Input[str]):
        pulumi.set(self, "source_storage", value)

    @property
    @pulumi.getter
    def throughput(self) -> pulumi.Input[int]:
        """
        The maximum transmission bandwidth of data flow, unit: `MB/s`. Valid values: `1200`, `1500`, `600`. **NOTE:** The transmission bandwidth of data flow must be less than the IO bandwidth of the file system.
        """
        return pulumi.get(self, "throughput")

    @throughput.setter
    def throughput(self, value: pulumi.Input[int]):
        pulumi.set(self, "throughput", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The Description of the data flow. Restrictions:
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

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
    @pulumi.getter(name="sourceSecurityType")
    def source_security_type(self) -> Optional[pulumi.Input[str]]:
        """
        The security protection type of the source storage. If the source storage must be accessed through security protection, specify the security protection type of the source storage. Value:
        - `NONE` (default): Indicates that the source storage does not need to be accessed through security protection.
        - `SSL`: Protects access through SSL certificates.
        """
        return pulumi.get(self, "source_security_type")

    @source_security_type.setter
    def source_security_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_security_type", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the Data flow. Valid values: `Running`, `Stopped`.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class _DataFlowState:
    def __init__(__self__, *,
                 data_flow_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 dry_run: Optional[pulumi.Input[bool]] = None,
                 file_system_id: Optional[pulumi.Input[str]] = None,
                 fset_id: Optional[pulumi.Input[str]] = None,
                 source_security_type: Optional[pulumi.Input[str]] = None,
                 source_storage: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 throughput: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering DataFlow resources.
        :param pulumi.Input[str] data_flow_id: The ID of the Data flow.
        :param pulumi.Input[str] description: The Description of the data flow. Restrictions:
        :param pulumi.Input[bool] dry_run: The dry run.
        :param pulumi.Input[str] file_system_id: The ID of the file system.
        :param pulumi.Input[str] fset_id: The ID of the Fileset.
        :param pulumi.Input[str] source_security_type: The security protection type of the source storage. If the source storage must be accessed through security protection, specify the security protection type of the source storage. Value:
               - `NONE` (default): Indicates that the source storage does not need to be accessed through security protection.
               - `SSL`: Protects access through SSL certificates.
        :param pulumi.Input[str] source_storage: The access path of the source store. Format: `<storage type>://<path>`. Among them:
               - storage type: currently only OSS is supported.
               - path: the bucket name of OSS.
               - Only lowercase letters, numbers, and dashes (-) are supported and must start and end with lowercase letters or numbers.
        :param pulumi.Input[str] status: The status of the Data flow. Valid values: `Running`, `Stopped`.
        :param pulumi.Input[int] throughput: The maximum transmission bandwidth of data flow, unit: `MB/s`. Valid values: `1200`, `1500`, `600`. **NOTE:** The transmission bandwidth of data flow must be less than the IO bandwidth of the file system.
        """
        if data_flow_id is not None:
            pulumi.set(__self__, "data_flow_id", data_flow_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if dry_run is not None:
            pulumi.set(__self__, "dry_run", dry_run)
        if file_system_id is not None:
            pulumi.set(__self__, "file_system_id", file_system_id)
        if fset_id is not None:
            pulumi.set(__self__, "fset_id", fset_id)
        if source_security_type is not None:
            pulumi.set(__self__, "source_security_type", source_security_type)
        if source_storage is not None:
            pulumi.set(__self__, "source_storage", source_storage)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if throughput is not None:
            pulumi.set(__self__, "throughput", throughput)

    @property
    @pulumi.getter(name="dataFlowId")
    def data_flow_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Data flow.
        """
        return pulumi.get(self, "data_flow_id")

    @data_flow_id.setter
    def data_flow_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "data_flow_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The Description of the data flow. Restrictions:
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

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
    @pulumi.getter(name="fileSystemId")
    def file_system_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the file system.
        """
        return pulumi.get(self, "file_system_id")

    @file_system_id.setter
    def file_system_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "file_system_id", value)

    @property
    @pulumi.getter(name="fsetId")
    def fset_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Fileset.
        """
        return pulumi.get(self, "fset_id")

    @fset_id.setter
    def fset_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "fset_id", value)

    @property
    @pulumi.getter(name="sourceSecurityType")
    def source_security_type(self) -> Optional[pulumi.Input[str]]:
        """
        The security protection type of the source storage. If the source storage must be accessed through security protection, specify the security protection type of the source storage. Value:
        - `NONE` (default): Indicates that the source storage does not need to be accessed through security protection.
        - `SSL`: Protects access through SSL certificates.
        """
        return pulumi.get(self, "source_security_type")

    @source_security_type.setter
    def source_security_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_security_type", value)

    @property
    @pulumi.getter(name="sourceStorage")
    def source_storage(self) -> Optional[pulumi.Input[str]]:
        """
        The access path of the source store. Format: `<storage type>://<path>`. Among them:
        - storage type: currently only OSS is supported.
        - path: the bucket name of OSS.
        - Only lowercase letters, numbers, and dashes (-) are supported and must start and end with lowercase letters or numbers.
        """
        return pulumi.get(self, "source_storage")

    @source_storage.setter
    def source_storage(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_storage", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the Data flow. Valid values: `Running`, `Stopped`.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def throughput(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum transmission bandwidth of data flow, unit: `MB/s`. Valid values: `1200`, `1500`, `600`. **NOTE:** The transmission bandwidth of data flow must be less than the IO bandwidth of the file system.
        """
        return pulumi.get(self, "throughput")

    @throughput.setter
    def throughput(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "throughput", value)


class DataFlow(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 dry_run: Optional[pulumi.Input[bool]] = None,
                 file_system_id: Optional[pulumi.Input[str]] = None,
                 fset_id: Optional[pulumi.Input[str]] = None,
                 source_security_type: Optional[pulumi.Input[str]] = None,
                 source_storage: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 throughput: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        Provides a Network Attached Storage (NAS) Data Flow resource.

        For information about Network Attached Storage (NAS) Data Flow and how to use it, see [What is Data Flow](https://www.alibabacloud.com/help/en/doc-detail/27530.html).

        > **NOTE:** Available since v1.153.0.

        ## Import

        Network Attached Storage (NAS) Data Flow can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:nas/dataFlow:DataFlow example <file_system_id>:<data_flow_id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The Description of the data flow. Restrictions:
        :param pulumi.Input[bool] dry_run: The dry run.
        :param pulumi.Input[str] file_system_id: The ID of the file system.
        :param pulumi.Input[str] fset_id: The ID of the Fileset.
        :param pulumi.Input[str] source_security_type: The security protection type of the source storage. If the source storage must be accessed through security protection, specify the security protection type of the source storage. Value:
               - `NONE` (default): Indicates that the source storage does not need to be accessed through security protection.
               - `SSL`: Protects access through SSL certificates.
        :param pulumi.Input[str] source_storage: The access path of the source store. Format: `<storage type>://<path>`. Among them:
               - storage type: currently only OSS is supported.
               - path: the bucket name of OSS.
               - Only lowercase letters, numbers, and dashes (-) are supported and must start and end with lowercase letters or numbers.
        :param pulumi.Input[str] status: The status of the Data flow. Valid values: `Running`, `Stopped`.
        :param pulumi.Input[int] throughput: The maximum transmission bandwidth of data flow, unit: `MB/s`. Valid values: `1200`, `1500`, `600`. **NOTE:** The transmission bandwidth of data flow must be less than the IO bandwidth of the file system.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DataFlowArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Network Attached Storage (NAS) Data Flow resource.

        For information about Network Attached Storage (NAS) Data Flow and how to use it, see [What is Data Flow](https://www.alibabacloud.com/help/en/doc-detail/27530.html).

        > **NOTE:** Available since v1.153.0.

        ## Import

        Network Attached Storage (NAS) Data Flow can be imported using the id, e.g.

        ```sh
        $ pulumi import alicloud:nas/dataFlow:DataFlow example <file_system_id>:<data_flow_id>
        ```

        :param str resource_name: The name of the resource.
        :param DataFlowArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DataFlowArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 dry_run: Optional[pulumi.Input[bool]] = None,
                 file_system_id: Optional[pulumi.Input[str]] = None,
                 fset_id: Optional[pulumi.Input[str]] = None,
                 source_security_type: Optional[pulumi.Input[str]] = None,
                 source_storage: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 throughput: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DataFlowArgs.__new__(DataFlowArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["dry_run"] = dry_run
            if file_system_id is None and not opts.urn:
                raise TypeError("Missing required property 'file_system_id'")
            __props__.__dict__["file_system_id"] = file_system_id
            if fset_id is None and not opts.urn:
                raise TypeError("Missing required property 'fset_id'")
            __props__.__dict__["fset_id"] = fset_id
            __props__.__dict__["source_security_type"] = source_security_type
            if source_storage is None and not opts.urn:
                raise TypeError("Missing required property 'source_storage'")
            __props__.__dict__["source_storage"] = source_storage
            __props__.__dict__["status"] = status
            if throughput is None and not opts.urn:
                raise TypeError("Missing required property 'throughput'")
            __props__.__dict__["throughput"] = throughput
            __props__.__dict__["data_flow_id"] = None
        super(DataFlow, __self__).__init__(
            'alicloud:nas/dataFlow:DataFlow',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            data_flow_id: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            dry_run: Optional[pulumi.Input[bool]] = None,
            file_system_id: Optional[pulumi.Input[str]] = None,
            fset_id: Optional[pulumi.Input[str]] = None,
            source_security_type: Optional[pulumi.Input[str]] = None,
            source_storage: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            throughput: Optional[pulumi.Input[int]] = None) -> 'DataFlow':
        """
        Get an existing DataFlow resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] data_flow_id: The ID of the Data flow.
        :param pulumi.Input[str] description: The Description of the data flow. Restrictions:
        :param pulumi.Input[bool] dry_run: The dry run.
        :param pulumi.Input[str] file_system_id: The ID of the file system.
        :param pulumi.Input[str] fset_id: The ID of the Fileset.
        :param pulumi.Input[str] source_security_type: The security protection type of the source storage. If the source storage must be accessed through security protection, specify the security protection type of the source storage. Value:
               - `NONE` (default): Indicates that the source storage does not need to be accessed through security protection.
               - `SSL`: Protects access through SSL certificates.
        :param pulumi.Input[str] source_storage: The access path of the source store. Format: `<storage type>://<path>`. Among them:
               - storage type: currently only OSS is supported.
               - path: the bucket name of OSS.
               - Only lowercase letters, numbers, and dashes (-) are supported and must start and end with lowercase letters or numbers.
        :param pulumi.Input[str] status: The status of the Data flow. Valid values: `Running`, `Stopped`.
        :param pulumi.Input[int] throughput: The maximum transmission bandwidth of data flow, unit: `MB/s`. Valid values: `1200`, `1500`, `600`. **NOTE:** The transmission bandwidth of data flow must be less than the IO bandwidth of the file system.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DataFlowState.__new__(_DataFlowState)

        __props__.__dict__["data_flow_id"] = data_flow_id
        __props__.__dict__["description"] = description
        __props__.__dict__["dry_run"] = dry_run
        __props__.__dict__["file_system_id"] = file_system_id
        __props__.__dict__["fset_id"] = fset_id
        __props__.__dict__["source_security_type"] = source_security_type
        __props__.__dict__["source_storage"] = source_storage
        __props__.__dict__["status"] = status
        __props__.__dict__["throughput"] = throughput
        return DataFlow(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="dataFlowId")
    def data_flow_id(self) -> pulumi.Output[str]:
        """
        The ID of the Data flow.
        """
        return pulumi.get(self, "data_flow_id")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The Description of the data flow. Restrictions:
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="dryRun")
    def dry_run(self) -> pulumi.Output[Optional[bool]]:
        """
        The dry run.
        """
        return pulumi.get(self, "dry_run")

    @property
    @pulumi.getter(name="fileSystemId")
    def file_system_id(self) -> pulumi.Output[str]:
        """
        The ID of the file system.
        """
        return pulumi.get(self, "file_system_id")

    @property
    @pulumi.getter(name="fsetId")
    def fset_id(self) -> pulumi.Output[str]:
        """
        The ID of the Fileset.
        """
        return pulumi.get(self, "fset_id")

    @property
    @pulumi.getter(name="sourceSecurityType")
    def source_security_type(self) -> pulumi.Output[str]:
        """
        The security protection type of the source storage. If the source storage must be accessed through security protection, specify the security protection type of the source storage. Value:
        - `NONE` (default): Indicates that the source storage does not need to be accessed through security protection.
        - `SSL`: Protects access through SSL certificates.
        """
        return pulumi.get(self, "source_security_type")

    @property
    @pulumi.getter(name="sourceStorage")
    def source_storage(self) -> pulumi.Output[str]:
        """
        The access path of the source store. Format: `<storage type>://<path>`. Among them:
        - storage type: currently only OSS is supported.
        - path: the bucket name of OSS.
        - Only lowercase letters, numbers, and dashes (-) are supported and must start and end with lowercase letters or numbers.
        """
        return pulumi.get(self, "source_storage")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The status of the Data flow. Valid values: `Running`, `Stopped`.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def throughput(self) -> pulumi.Output[int]:
        """
        The maximum transmission bandwidth of data flow, unit: `MB/s`. Valid values: `1200`, `1500`, `600`. **NOTE:** The transmission bandwidth of data flow must be less than the IO bandwidth of the file system.
        """
        return pulumi.get(self, "throughput")

