"""Lookup to provide a default value."""

# pyright: reportIncompatibleMethodOverride=none
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final, Optional

from ....lookups.handlers.base import LookupHandler

if TYPE_CHECKING:
    from typing_extensions import Literal

    from ....context import CfnginContext


class DefaultLookup(LookupHandler):
    """Lookup to provide a default value."""

    TYPE_NAME: Final[Literal["default"]] = "default"
    """Name that the Lookup is registered as."""

    @classmethod
    def handle(cls, value: str, context: Optional[CfnginContext] = None, **_: Any) -> Any:
        """Use a value from the environment or fall back to a default value.

        Allows defaults to be set at the config file level.

        Args:
            value: Parameter(s) given to this lookup. ``<env_var>::<default value>``
            context: Context instance.

        Example:
            ::

                Groups: ${default app_security_groups::sg-12345,sg-67890}

            If ``app_security_groups`` is defined in the environment, its
            defined value will be returned. Otherwise, ``sg-12345,sg-67890``
            will be the returned value.

        """
        try:
            env_var_name, default_val = value.split("::", 1)
        except ValueError:
            raise ValueError(
                f"Invalid value for default: {value}. Must be in "
                "<env_var>::<default value> format."
            ) from None

        if context and env_var_name in context.parameters:
            return context.parameters[env_var_name]
        return default_val
