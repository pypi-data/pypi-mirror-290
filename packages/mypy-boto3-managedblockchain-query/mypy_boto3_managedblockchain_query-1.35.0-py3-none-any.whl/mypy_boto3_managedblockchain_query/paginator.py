"""
Type annotations for managedblockchain-query service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_managedblockchain_query/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_managedblockchain_query.client import ManagedBlockchainQueryClient
    from mypy_boto3_managedblockchain_query.paginator import (
        ListAssetContractsPaginator,
        ListFilteredTransactionEventsPaginator,
        ListTokenBalancesPaginator,
        ListTransactionEventsPaginator,
        ListTransactionsPaginator,
    )

    session = Session()
    client: ManagedBlockchainQueryClient = session.client("managedblockchain-query")

    list_asset_contracts_paginator: ListAssetContractsPaginator = client.get_paginator("list_asset_contracts")
    list_filtered_transaction_events_paginator: ListFilteredTransactionEventsPaginator = client.get_paginator("list_filtered_transaction_events")
    list_token_balances_paginator: ListTokenBalancesPaginator = client.get_paginator("list_token_balances")
    list_transaction_events_paginator: ListTransactionEventsPaginator = client.get_paginator("list_transaction_events")
    list_transactions_paginator: ListTransactionsPaginator = client.get_paginator("list_transactions")
    ```
"""

from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .literals import QueryNetworkType
from .type_defs import (
    AddressIdentifierFilterTypeDef,
    BlockchainInstantUnionTypeDef,
    ConfirmationStatusFilterTypeDef,
    ContractFilterTypeDef,
    ListAssetContractsOutputTypeDef,
    ListFilteredTransactionEventsOutputTypeDef,
    ListFilteredTransactionEventsSortTypeDef,
    ListTokenBalancesOutputTypeDef,
    ListTransactionEventsOutputTypeDef,
    ListTransactionsOutputTypeDef,
    ListTransactionsSortTypeDef,
    OwnerFilterTypeDef,
    PaginatorConfigTypeDef,
    TimeFilterTypeDef,
    TokenFilterTypeDef,
    VoutFilterTypeDef,
)

__all__ = (
    "ListAssetContractsPaginator",
    "ListFilteredTransactionEventsPaginator",
    "ListTokenBalancesPaginator",
    "ListTransactionEventsPaginator",
    "ListTransactionsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAssetContractsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query.html#ManagedBlockchainQuery.Paginator.ListAssetContracts)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_managedblockchain_query/paginators/#listassetcontractspaginator)
    """

    def paginate(
        self,
        *,
        contractFilter: ContractFilterTypeDef,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListAssetContractsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query.html#ManagedBlockchainQuery.Paginator.ListAssetContracts.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_managedblockchain_query/paginators/#listassetcontractspaginator)
        """


class ListFilteredTransactionEventsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query.html#ManagedBlockchainQuery.Paginator.ListFilteredTransactionEvents)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_managedblockchain_query/paginators/#listfilteredtransactioneventspaginator)
    """

    def paginate(
        self,
        *,
        network: str,
        addressIdentifierFilter: AddressIdentifierFilterTypeDef,
        timeFilter: TimeFilterTypeDef = ...,
        voutFilter: VoutFilterTypeDef = ...,
        confirmationStatusFilter: ConfirmationStatusFilterTypeDef = ...,
        sort: ListFilteredTransactionEventsSortTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListFilteredTransactionEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query.html#ManagedBlockchainQuery.Paginator.ListFilteredTransactionEvents.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_managedblockchain_query/paginators/#listfilteredtransactioneventspaginator)
        """


class ListTokenBalancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query.html#ManagedBlockchainQuery.Paginator.ListTokenBalances)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_managedblockchain_query/paginators/#listtokenbalancespaginator)
    """

    def paginate(
        self,
        *,
        tokenFilter: TokenFilterTypeDef,
        ownerFilter: OwnerFilterTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListTokenBalancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query.html#ManagedBlockchainQuery.Paginator.ListTokenBalances.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_managedblockchain_query/paginators/#listtokenbalancespaginator)
        """


class ListTransactionEventsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query.html#ManagedBlockchainQuery.Paginator.ListTransactionEvents)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_managedblockchain_query/paginators/#listtransactioneventspaginator)
    """

    def paginate(
        self,
        *,
        network: QueryNetworkType,
        transactionHash: str = ...,
        transactionId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListTransactionEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query.html#ManagedBlockchainQuery.Paginator.ListTransactionEvents.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_managedblockchain_query/paginators/#listtransactioneventspaginator)
        """


class ListTransactionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query.html#ManagedBlockchainQuery.Paginator.ListTransactions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_managedblockchain_query/paginators/#listtransactionspaginator)
    """

    def paginate(
        self,
        *,
        address: str,
        network: QueryNetworkType,
        fromBlockchainInstant: BlockchainInstantUnionTypeDef = ...,
        toBlockchainInstant: BlockchainInstantUnionTypeDef = ...,
        sort: ListTransactionsSortTypeDef = ...,
        confirmationStatusFilter: ConfirmationStatusFilterTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListTransactionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain-query.html#ManagedBlockchainQuery.Paginator.ListTransactions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_managedblockchain_query/paginators/#listtransactionspaginator)
        """
