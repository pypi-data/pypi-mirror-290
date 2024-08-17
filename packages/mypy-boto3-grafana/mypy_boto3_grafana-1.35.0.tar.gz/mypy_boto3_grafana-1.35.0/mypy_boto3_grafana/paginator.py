"""
Type annotations for grafana service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_grafana.client import ManagedGrafanaClient
    from mypy_boto3_grafana.paginator import (
        ListPermissionsPaginator,
        ListVersionsPaginator,
        ListWorkspaceServiceAccountTokensPaginator,
        ListWorkspaceServiceAccountsPaginator,
        ListWorkspacesPaginator,
    )

    session = Session()
    client: ManagedGrafanaClient = session.client("grafana")

    list_permissions_paginator: ListPermissionsPaginator = client.get_paginator("list_permissions")
    list_versions_paginator: ListVersionsPaginator = client.get_paginator("list_versions")
    list_workspace_service_account_tokens_paginator: ListWorkspaceServiceAccountTokensPaginator = client.get_paginator("list_workspace_service_account_tokens")
    list_workspace_service_accounts_paginator: ListWorkspaceServiceAccountsPaginator = client.get_paginator("list_workspace_service_accounts")
    list_workspaces_paginator: ListWorkspacesPaginator = client.get_paginator("list_workspaces")
    ```
"""

from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .literals import UserTypeType
from .type_defs import (
    ListPermissionsResponseTypeDef,
    ListVersionsResponseTypeDef,
    ListWorkspaceServiceAccountsResponseTypeDef,
    ListWorkspaceServiceAccountTokensResponseTypeDef,
    ListWorkspacesResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListPermissionsPaginator",
    "ListVersionsPaginator",
    "ListWorkspaceServiceAccountTokensPaginator",
    "ListWorkspaceServiceAccountsPaginator",
    "ListWorkspacesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListPermissionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Paginator.ListPermissions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/paginators/#listpermissionspaginator)
    """

    def paginate(
        self,
        *,
        workspaceId: str,
        groupId: str = ...,
        userId: str = ...,
        userType: UserTypeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListPermissionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Paginator.ListPermissions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/paginators/#listpermissionspaginator)
        """


class ListVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Paginator.ListVersions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/paginators/#listversionspaginator)
    """

    def paginate(
        self, *, workspaceId: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Paginator.ListVersions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/paginators/#listversionspaginator)
        """


class ListWorkspaceServiceAccountTokensPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Paginator.ListWorkspaceServiceAccountTokens)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/paginators/#listworkspaceserviceaccounttokenspaginator)
    """

    def paginate(
        self,
        *,
        serviceAccountId: str,
        workspaceId: str,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListWorkspaceServiceAccountTokensResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Paginator.ListWorkspaceServiceAccountTokens.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/paginators/#listworkspaceserviceaccounttokenspaginator)
        """


class ListWorkspaceServiceAccountsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Paginator.ListWorkspaceServiceAccounts)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/paginators/#listworkspaceserviceaccountspaginator)
    """

    def paginate(
        self, *, workspaceId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListWorkspaceServiceAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Paginator.ListWorkspaceServiceAccounts.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/paginators/#listworkspaceserviceaccountspaginator)
        """


class ListWorkspacesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Paginator.ListWorkspaces)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/paginators/#listworkspacespaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListWorkspacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/grafana.html#ManagedGrafana.Paginator.ListWorkspaces.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_grafana/paginators/#listworkspacespaginator)
        """
