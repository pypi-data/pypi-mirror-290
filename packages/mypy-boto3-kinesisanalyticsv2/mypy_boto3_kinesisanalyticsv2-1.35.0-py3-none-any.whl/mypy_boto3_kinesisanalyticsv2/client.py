"""
Type annotations for kinesisanalyticsv2 service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_kinesisanalyticsv2.client import KinesisAnalyticsV2Client

    session = Session()
    client: KinesisAnalyticsV2Client = session.client("kinesisanalyticsv2")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import ApplicationModeType, OperationStatusType, RuntimeEnvironmentType, UrlTypeType
from .paginator import (
    ListApplicationOperationsPaginator,
    ListApplicationSnapshotsPaginator,
    ListApplicationsPaginator,
    ListApplicationVersionsPaginator,
)
from .type_defs import (
    AddApplicationCloudWatchLoggingOptionResponseTypeDef,
    AddApplicationInputProcessingConfigurationResponseTypeDef,
    AddApplicationInputResponseTypeDef,
    AddApplicationOutputResponseTypeDef,
    AddApplicationReferenceDataSourceResponseTypeDef,
    AddApplicationVpcConfigurationResponseTypeDef,
    ApplicationConfigurationTypeDef,
    ApplicationConfigurationUpdateTypeDef,
    ApplicationMaintenanceConfigurationUpdateTypeDef,
    CloudWatchLoggingOptionTypeDef,
    CloudWatchLoggingOptionUpdateTypeDef,
    CreateApplicationPresignedUrlResponseTypeDef,
    CreateApplicationResponseTypeDef,
    DeleteApplicationCloudWatchLoggingOptionResponseTypeDef,
    DeleteApplicationInputProcessingConfigurationResponseTypeDef,
    DeleteApplicationOutputResponseTypeDef,
    DeleteApplicationReferenceDataSourceResponseTypeDef,
    DeleteApplicationVpcConfigurationResponseTypeDef,
    DescribeApplicationOperationResponseTypeDef,
    DescribeApplicationResponseTypeDef,
    DescribeApplicationSnapshotResponseTypeDef,
    DescribeApplicationVersionResponseTypeDef,
    DiscoverInputSchemaResponseTypeDef,
    InputProcessingConfigurationTypeDef,
    InputStartingPositionConfigurationTypeDef,
    InputTypeDef,
    ListApplicationOperationsResponseTypeDef,
    ListApplicationSnapshotsResponseTypeDef,
    ListApplicationsResponseTypeDef,
    ListApplicationVersionsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    OutputTypeDef,
    ReferenceDataSourceTypeDef,
    RollbackApplicationResponseTypeDef,
    RunConfigurationTypeDef,
    RunConfigurationUpdateTypeDef,
    S3ConfigurationTypeDef,
    StartApplicationResponseTypeDef,
    StopApplicationResponseTypeDef,
    TagTypeDef,
    TimestampTypeDef,
    UpdateApplicationMaintenanceConfigurationResponseTypeDef,
    UpdateApplicationResponseTypeDef,
    VpcConfigurationTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("KinesisAnalyticsV2Client",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    CodeValidationException: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    InvalidApplicationConfigurationException: Type[BotocoreClientError]
    InvalidArgumentException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceProvisionedThroughputExceededException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    UnableToDetectSchemaException: Type[BotocoreClientError]
    UnsupportedOperationException: Type[BotocoreClientError]


class KinesisAnalyticsV2Client(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        KinesisAnalyticsV2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#exceptions)
        """

    def add_application_cloud_watch_logging_option(
        self,
        *,
        ApplicationName: str,
        CloudWatchLoggingOption: CloudWatchLoggingOptionTypeDef,
        CurrentApplicationVersionId: int = ...,
        ConditionalToken: str = ...,
    ) -> AddApplicationCloudWatchLoggingOptionResponseTypeDef:
        """
        Adds an Amazon CloudWatch log stream to monitor application configuration
        errors.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.add_application_cloud_watch_logging_option)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#add_application_cloud_watch_logging_option)
        """

    def add_application_input(
        self, *, ApplicationName: str, CurrentApplicationVersionId: int, Input: InputTypeDef
    ) -> AddApplicationInputResponseTypeDef:
        """
        Adds a streaming source to your SQL-based Kinesis Data Analytics application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.add_application_input)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#add_application_input)
        """

    def add_application_input_processing_configuration(
        self,
        *,
        ApplicationName: str,
        CurrentApplicationVersionId: int,
        InputId: str,
        InputProcessingConfiguration: InputProcessingConfigurationTypeDef,
    ) -> AddApplicationInputProcessingConfigurationResponseTypeDef:
        """
        Adds an  InputProcessingConfiguration to a SQL-based Kinesis Data Analytics
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.add_application_input_processing_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#add_application_input_processing_configuration)
        """

    def add_application_output(
        self, *, ApplicationName: str, CurrentApplicationVersionId: int, Output: OutputTypeDef
    ) -> AddApplicationOutputResponseTypeDef:
        """
        Adds an external destination to your SQL-based Kinesis Data Analytics
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.add_application_output)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#add_application_output)
        """

    def add_application_reference_data_source(
        self,
        *,
        ApplicationName: str,
        CurrentApplicationVersionId: int,
        ReferenceDataSource: ReferenceDataSourceTypeDef,
    ) -> AddApplicationReferenceDataSourceResponseTypeDef:
        """
        Adds a reference data source to an existing SQL-based Kinesis Data Analytics
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.add_application_reference_data_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#add_application_reference_data_source)
        """

    def add_application_vpc_configuration(
        self,
        *,
        ApplicationName: str,
        VpcConfiguration: VpcConfigurationTypeDef,
        CurrentApplicationVersionId: int = ...,
        ConditionalToken: str = ...,
    ) -> AddApplicationVpcConfigurationResponseTypeDef:
        """
        Adds a Virtual Private Cloud (VPC) configuration to the application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.add_application_vpc_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#add_application_vpc_configuration)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#close)
        """

    def create_application(
        self,
        *,
        ApplicationName: str,
        RuntimeEnvironment: RuntimeEnvironmentType,
        ServiceExecutionRole: str,
        ApplicationDescription: str = ...,
        ApplicationConfiguration: ApplicationConfigurationTypeDef = ...,
        CloudWatchLoggingOptions: Sequence[CloudWatchLoggingOptionTypeDef] = ...,
        Tags: Sequence[TagTypeDef] = ...,
        ApplicationMode: ApplicationModeType = ...,
    ) -> CreateApplicationResponseTypeDef:
        """
        Creates a Managed Service for Apache Flink application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.create_application)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#create_application)
        """

    def create_application_presigned_url(
        self,
        *,
        ApplicationName: str,
        UrlType: UrlTypeType,
        SessionExpirationDurationInSeconds: int = ...,
    ) -> CreateApplicationPresignedUrlResponseTypeDef:
        """
        Creates and returns a URL that you can use to connect to an application's
        extension.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.create_application_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#create_application_presigned_url)
        """

    def create_application_snapshot(
        self, *, ApplicationName: str, SnapshotName: str
    ) -> Dict[str, Any]:
        """
        Creates a snapshot of the application's state data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.create_application_snapshot)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#create_application_snapshot)
        """

    def delete_application(
        self, *, ApplicationName: str, CreateTimestamp: TimestampTypeDef
    ) -> Dict[str, Any]:
        """
        Deletes the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.delete_application)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#delete_application)
        """

    def delete_application_cloud_watch_logging_option(
        self,
        *,
        ApplicationName: str,
        CloudWatchLoggingOptionId: str,
        CurrentApplicationVersionId: int = ...,
        ConditionalToken: str = ...,
    ) -> DeleteApplicationCloudWatchLoggingOptionResponseTypeDef:
        """
        Deletes an Amazon CloudWatch log stream from an SQL-based Kinesis Data
        Analytics
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.delete_application_cloud_watch_logging_option)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#delete_application_cloud_watch_logging_option)
        """

    def delete_application_input_processing_configuration(
        self, *, ApplicationName: str, CurrentApplicationVersionId: int, InputId: str
    ) -> DeleteApplicationInputProcessingConfigurationResponseTypeDef:
        """
        Deletes an  InputProcessingConfiguration from an input.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.delete_application_input_processing_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#delete_application_input_processing_configuration)
        """

    def delete_application_output(
        self, *, ApplicationName: str, CurrentApplicationVersionId: int, OutputId: str
    ) -> DeleteApplicationOutputResponseTypeDef:
        """
        Deletes the output destination configuration from your SQL-based Kinesis Data
        Analytics application's
        configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.delete_application_output)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#delete_application_output)
        """

    def delete_application_reference_data_source(
        self, *, ApplicationName: str, CurrentApplicationVersionId: int, ReferenceId: str
    ) -> DeleteApplicationReferenceDataSourceResponseTypeDef:
        """
        Deletes a reference data source configuration from the specified SQL-based
        Kinesis Data Analytics application's
        configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.delete_application_reference_data_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#delete_application_reference_data_source)
        """

    def delete_application_snapshot(
        self,
        *,
        ApplicationName: str,
        SnapshotName: str,
        SnapshotCreationTimestamp: TimestampTypeDef,
    ) -> Dict[str, Any]:
        """
        Deletes a snapshot of application state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.delete_application_snapshot)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#delete_application_snapshot)
        """

    def delete_application_vpc_configuration(
        self,
        *,
        ApplicationName: str,
        VpcConfigurationId: str,
        CurrentApplicationVersionId: int = ...,
        ConditionalToken: str = ...,
    ) -> DeleteApplicationVpcConfigurationResponseTypeDef:
        """
        Removes a VPC configuration from a Managed Service for Apache Flink application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.delete_application_vpc_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#delete_application_vpc_configuration)
        """

    def describe_application(
        self, *, ApplicationName: str, IncludeAdditionalDetails: bool = ...
    ) -> DescribeApplicationResponseTypeDef:
        """
        Returns information about a specific Managed Service for Apache Flink
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.describe_application)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#describe_application)
        """

    def describe_application_operation(
        self, *, ApplicationName: str, OperationId: str
    ) -> DescribeApplicationOperationResponseTypeDef:
        """
        Returns information about a specific operation performed on a Managed Service
        for Apache Flink application See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/kinesisanalyticsv2-2018-05-23/DescribeApplicationOperation).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.describe_application_operation)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#describe_application_operation)
        """

    def describe_application_snapshot(
        self, *, ApplicationName: str, SnapshotName: str
    ) -> DescribeApplicationSnapshotResponseTypeDef:
        """
        Returns information about a snapshot of application state data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.describe_application_snapshot)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#describe_application_snapshot)
        """

    def describe_application_version(
        self, *, ApplicationName: str, ApplicationVersionId: int
    ) -> DescribeApplicationVersionResponseTypeDef:
        """
        Provides a detailed description of a specified version of the application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.describe_application_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#describe_application_version)
        """

    def discover_input_schema(
        self,
        *,
        ServiceExecutionRole: str,
        ResourceARN: str = ...,
        InputStartingPositionConfiguration: InputStartingPositionConfigurationTypeDef = ...,
        S3Configuration: S3ConfigurationTypeDef = ...,
        InputProcessingConfiguration: InputProcessingConfigurationTypeDef = ...,
    ) -> DiscoverInputSchemaResponseTypeDef:
        """
        Infers a schema for a SQL-based Kinesis Data Analytics application by
        evaluating sample records on the specified streaming source (Kinesis data
        stream or Kinesis Data Firehose delivery stream) or Amazon S3
        object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.discover_input_schema)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#discover_input_schema)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#generate_presigned_url)
        """

    def list_application_operations(
        self,
        *,
        ApplicationName: str,
        Limit: int = ...,
        NextToken: str = ...,
        Operation: str = ...,
        OperationStatus: OperationStatusType = ...,
    ) -> ListApplicationOperationsResponseTypeDef:
        """
        Lists information about operations performed on a Managed Service for Apache
        Flink application See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/kinesisanalyticsv2-2018-05-23/ListApplicationOperations).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.list_application_operations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#list_application_operations)
        """

    def list_application_snapshots(
        self, *, ApplicationName: str, Limit: int = ..., NextToken: str = ...
    ) -> ListApplicationSnapshotsResponseTypeDef:
        """
        Lists information about the current application snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.list_application_snapshots)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#list_application_snapshots)
        """

    def list_application_versions(
        self, *, ApplicationName: str, Limit: int = ..., NextToken: str = ...
    ) -> ListApplicationVersionsResponseTypeDef:
        """
        Lists all the versions for the specified application, including versions that
        were rolled
        back.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.list_application_versions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#list_application_versions)
        """

    def list_applications(
        self, *, Limit: int = ..., NextToken: str = ...
    ) -> ListApplicationsResponseTypeDef:
        """
        Returns a list of Managed Service for Apache Flink applications in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.list_applications)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#list_applications)
        """

    def list_tags_for_resource(self, *, ResourceARN: str) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves the list of key-value tags assigned to the application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#list_tags_for_resource)
        """

    def rollback_application(
        self, *, ApplicationName: str, CurrentApplicationVersionId: int
    ) -> RollbackApplicationResponseTypeDef:
        """
        Reverts the application to the previous running version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.rollback_application)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#rollback_application)
        """

    def start_application(
        self, *, ApplicationName: str, RunConfiguration: RunConfigurationTypeDef = ...
    ) -> StartApplicationResponseTypeDef:
        """
        Starts the specified Managed Service for Apache Flink application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.start_application)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#start_application)
        """

    def stop_application(
        self, *, ApplicationName: str, Force: bool = ...
    ) -> StopApplicationResponseTypeDef:
        """
        Stops the application from processing data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.stop_application)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#stop_application)
        """

    def tag_resource(self, *, ResourceARN: str, Tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Adds one or more key-value tags to a Managed Service for Apache Flink
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#tag_resource)
        """

    def untag_resource(self, *, ResourceARN: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes one or more tags from a Managed Service for Apache Flink application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#untag_resource)
        """

    def update_application(
        self,
        *,
        ApplicationName: str,
        CurrentApplicationVersionId: int = ...,
        ApplicationConfigurationUpdate: ApplicationConfigurationUpdateTypeDef = ...,
        ServiceExecutionRoleUpdate: str = ...,
        RunConfigurationUpdate: RunConfigurationUpdateTypeDef = ...,
        CloudWatchLoggingOptionUpdates: Sequence[CloudWatchLoggingOptionUpdateTypeDef] = ...,
        ConditionalToken: str = ...,
        RuntimeEnvironmentUpdate: RuntimeEnvironmentType = ...,
    ) -> UpdateApplicationResponseTypeDef:
        """
        Updates an existing Managed Service for Apache Flink application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.update_application)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#update_application)
        """

    def update_application_maintenance_configuration(
        self,
        *,
        ApplicationName: str,
        ApplicationMaintenanceConfigurationUpdate: ApplicationMaintenanceConfigurationUpdateTypeDef,
    ) -> UpdateApplicationMaintenanceConfigurationResponseTypeDef:
        """
        Updates the maintenance configuration of the Managed Service for Apache Flink
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.update_application_maintenance_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#update_application_maintenance_configuration)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_application_operations"]
    ) -> ListApplicationOperationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_application_snapshots"]
    ) -> ListApplicationSnapshotsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_application_versions"]
    ) -> ListApplicationVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_applications"]
    ) -> ListApplicationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisanalyticsv2.html#KinesisAnalyticsV2.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesisanalyticsv2/client/#get_paginator)
        """
