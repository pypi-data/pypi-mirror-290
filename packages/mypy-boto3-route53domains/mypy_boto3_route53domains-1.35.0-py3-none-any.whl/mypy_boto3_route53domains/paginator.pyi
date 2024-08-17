"""
Type annotations for route53domains service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53domains/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_route53domains.client import Route53DomainsClient
    from mypy_boto3_route53domains.paginator import (
        ListDomainsPaginator,
        ListOperationsPaginator,
        ListPricesPaginator,
        ViewBillingPaginator,
    )

    session = Session()
    client: Route53DomainsClient = session.client("route53domains")

    list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
    list_operations_paginator: ListOperationsPaginator = client.get_paginator("list_operations")
    list_prices_paginator: ListPricesPaginator = client.get_paginator("list_prices")
    view_billing_paginator: ViewBillingPaginator = client.get_paginator("view_billing")
    ```
"""

import sys
from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator, Paginator

from .literals import OperationStatusType, OperationTypeType, SortOrderType
from .type_defs import (
    FilterConditionTypeDef,
    ListDomainsResponseTypeDef,
    ListOperationsResponseTypeDef,
    ListPricesResponseTypeDef,
    PaginatorConfigTypeDef,
    SortConditionTypeDef,
    TimestampTypeDef,
    ViewBillingResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "ListDomainsPaginator",
    "ListOperationsPaginator",
    "ListPricesPaginator",
    "ViewBillingPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListDomainsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Paginator.ListDomains)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53domains/paginators/#listdomainspaginator)
    """

    def paginate(
        self,
        *,
        FilterConditions: Sequence[FilterConditionTypeDef] = ...,
        SortCondition: SortConditionTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListDomainsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Paginator.ListDomains.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53domains/paginators/#listdomainspaginator)
        """

class ListOperationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Paginator.ListOperations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53domains/paginators/#listoperationspaginator)
    """

    def paginate(
        self,
        *,
        SubmittedSince: TimestampTypeDef = ...,
        Status: Sequence[OperationStatusType] = ...,
        Type: Sequence[OperationTypeType] = ...,
        SortBy: Literal["SubmittedDate"] = ...,
        SortOrder: SortOrderType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListOperationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Paginator.ListOperations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53domains/paginators/#listoperationspaginator)
        """

class ListPricesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Paginator.ListPrices)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53domains/paginators/#listpricespaginator)
    """

    def paginate(
        self, *, Tld: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPricesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Paginator.ListPrices.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53domains/paginators/#listpricespaginator)
        """

class ViewBillingPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Paginator.ViewBilling)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53domains/paginators/#viewbillingpaginator)
    """

    def paginate(
        self,
        *,
        Start: TimestampTypeDef = ...,
        End: TimestampTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ViewBillingResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Paginator.ViewBilling.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53domains/paginators/#viewbillingpaginator)
        """
