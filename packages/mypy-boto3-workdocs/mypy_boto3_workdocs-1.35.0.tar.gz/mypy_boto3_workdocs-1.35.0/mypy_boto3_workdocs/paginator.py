"""
Type annotations for workdocs service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_workdocs.client import WorkDocsClient
    from mypy_boto3_workdocs.paginator import (
        DescribeActivitiesPaginator,
        DescribeCommentsPaginator,
        DescribeDocumentVersionsPaginator,
        DescribeFolderContentsPaginator,
        DescribeGroupsPaginator,
        DescribeNotificationSubscriptionsPaginator,
        DescribeResourcePermissionsPaginator,
        DescribeRootFoldersPaginator,
        DescribeUsersPaginator,
        SearchResourcesPaginator,
    )

    session = Session()
    client: WorkDocsClient = session.client("workdocs")

    describe_activities_paginator: DescribeActivitiesPaginator = client.get_paginator("describe_activities")
    describe_comments_paginator: DescribeCommentsPaginator = client.get_paginator("describe_comments")
    describe_document_versions_paginator: DescribeDocumentVersionsPaginator = client.get_paginator("describe_document_versions")
    describe_folder_contents_paginator: DescribeFolderContentsPaginator = client.get_paginator("describe_folder_contents")
    describe_groups_paginator: DescribeGroupsPaginator = client.get_paginator("describe_groups")
    describe_notification_subscriptions_paginator: DescribeNotificationSubscriptionsPaginator = client.get_paginator("describe_notification_subscriptions")
    describe_resource_permissions_paginator: DescribeResourcePermissionsPaginator = client.get_paginator("describe_resource_permissions")
    describe_root_folders_paginator: DescribeRootFoldersPaginator = client.get_paginator("describe_root_folders")
    describe_users_paginator: DescribeUsersPaginator = client.get_paginator("describe_users")
    search_resources_paginator: SearchResourcesPaginator = client.get_paginator("search_resources")
    ```
"""

import sys
from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator, Paginator

from .literals import (
    FolderContentTypeType,
    OrderTypeType,
    ResourceSortTypeType,
    SearchQueryScopeTypeType,
    UserFilterTypeType,
    UserSortTypeType,
)
from .type_defs import (
    DescribeActivitiesResponseTypeDef,
    DescribeCommentsResponseTypeDef,
    DescribeDocumentVersionsResponseTypeDef,
    DescribeFolderContentsResponseTypeDef,
    DescribeGroupsResponseTypeDef,
    DescribeNotificationSubscriptionsResponseTypeDef,
    DescribeResourcePermissionsResponseTypeDef,
    DescribeRootFoldersResponseTypeDef,
    DescribeUsersResponseTypeDef,
    FiltersTypeDef,
    PaginatorConfigTypeDef,
    SearchResourcesResponseTypeDef,
    SearchSortResultTypeDef,
    TimestampTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "DescribeActivitiesPaginator",
    "DescribeCommentsPaginator",
    "DescribeDocumentVersionsPaginator",
    "DescribeFolderContentsPaginator",
    "DescribeGroupsPaginator",
    "DescribeNotificationSubscriptionsPaginator",
    "DescribeResourcePermissionsPaginator",
    "DescribeRootFoldersPaginator",
    "DescribeUsersPaginator",
    "SearchResourcesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeActivitiesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeActivities)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/paginators/#describeactivitiespaginator)
    """

    def paginate(
        self,
        *,
        AuthenticationToken: str = ...,
        StartTime: TimestampTypeDef = ...,
        EndTime: TimestampTypeDef = ...,
        OrganizationId: str = ...,
        ActivityTypes: str = ...,
        ResourceId: str = ...,
        UserId: str = ...,
        IncludeIndirectActivities: bool = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[DescribeActivitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeActivities.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/paginators/#describeactivitiespaginator)
        """


class DescribeCommentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeComments)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/paginators/#describecommentspaginator)
    """

    def paginate(
        self,
        *,
        DocumentId: str,
        VersionId: str,
        AuthenticationToken: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[DescribeCommentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeComments.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/paginators/#describecommentspaginator)
        """


class DescribeDocumentVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeDocumentVersions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/paginators/#describedocumentversionspaginator)
    """

    def paginate(
        self,
        *,
        DocumentId: str,
        AuthenticationToken: str = ...,
        Include: str = ...,
        Fields: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[DescribeDocumentVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeDocumentVersions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/paginators/#describedocumentversionspaginator)
        """


class DescribeFolderContentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeFolderContents)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/paginators/#describefoldercontentspaginator)
    """

    def paginate(
        self,
        *,
        FolderId: str,
        AuthenticationToken: str = ...,
        Sort: ResourceSortTypeType = ...,
        Order: OrderTypeType = ...,
        Type: FolderContentTypeType = ...,
        Include: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[DescribeFolderContentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeFolderContents.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/paginators/#describefoldercontentspaginator)
        """


class DescribeGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeGroups)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/paginators/#describegroupspaginator)
    """

    def paginate(
        self,
        *,
        SearchQuery: str,
        AuthenticationToken: str = ...,
        OrganizationId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[DescribeGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeGroups.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/paginators/#describegroupspaginator)
        """


class DescribeNotificationSubscriptionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeNotificationSubscriptions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/paginators/#describenotificationsubscriptionspaginator)
    """

    def paginate(
        self, *, OrganizationId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeNotificationSubscriptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeNotificationSubscriptions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/paginators/#describenotificationsubscriptionspaginator)
        """


class DescribeResourcePermissionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeResourcePermissions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/paginators/#describeresourcepermissionspaginator)
    """

    def paginate(
        self,
        *,
        ResourceId: str,
        AuthenticationToken: str = ...,
        PrincipalId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[DescribeResourcePermissionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeResourcePermissions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/paginators/#describeresourcepermissionspaginator)
        """


class DescribeRootFoldersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeRootFolders)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/paginators/#describerootfolderspaginator)
    """

    def paginate(
        self, *, AuthenticationToken: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeRootFoldersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeRootFolders.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/paginators/#describerootfolderspaginator)
        """


class DescribeUsersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeUsers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/paginators/#describeuserspaginator)
    """

    def paginate(
        self,
        *,
        AuthenticationToken: str = ...,
        OrganizationId: str = ...,
        UserIds: str = ...,
        Query: str = ...,
        Include: UserFilterTypeType = ...,
        Order: OrderTypeType = ...,
        Sort: UserSortTypeType = ...,
        Fields: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[DescribeUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.DescribeUsers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/paginators/#describeuserspaginator)
        """


class SearchResourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.SearchResources)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/paginators/#searchresourcespaginator)
    """

    def paginate(
        self,
        *,
        AuthenticationToken: str = ...,
        QueryText: str = ...,
        QueryScopes: Sequence[SearchQueryScopeTypeType] = ...,
        OrganizationId: str = ...,
        AdditionalResponseFields: Sequence[Literal["WEBURL"]] = ...,
        Filters: FiltersTypeDef = ...,
        OrderBy: Sequence[SearchSortResultTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[SearchResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Paginator.SearchResources.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_workdocs/paginators/#searchresourcespaginator)
        """
