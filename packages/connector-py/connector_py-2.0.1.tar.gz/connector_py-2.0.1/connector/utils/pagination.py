"""Utilities for resource pagination.

When providing unified interface for several third-party APIs, we stand
before a problem how to define the pagination interface. On the level
of connectors, we decided to use ``next_page_token`` parameter that
will contain all information necessary to paginate over the third-party
interface.

The SDK provides basic class for representing third-party pagination and
utilities for converting the third-party pagination parameters from and
to next page token.

Since a third-party API can have very specific pagination parameters,
its representation in Lumos system is very generic. Since we are not
sure about how much third-party "endpoints" are to be called for one
call of connector method, we decided to use a list of pagination
parameters to be included in one next page token. We also expect that
paginations will differ for all third-party endpoints called during
one connector method call.

At the connector level, you have to define your own representation of
third-party pagination parameters by subclassing ``PaginationBase``
model and then create a class for converting third-party pagination
parameters to and from next page token. The class is created by passing
the pagination parameters model to ``create_next_page_token`` function.

Some connector methods paginate their results. The method response
format is defined in :py:module:``connector.serializers.lumos`` and
will always be a subclass of :py:class:``ResponseWrapper``. The token
will be stored either in ``method_response.next_page_token`` (new
format) or in ``method_response.cursor.next`` (legacy way). To create
a token for your response, use the following: ::

    NextPageToken = create_next_page_token(model, "NextPageToken")
    next_page_token = NextPageToken.from_paginations(paginations)
    response = ResponseWrapper(
        reponse=your_data,
        ...,
        next_page_token=next_page_token.token,
    )

The token created with the ``NextPageTokenInterface`` subclass can be
used as an input for the next method call. To access the decoded
third-party pagination, use the following: ::

    class ArgsWithNextPageToken(...):
        next_page_token: str | None

    def your_method(args: ArgsWithNextPageToken) -> Response:
        paginations = NextPageToken(token=args.next_page_token).paginations()
        for pagination in paginations:
            # each pagination is the third-party pagination object
            pass
"""

import abc
import dataclasses
import typing as t

import msgpack
import pydantic


class PaginationBase(pydantic.BaseModel):
    """Base class for all third-party paginations.

    Connectors will most likely inherit this class and put the params
    specific to third-party API there.

    Attributes
    ----------
    endpoint:
        Name of endpoint that should be called by the connector. This
        could serve not only for http client but also for all other
        types. The information about where to send the "request" should
        go there.

    resource_type:
        Type of resource representing pagination entity. This could be
        used for logging purposes or for any other purpose where we
        need to know what kind of resource we are working with.

    """

    endpoint: str | None = None
    resource_type: str | None = None

    model_config = pydantic.ConfigDict(
        extra="forbid",
    )


PT = t.TypeVar("PT", bound=PaginationBase)


@dataclasses.dataclass
class NextPageTokenInterface(abc.ABC, t.Generic[PT]):
    """Interface for class that handles next page token serialization.

    Each connector has specific format of third-party API pagination
    represented with a subclass of ``PaginationBase``. The resulted
    token class will provide functionality to encode the third-party
    pagination parameters into next page token that is a part of
    connector interface.
    """

    token: str

    @classmethod
    @abc.abstractmethod
    def from_paginations(cls, paginations: list[PT]) -> t.Self:
        """Encode group of paginations to token.

        This method is useful when we have to paginate over resource
        that is created as a concatenation of several third-party
        endpoints, e.g., list roles and licenses. Since the pagination
        over the result is not equal to pagination over its parts, we
        need to encode the pagination of all parts into one pagination
        over the result.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def paginations(self) -> list[PT]:
        """Decode token to group of paginations.

        This is an inversion of ``from_paginations`` and the following
        should hold true:
        ``list(Token.from_paginations(paginations).paginations())
        == paginations``.
        """
        raise NotImplementedError


def create_next_page_token(
    model: type[PT],
    class_name: str,
    docstring: str | None = None,
) -> type[NextPageTokenInterface[PT]]:
    """Create NextPageToken class for given model.

    See :py:class:``TokenInterface`` for more reference.

    The ``class_name`` is used to set the name for generated class so
    all classes don't have the same name. It is advised to use the
    same name we use for class identifier, i.e.
    ``NextPageToken = create_next_page_token(model, "NextPageToken")``

    Please note that mypy cannot determine the actual type of
    dynamically created class and will not even see it as a valid type.
    For this reason, it is recommended to do the following: ::

        if typing.TYPE_CHECKING:
            class NextPageToken(NextPageTokenInterface): pass
        else:
            NextPageToken = create_next_page_token(model, "NextPageToken)

    This will create the next page token class correctly in runtime
    while the correct type will be available for the type checker.
    """

    class Token(NextPageTokenInterface[PT]):
        """NextPageToken (de)serializer class."""

        @classmethod
        def from_paginations(cls, paginations: list[PT]) -> t.Self:
            paginations_data = [pagination.model_dump() for pagination in paginations]
            return cls(
                token=msgpack.packb(paginations_data).hex(),
            )

        def paginations(self) -> list[PT]:
            return [
                model(**pagination) for pagination in msgpack.unpackb(bytes.fromhex(self.token))
            ]

    Token.__name__ = class_name
    Token.__qualname__ = class_name
    Token.__doc__ = docstring or Token.__doc__
    return Token
