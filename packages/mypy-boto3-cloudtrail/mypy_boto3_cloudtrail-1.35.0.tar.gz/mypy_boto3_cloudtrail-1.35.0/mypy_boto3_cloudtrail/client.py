"""
Type annotations for cloudtrail service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_cloudtrail.client import CloudTrailClient

    session = Session()
    client: CloudTrailClient = session.client("cloudtrail")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    BillingModeType,
    ImportStatusType,
    InsightsMetricDataTypeType,
    InsightTypeType,
    QueryStatusType,
)
from .paginator import (
    ListImportFailuresPaginator,
    ListImportsPaginator,
    ListPublicKeysPaginator,
    ListTagsPaginator,
    ListTrailsPaginator,
    LookupEventsPaginator,
)
from .type_defs import (
    AdvancedEventSelectorUnionTypeDef,
    CancelQueryResponseTypeDef,
    CreateChannelResponseTypeDef,
    CreateEventDataStoreResponseTypeDef,
    CreateTrailResponseTypeDef,
    DescribeQueryResponseTypeDef,
    DescribeTrailsResponseTypeDef,
    DestinationTypeDef,
    DisableFederationResponseTypeDef,
    EnableFederationResponseTypeDef,
    EventSelectorUnionTypeDef,
    GetChannelResponseTypeDef,
    GetEventDataStoreResponseTypeDef,
    GetEventSelectorsResponseTypeDef,
    GetImportResponseTypeDef,
    GetInsightSelectorsResponseTypeDef,
    GetQueryResultsResponseTypeDef,
    GetResourcePolicyResponseTypeDef,
    GetTrailResponseTypeDef,
    GetTrailStatusResponseTypeDef,
    ImportSourceTypeDef,
    InsightSelectorTypeDef,
    ListChannelsResponseTypeDef,
    ListEventDataStoresResponseTypeDef,
    ListImportFailuresResponseTypeDef,
    ListImportsResponseTypeDef,
    ListInsightsMetricDataResponseTypeDef,
    ListPublicKeysResponseTypeDef,
    ListQueriesResponseTypeDef,
    ListTagsResponseTypeDef,
    ListTrailsResponseTypeDef,
    LookupAttributeTypeDef,
    LookupEventsResponseTypeDef,
    PutEventSelectorsResponseTypeDef,
    PutInsightSelectorsResponseTypeDef,
    PutResourcePolicyResponseTypeDef,
    RestoreEventDataStoreResponseTypeDef,
    StartImportResponseTypeDef,
    StartQueryResponseTypeDef,
    StopImportResponseTypeDef,
    TagTypeDef,
    TimestampTypeDef,
    UpdateChannelResponseTypeDef,
    UpdateEventDataStoreResponseTypeDef,
    UpdateTrailResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("CloudTrailClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    AccountHasOngoingImportException: Type[BotocoreClientError]
    AccountNotFoundException: Type[BotocoreClientError]
    AccountNotRegisteredException: Type[BotocoreClientError]
    AccountRegisteredException: Type[BotocoreClientError]
    CannotDelegateManagementAccountException: Type[BotocoreClientError]
    ChannelARNInvalidException: Type[BotocoreClientError]
    ChannelAlreadyExistsException: Type[BotocoreClientError]
    ChannelExistsForEDSException: Type[BotocoreClientError]
    ChannelMaxLimitExceededException: Type[BotocoreClientError]
    ChannelNotFoundException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    CloudTrailARNInvalidException: Type[BotocoreClientError]
    CloudTrailAccessNotEnabledException: Type[BotocoreClientError]
    CloudTrailInvalidClientTokenIdException: Type[BotocoreClientError]
    CloudWatchLogsDeliveryUnavailableException: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DelegatedAdminAccountLimitExceededException: Type[BotocoreClientError]
    EventDataStoreARNInvalidException: Type[BotocoreClientError]
    EventDataStoreAlreadyExistsException: Type[BotocoreClientError]
    EventDataStoreFederationEnabledException: Type[BotocoreClientError]
    EventDataStoreHasOngoingImportException: Type[BotocoreClientError]
    EventDataStoreMaxLimitExceededException: Type[BotocoreClientError]
    EventDataStoreNotFoundException: Type[BotocoreClientError]
    EventDataStoreTerminationProtectedException: Type[BotocoreClientError]
    ImportNotFoundException: Type[BotocoreClientError]
    InactiveEventDataStoreException: Type[BotocoreClientError]
    InactiveQueryException: Type[BotocoreClientError]
    InsightNotEnabledException: Type[BotocoreClientError]
    InsufficientDependencyServiceAccessPermissionException: Type[BotocoreClientError]
    InsufficientEncryptionPolicyException: Type[BotocoreClientError]
    InsufficientS3BucketPolicyException: Type[BotocoreClientError]
    InsufficientSnsTopicPolicyException: Type[BotocoreClientError]
    InvalidCloudWatchLogsLogGroupArnException: Type[BotocoreClientError]
    InvalidCloudWatchLogsRoleArnException: Type[BotocoreClientError]
    InvalidDateRangeException: Type[BotocoreClientError]
    InvalidEventCategoryException: Type[BotocoreClientError]
    InvalidEventDataStoreCategoryException: Type[BotocoreClientError]
    InvalidEventDataStoreStatusException: Type[BotocoreClientError]
    InvalidEventSelectorsException: Type[BotocoreClientError]
    InvalidHomeRegionException: Type[BotocoreClientError]
    InvalidImportSourceException: Type[BotocoreClientError]
    InvalidInsightSelectorsException: Type[BotocoreClientError]
    InvalidKmsKeyIdException: Type[BotocoreClientError]
    InvalidLookupAttributesException: Type[BotocoreClientError]
    InvalidMaxResultsException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidParameterCombinationException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidQueryStatementException: Type[BotocoreClientError]
    InvalidQueryStatusException: Type[BotocoreClientError]
    InvalidS3BucketNameException: Type[BotocoreClientError]
    InvalidS3PrefixException: Type[BotocoreClientError]
    InvalidSnsTopicNameException: Type[BotocoreClientError]
    InvalidSourceException: Type[BotocoreClientError]
    InvalidTagParameterException: Type[BotocoreClientError]
    InvalidTimeRangeException: Type[BotocoreClientError]
    InvalidTokenException: Type[BotocoreClientError]
    InvalidTrailNameException: Type[BotocoreClientError]
    KmsException: Type[BotocoreClientError]
    KmsKeyDisabledException: Type[BotocoreClientError]
    KmsKeyNotFoundException: Type[BotocoreClientError]
    MaxConcurrentQueriesException: Type[BotocoreClientError]
    MaximumNumberOfTrailsExceededException: Type[BotocoreClientError]
    NoManagementAccountSLRExistsException: Type[BotocoreClientError]
    NotOrganizationManagementAccountException: Type[BotocoreClientError]
    NotOrganizationMasterAccountException: Type[BotocoreClientError]
    OperationNotPermittedException: Type[BotocoreClientError]
    OrganizationNotInAllFeaturesModeException: Type[BotocoreClientError]
    OrganizationsNotInUseException: Type[BotocoreClientError]
    QueryIdNotFoundException: Type[BotocoreClientError]
    ResourceARNNotValidException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourcePolicyNotFoundException: Type[BotocoreClientError]
    ResourcePolicyNotValidException: Type[BotocoreClientError]
    ResourceTypeNotSupportedException: Type[BotocoreClientError]
    S3BucketDoesNotExistException: Type[BotocoreClientError]
    TagsLimitExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TrailAlreadyExistsException: Type[BotocoreClientError]
    TrailNotFoundException: Type[BotocoreClientError]
    TrailNotProvidedException: Type[BotocoreClientError]
    UnsupportedOperationException: Type[BotocoreClientError]


class CloudTrailClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudTrailClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#exceptions)
        """

    def add_tags(self, *, ResourceId: str, TagsList: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Adds one or more tags to a trail, event data store, or channel, up to a limit
        of
        50.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.add_tags)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#add_tags)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#can_paginate)
        """

    def cancel_query(
        self, *, QueryId: str, EventDataStore: str = ...
    ) -> CancelQueryResponseTypeDef:
        """
        Cancels a query if the query is not in a terminated state, such as `CANCELLED`,
        `FAILED`, `TIMED_OUT`, or
        `FINISHED`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.cancel_query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#cancel_query)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#close)
        """

    def create_channel(
        self,
        *,
        Name: str,
        Source: str,
        Destinations: Sequence[DestinationTypeDef],
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateChannelResponseTypeDef:
        """
        Creates a channel for CloudTrail to ingest events from a partner or external
        source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.create_channel)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#create_channel)
        """

    def create_event_data_store(
        self,
        *,
        Name: str,
        AdvancedEventSelectors: Sequence[AdvancedEventSelectorUnionTypeDef] = ...,
        MultiRegionEnabled: bool = ...,
        OrganizationEnabled: bool = ...,
        RetentionPeriod: int = ...,
        TerminationProtectionEnabled: bool = ...,
        TagsList: Sequence[TagTypeDef] = ...,
        KmsKeyId: str = ...,
        StartIngestion: bool = ...,
        BillingMode: BillingModeType = ...,
    ) -> CreateEventDataStoreResponseTypeDef:
        """
        Creates a new event data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.create_event_data_store)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#create_event_data_store)
        """

    def create_trail(
        self,
        *,
        Name: str,
        S3BucketName: str,
        S3KeyPrefix: str = ...,
        SnsTopicName: str = ...,
        IncludeGlobalServiceEvents: bool = ...,
        IsMultiRegionTrail: bool = ...,
        EnableLogFileValidation: bool = ...,
        CloudWatchLogsLogGroupArn: str = ...,
        CloudWatchLogsRoleArn: str = ...,
        KmsKeyId: str = ...,
        IsOrganizationTrail: bool = ...,
        TagsList: Sequence[TagTypeDef] = ...,
    ) -> CreateTrailResponseTypeDef:
        """
        Creates a trail that specifies the settings for delivery of log data to an
        Amazon S3
        bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.create_trail)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#create_trail)
        """

    def delete_channel(self, *, Channel: str) -> Dict[str, Any]:
        """
        Deletes a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.delete_channel)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#delete_channel)
        """

    def delete_event_data_store(self, *, EventDataStore: str) -> Dict[str, Any]:
        """
        Disables the event data store specified by `EventDataStore`, which accepts an
        event data store
        ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.delete_event_data_store)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#delete_event_data_store)
        """

    def delete_resource_policy(self, *, ResourceArn: str) -> Dict[str, Any]:
        """
        Deletes the resource-based policy attached to the CloudTrail channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.delete_resource_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#delete_resource_policy)
        """

    def delete_trail(self, *, Name: str) -> Dict[str, Any]:
        """
        Deletes a trail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.delete_trail)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#delete_trail)
        """

    def deregister_organization_delegated_admin(
        self, *, DelegatedAdminAccountId: str
    ) -> Dict[str, Any]:
        """
        Removes CloudTrail delegated administrator permissions from a member account in
        an
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.deregister_organization_delegated_admin)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#deregister_organization_delegated_admin)
        """

    def describe_query(
        self, *, EventDataStore: str = ..., QueryId: str = ..., QueryAlias: str = ...
    ) -> DescribeQueryResponseTypeDef:
        """
        Returns metadata about a query, including query run time in milliseconds,
        number of events scanned and matched, and query
        status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.describe_query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#describe_query)
        """

    def describe_trails(
        self, *, trailNameList: Sequence[str] = ..., includeShadowTrails: bool = ...
    ) -> DescribeTrailsResponseTypeDef:
        """
        Retrieves settings for one or more trails associated with the current Region
        for your
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.describe_trails)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#describe_trails)
        """

    def disable_federation(self, *, EventDataStore: str) -> DisableFederationResponseTypeDef:
        """
        Disables Lake query federation on the specified event data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.disable_federation)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#disable_federation)
        """

    def enable_federation(
        self, *, EventDataStore: str, FederationRoleArn: str
    ) -> EnableFederationResponseTypeDef:
        """
        Enables Lake query federation on the specified event data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.enable_federation)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#enable_federation)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#generate_presigned_url)
        """

    def get_channel(self, *, Channel: str) -> GetChannelResponseTypeDef:
        """
        Returns information about a specific channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.get_channel)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_channel)
        """

    def get_event_data_store(self, *, EventDataStore: str) -> GetEventDataStoreResponseTypeDef:
        """
        Returns information about an event data store specified as either an ARN or the
        ID portion of the
        ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.get_event_data_store)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_event_data_store)
        """

    def get_event_selectors(self, *, TrailName: str) -> GetEventSelectorsResponseTypeDef:
        """
        Describes the settings for the event selectors that you configured for your
        trail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.get_event_selectors)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_event_selectors)
        """

    def get_import(self, *, ImportId: str) -> GetImportResponseTypeDef:
        """
        Returns information about a specific import.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.get_import)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_import)
        """

    def get_insight_selectors(
        self, *, TrailName: str = ..., EventDataStore: str = ...
    ) -> GetInsightSelectorsResponseTypeDef:
        """
        Describes the settings for the Insights event selectors that you configured for
        your trail or event data
        store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.get_insight_selectors)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_insight_selectors)
        """

    def get_query_results(
        self,
        *,
        QueryId: str,
        EventDataStore: str = ...,
        NextToken: str = ...,
        MaxQueryResults: int = ...,
    ) -> GetQueryResultsResponseTypeDef:
        """
        Gets event data results of a query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.get_query_results)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_query_results)
        """

    def get_resource_policy(self, *, ResourceArn: str) -> GetResourcePolicyResponseTypeDef:
        """
        Retrieves the JSON text of the resource-based policy document attached to the
        CloudTrail
        channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.get_resource_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_resource_policy)
        """

    def get_trail(self, *, Name: str) -> GetTrailResponseTypeDef:
        """
        Returns settings information for a specified trail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.get_trail)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_trail)
        """

    def get_trail_status(self, *, Name: str) -> GetTrailStatusResponseTypeDef:
        """
        Returns a JSON-formatted list of information about the specified trail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.get_trail_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_trail_status)
        """

    def list_channels(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListChannelsResponseTypeDef:
        """
        Lists the channels in the current account, and their source names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.list_channels)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#list_channels)
        """

    def list_event_data_stores(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListEventDataStoresResponseTypeDef:
        """
        Returns information about all event data stores in the account, in the current
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.list_event_data_stores)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#list_event_data_stores)
        """

    def list_import_failures(
        self, *, ImportId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListImportFailuresResponseTypeDef:
        """
        Returns a list of failures for the specified import.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.list_import_failures)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#list_import_failures)
        """

    def list_imports(
        self,
        *,
        MaxResults: int = ...,
        Destination: str = ...,
        ImportStatus: ImportStatusType = ...,
        NextToken: str = ...,
    ) -> ListImportsResponseTypeDef:
        """
        Returns information on all imports, or a select set of imports by
        `ImportStatus` or
        `Destination`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.list_imports)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#list_imports)
        """

    def list_insights_metric_data(
        self,
        *,
        EventSource: str,
        EventName: str,
        InsightType: InsightTypeType,
        ErrorCode: str = ...,
        StartTime: TimestampTypeDef = ...,
        EndTime: TimestampTypeDef = ...,
        Period: int = ...,
        DataType: InsightsMetricDataTypeType = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> ListInsightsMetricDataResponseTypeDef:
        """
        Returns Insights metrics data for trails that have enabled Insights.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.list_insights_metric_data)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#list_insights_metric_data)
        """

    def list_public_keys(
        self,
        *,
        StartTime: TimestampTypeDef = ...,
        EndTime: TimestampTypeDef = ...,
        NextToken: str = ...,
    ) -> ListPublicKeysResponseTypeDef:
        """
        Returns all public keys whose private keys were used to sign the digest files
        within the specified time
        range.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.list_public_keys)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#list_public_keys)
        """

    def list_queries(
        self,
        *,
        EventDataStore: str,
        NextToken: str = ...,
        MaxResults: int = ...,
        StartTime: TimestampTypeDef = ...,
        EndTime: TimestampTypeDef = ...,
        QueryStatus: QueryStatusType = ...,
    ) -> ListQueriesResponseTypeDef:
        """
        Returns a list of queries and query statuses for the past seven days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.list_queries)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#list_queries)
        """

    def list_tags(
        self, *, ResourceIdList: Sequence[str], NextToken: str = ...
    ) -> ListTagsResponseTypeDef:
        """
        Lists the tags for the specified trails, event data stores, or channels in the
        current
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.list_tags)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#list_tags)
        """

    def list_trails(self, *, NextToken: str = ...) -> ListTrailsResponseTypeDef:
        """
        Lists trails that are in the current account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.list_trails)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#list_trails)
        """

    def lookup_events(
        self,
        *,
        LookupAttributes: Sequence[LookupAttributeTypeDef] = ...,
        StartTime: TimestampTypeDef = ...,
        EndTime: TimestampTypeDef = ...,
        EventCategory: Literal["insight"] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> LookupEventsResponseTypeDef:
        """
        Looks up [management
        events](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-concepts.html#cloudtrail-concepts-management-events)
        or `CloudTrail Insights events
        <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-concepts.html#cloudtrail-concepts-insigh...`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.lookup_events)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#lookup_events)
        """

    def put_event_selectors(
        self,
        *,
        TrailName: str,
        EventSelectors: Sequence[EventSelectorUnionTypeDef] = ...,
        AdvancedEventSelectors: Sequence[AdvancedEventSelectorUnionTypeDef] = ...,
    ) -> PutEventSelectorsResponseTypeDef:
        """
        Configures an event selector or advanced event selectors for your trail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.put_event_selectors)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#put_event_selectors)
        """

    def put_insight_selectors(
        self,
        *,
        InsightSelectors: Sequence[InsightSelectorTypeDef],
        TrailName: str = ...,
        EventDataStore: str = ...,
        InsightsDestination: str = ...,
    ) -> PutInsightSelectorsResponseTypeDef:
        """
        Lets you enable Insights event logging by specifying the Insights selectors
        that you want to enable on an existing trail or event data
        store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.put_insight_selectors)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#put_insight_selectors)
        """

    def put_resource_policy(
        self, *, ResourceArn: str, ResourcePolicy: str
    ) -> PutResourcePolicyResponseTypeDef:
        """
        Attaches a resource-based permission policy to a CloudTrail channel that is
        used for an integration with an event source outside of Amazon Web
        Services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.put_resource_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#put_resource_policy)
        """

    def register_organization_delegated_admin(self, *, MemberAccountId: str) -> Dict[str, Any]:
        """
        Registers an organization's member account as the CloudTrail [delegated
        administrator](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-delegated-administrator.html).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.register_organization_delegated_admin)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#register_organization_delegated_admin)
        """

    def remove_tags(self, *, ResourceId: str, TagsList: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Removes the specified tags from a trail, event data store, or channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.remove_tags)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#remove_tags)
        """

    def restore_event_data_store(
        self, *, EventDataStore: str
    ) -> RestoreEventDataStoreResponseTypeDef:
        """
        Restores a deleted event data store specified by `EventDataStore`, which
        accepts an event data store
        ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.restore_event_data_store)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#restore_event_data_store)
        """

    def start_event_data_store_ingestion(self, *, EventDataStore: str) -> Dict[str, Any]:
        """
        Starts the ingestion of live events on an event data store specified as either
        an ARN or the ID portion of the
        ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.start_event_data_store_ingestion)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#start_event_data_store_ingestion)
        """

    def start_import(
        self,
        *,
        Destinations: Sequence[str] = ...,
        ImportSource: ImportSourceTypeDef = ...,
        StartEventTime: TimestampTypeDef = ...,
        EndEventTime: TimestampTypeDef = ...,
        ImportId: str = ...,
    ) -> StartImportResponseTypeDef:
        """
        Starts an import of logged trail events from a source S3 bucket to a
        destination event data
        store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.start_import)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#start_import)
        """

    def start_logging(self, *, Name: str) -> Dict[str, Any]:
        """
        Starts the recording of Amazon Web Services API calls and log file delivery for
        a
        trail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.start_logging)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#start_logging)
        """

    def start_query(
        self,
        *,
        QueryStatement: str = ...,
        DeliveryS3Uri: str = ...,
        QueryAlias: str = ...,
        QueryParameters: Sequence[str] = ...,
    ) -> StartQueryResponseTypeDef:
        """
        Starts a CloudTrail Lake query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.start_query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#start_query)
        """

    def stop_event_data_store_ingestion(self, *, EventDataStore: str) -> Dict[str, Any]:
        """
        Stops the ingestion of live events on an event data store specified as either
        an ARN or the ID portion of the
        ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.stop_event_data_store_ingestion)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#stop_event_data_store_ingestion)
        """

    def stop_import(self, *, ImportId: str) -> StopImportResponseTypeDef:
        """
        Stops a specified import.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.stop_import)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#stop_import)
        """

    def stop_logging(self, *, Name: str) -> Dict[str, Any]:
        """
        Suspends the recording of Amazon Web Services API calls and log file delivery
        for the specified
        trail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.stop_logging)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#stop_logging)
        """

    def update_channel(
        self, *, Channel: str, Destinations: Sequence[DestinationTypeDef] = ..., Name: str = ...
    ) -> UpdateChannelResponseTypeDef:
        """
        Updates a channel specified by a required channel ARN or UUID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.update_channel)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#update_channel)
        """

    def update_event_data_store(
        self,
        *,
        EventDataStore: str,
        Name: str = ...,
        AdvancedEventSelectors: Sequence[AdvancedEventSelectorUnionTypeDef] = ...,
        MultiRegionEnabled: bool = ...,
        OrganizationEnabled: bool = ...,
        RetentionPeriod: int = ...,
        TerminationProtectionEnabled: bool = ...,
        KmsKeyId: str = ...,
        BillingMode: BillingModeType = ...,
    ) -> UpdateEventDataStoreResponseTypeDef:
        """
        Updates an event data store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.update_event_data_store)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#update_event_data_store)
        """

    def update_trail(
        self,
        *,
        Name: str,
        S3BucketName: str = ...,
        S3KeyPrefix: str = ...,
        SnsTopicName: str = ...,
        IncludeGlobalServiceEvents: bool = ...,
        IsMultiRegionTrail: bool = ...,
        EnableLogFileValidation: bool = ...,
        CloudWatchLogsLogGroupArn: str = ...,
        CloudWatchLogsRoleArn: str = ...,
        KmsKeyId: str = ...,
        IsOrganizationTrail: bool = ...,
    ) -> UpdateTrailResponseTypeDef:
        """
        Updates trail settings that control what events you are logging, and how to
        handle log
        files.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.update_trail)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#update_trail)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_import_failures"]
    ) -> ListImportFailuresPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_imports"]) -> ListImportsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_public_keys"]) -> ListPublicKeysPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tags"]) -> ListTagsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_trails"]) -> ListTrailsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["lookup_events"]) -> LookupEventsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudtrail/client/#get_paginator)
        """
