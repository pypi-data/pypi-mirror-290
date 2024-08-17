"""
Type annotations for detective service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_detective.client import DetectiveClient

    session = Session()
    client: DetectiveClient = session.client("detective")
    ```
"""

from typing import Any, Dict, Mapping, Sequence, Type

from botocore.client import BaseClient, ClientMeta

from .literals import DatasourcePackageType, IndicatorTypeType, StateType
from .type_defs import (
    AccountTypeDef,
    BatchGetGraphMemberDatasourcesResponseTypeDef,
    BatchGetMembershipDatasourcesResponseTypeDef,
    CreateGraphResponseTypeDef,
    CreateMembersResponseTypeDef,
    DeleteMembersResponseTypeDef,
    DescribeOrganizationConfigurationResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    FilterCriteriaTypeDef,
    GetInvestigationResponseTypeDef,
    GetMembersResponseTypeDef,
    ListDatasourcePackagesResponseTypeDef,
    ListGraphsResponseTypeDef,
    ListIndicatorsResponseTypeDef,
    ListInvestigationsResponseTypeDef,
    ListInvitationsResponseTypeDef,
    ListMembersResponseTypeDef,
    ListOrganizationAdminAccountsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    SortCriteriaTypeDef,
    StartInvestigationResponseTypeDef,
    TimestampTypeDef,
)

__all__ = ("DetectiveClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class DetectiveClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DetectiveClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#exceptions)
        """

    def accept_invitation(self, *, GraphArn: str) -> EmptyResponseMetadataTypeDef:
        """
        Accepts an invitation for the member account to contribute data to a behavior
        graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.accept_invitation)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#accept_invitation)
        """

    def batch_get_graph_member_datasources(
        self, *, GraphArn: str, AccountIds: Sequence[str]
    ) -> BatchGetGraphMemberDatasourcesResponseTypeDef:
        """
        Gets data source package information for the behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.batch_get_graph_member_datasources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#batch_get_graph_member_datasources)
        """

    def batch_get_membership_datasources(
        self, *, GraphArns: Sequence[str]
    ) -> BatchGetMembershipDatasourcesResponseTypeDef:
        """
        Gets information on the data source package history for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.batch_get_membership_datasources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#batch_get_membership_datasources)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#close)
        """

    def create_graph(self, *, Tags: Mapping[str, str] = ...) -> CreateGraphResponseTypeDef:
        """
        Creates a new behavior graph for the calling account, and sets that account as
        the administrator
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.create_graph)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#create_graph)
        """

    def create_members(
        self,
        *,
        GraphArn: str,
        Accounts: Sequence[AccountTypeDef],
        Message: str = ...,
        DisableEmailNotification: bool = ...,
    ) -> CreateMembersResponseTypeDef:
        """
        `CreateMembers` is used to send invitations to accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.create_members)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#create_members)
        """

    def delete_graph(self, *, GraphArn: str) -> EmptyResponseMetadataTypeDef:
        """
        Disables the specified behavior graph and queues it to be deleted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.delete_graph)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#delete_graph)
        """

    def delete_members(
        self, *, GraphArn: str, AccountIds: Sequence[str]
    ) -> DeleteMembersResponseTypeDef:
        """
        Removes the specified member accounts from the behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.delete_members)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#delete_members)
        """

    def describe_organization_configuration(
        self, *, GraphArn: str
    ) -> DescribeOrganizationConfigurationResponseTypeDef:
        """
        Returns information about the configuration for the organization behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.describe_organization_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#describe_organization_configuration)
        """

    def disable_organization_admin_account(self) -> EmptyResponseMetadataTypeDef:
        """
        Removes the Detective administrator account in the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.disable_organization_admin_account)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#disable_organization_admin_account)
        """

    def disassociate_membership(self, *, GraphArn: str) -> EmptyResponseMetadataTypeDef:
        """
        Removes the member account from the specified behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.disassociate_membership)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#disassociate_membership)
        """

    def enable_organization_admin_account(self, *, AccountId: str) -> EmptyResponseMetadataTypeDef:
        """
        Designates the Detective administrator account for the organization in the
        current
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.enable_organization_admin_account)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#enable_organization_admin_account)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#generate_presigned_url)
        """

    def get_investigation(
        self, *, GraphArn: str, InvestigationId: str
    ) -> GetInvestigationResponseTypeDef:
        """
        Detective investigations lets you investigate IAM users and IAM roles using
        indicators of
        compromise.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.get_investigation)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#get_investigation)
        """

    def get_members(self, *, GraphArn: str, AccountIds: Sequence[str]) -> GetMembersResponseTypeDef:
        """
        Returns the membership details for specified member accounts for a behavior
        graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.get_members)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#get_members)
        """

    def list_datasource_packages(
        self, *, GraphArn: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListDatasourcePackagesResponseTypeDef:
        """
        Lists data source packages in the behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.list_datasource_packages)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#list_datasource_packages)
        """

    def list_graphs(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListGraphsResponseTypeDef:
        """
        Returns the list of behavior graphs that the calling account is an
        administrator account
        of.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.list_graphs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#list_graphs)
        """

    def list_indicators(
        self,
        *,
        GraphArn: str,
        InvestigationId: str,
        IndicatorType: IndicatorTypeType = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> ListIndicatorsResponseTypeDef:
        """
        Gets the indicators from an investigation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.list_indicators)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#list_indicators)
        """

    def list_investigations(
        self,
        *,
        GraphArn: str,
        NextToken: str = ...,
        MaxResults: int = ...,
        FilterCriteria: FilterCriteriaTypeDef = ...,
        SortCriteria: SortCriteriaTypeDef = ...,
    ) -> ListInvestigationsResponseTypeDef:
        """
        Detective investigations lets you investigate IAM users and IAM roles using
        indicators of
        compromise.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.list_investigations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#list_investigations)
        """

    def list_invitations(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListInvitationsResponseTypeDef:
        """
        Retrieves the list of open and accepted behavior graph invitations for the
        member
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.list_invitations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#list_invitations)
        """

    def list_members(
        self, *, GraphArn: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListMembersResponseTypeDef:
        """
        Retrieves the list of member accounts for a behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.list_members)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#list_members)
        """

    def list_organization_admin_accounts(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListOrganizationAdminAccountsResponseTypeDef:
        """
        Returns information about the Detective administrator account for an
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.list_organization_admin_accounts)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#list_organization_admin_accounts)
        """

    def list_tags_for_resource(self, *, ResourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Returns the tag values that are assigned to a behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#list_tags_for_resource)
        """

    def reject_invitation(self, *, GraphArn: str) -> EmptyResponseMetadataTypeDef:
        """
        Rejects an invitation to contribute the account data to a behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.reject_invitation)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#reject_invitation)
        """

    def start_investigation(
        self,
        *,
        GraphArn: str,
        EntityArn: str,
        ScopeStartTime: TimestampTypeDef,
        ScopeEndTime: TimestampTypeDef,
    ) -> StartInvestigationResponseTypeDef:
        """
        Detective investigations lets you investigate IAM users and IAM roles using
        indicators of
        compromise.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.start_investigation)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#start_investigation)
        """

    def start_monitoring_member(
        self, *, GraphArn: str, AccountId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sends a request to enable data ingest for a member account that has a status of
        `ACCEPTED_BUT_DISABLED`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.start_monitoring_member)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#start_monitoring_member)
        """

    def tag_resource(self, *, ResourceArn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Applies tag values to a behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#tag_resource)
        """

    def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from a behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#untag_resource)
        """

    def update_datasource_packages(
        self, *, GraphArn: str, DatasourcePackages: Sequence[DatasourcePackageType]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Starts a data source packages for the behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.update_datasource_packages)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#update_datasource_packages)
        """

    def update_investigation_state(
        self, *, GraphArn: str, InvestigationId: str, State: StateType
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the state of an investigation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.update_investigation_state)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#update_investigation_state)
        """

    def update_organization_configuration(
        self, *, GraphArn: str, AutoEnable: bool = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the configuration for the Organizations integration in the current
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client.update_organization_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_detective/client/#update_organization_configuration)
        """
