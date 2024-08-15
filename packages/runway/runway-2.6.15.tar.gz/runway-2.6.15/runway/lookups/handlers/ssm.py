"""Retrieve a value from SSM Parameter Store."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Final, Union

from ...lookups.handlers.base import LookupHandler

if TYPE_CHECKING:
    from typing_extensions import Literal

    from ...context import CfnginContext, RunwayContext

LOGGER = logging.getLogger(__name__)


class SsmLookup(LookupHandler):
    """SSM Parameter Store Lookup."""

    TYPE_NAME: Final[Literal["ssm"]] = "ssm"
    """Name that the Lookup is registered as."""

    @classmethod
    def handle(
        cls,
        value: str,
        context: Union[CfnginContext, RunwayContext],
        *__args: Any,
        **__kwargs: Any,
    ) -> Any:
        """Retrieve a value from SSM Parameter Store.

        Args:
            value: The value passed to the Lookup.
            context: The current context object.

        Raises:
            ParameterNotFound: Parameter not found in SSM and a default value
                was not provided.

        """
        query, args = cls.parse(value)

        session = context.get_session(region=args.get("region"))
        client = session.client("ssm")

        try:
            response = client.get_parameter(Name=query, WithDecryption=True)["Parameter"]
            return cls.format_results(
                (
                    response["Value"].split(",")
                    if response["Type"] == "StringList"
                    else response["Value"]
                ),
                **args,
            )
        except client.exceptions.ParameterNotFound:
            if args.get("default"):
                args.pop("load", None)  # don't load a default value
                return cls.format_results(args.pop("default"), **args)
            raise
