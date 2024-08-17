"""
Type annotations for pipes service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pipes/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_pipes.client import EventBridgePipesClient
    from mypy_boto3_pipes.paginator import (
        ListPipesPaginator,
    )

    session = Session()
    client: EventBridgePipesClient = session.client("pipes")

    list_pipes_paginator: ListPipesPaginator = client.get_paginator("list_pipes")
    ```
"""

from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .literals import PipeStateType, RequestedPipeStateType
from .type_defs import ListPipesResponseTypeDef, PaginatorConfigTypeDef

__all__ = ("ListPipesPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListPipesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pipes.html#EventBridgePipes.Paginator.ListPipes)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pipes/paginators/#listpipespaginator)
    """

    def paginate(
        self,
        *,
        NamePrefix: str = ...,
        DesiredState: RequestedPipeStateType = ...,
        CurrentState: PipeStateType = ...,
        SourcePrefix: str = ...,
        TargetPrefix: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListPipesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pipes.html#EventBridgePipes.Paginator.ListPipes.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pipes/paginators/#listpipespaginator)
        """
