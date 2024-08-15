"""Runway config test definition."""

# ruff: noqa: UP006, UP035
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Generic, Tuple, TypeVar, Union

from ....variables import Variable
from ...models.runway import (
    CfnLintRunwayTestArgs,
    CfnLintRunwayTestDefinitionModel,
    RunwayTestDefinitionModel,
    ScriptRunwayTestArgs,
    ScriptRunwayTestDefinitionModel,
    ValidRunwayTestTypeValues,
    YamlLintRunwayTestDefinitionModel,
)
from .base import ConfigComponentDefinition

if TYPE_CHECKING:
    from typing_extensions import Literal

    from ...models.base import ConfigProperty


_DataModel = TypeVar(
    "_DataModel",
    CfnLintRunwayTestDefinitionModel,
    RunwayTestDefinitionModel,
    ScriptRunwayTestDefinitionModel,
    YamlLintRunwayTestDefinitionModel,
)


class RunwayTestDefinition(Generic[_DataModel], ConfigComponentDefinition):
    """Runway test definition."""

    args: Union[Dict[str, Any], ConfigProperty]
    name: str
    required: bool
    type: ValidRunwayTestTypeValues

    _data: RunwayTestDefinitionModel
    _supports_vars: Tuple[str, ...] = ("args", "required")

    def __init__(self, data: _DataModel) -> None:
        """Instantiate class."""
        super().__init__(data)

    def __new__(
        cls,
        data: _DataModel,
    ) -> RunwayTestDefinition[_DataModel]:
        """Create a new instance of a class.

        Returns:
            Correct subclass of RunwayTestDefinition for the given data.

        """
        if cls is not RunwayTestDefinition:
            return super().__new__(cls)
        if isinstance(data, CfnLintRunwayTestDefinitionModel):
            return super().__new__(CfnLintRunwayTestDefinition)  # type: ignore
        if isinstance(data, ScriptRunwayTestDefinitionModel):
            return super().__new__(ScriptRunwayTestDefinition)  # type: ignore
        if isinstance(data, YamlLintRunwayTestDefinitionModel):
            return super().__new__(YamlLintRunwayTestDefinition)  # type: ignore
        raise TypeError(
            "expected data of type CfnLintRunwayTestDefinitionModel, "
            "ScriptRunwayTestDefinitionModel, or YamlLintRunwayTestDefinitionModel; "
            f"got {type(data)}"
        )

    def _register_variable(self, var_name: str, var_value: Any) -> None:
        """Register a variable.

        Args:
            var_name: Name of the config field that can contain a variable
                lookup.
            var_value: Literal value supplied in the config to be resolved
                as a variable if it contains a lookup.

        """
        self._vars[var_name] = Variable(
            name=f"{self.name}.{var_name}", value=var_value, variable_type="runway"
        )

    @classmethod
    def parse_obj(cls, obj: Any) -> RunwayTestDefinition[_DataModel]:
        """Parse a python object into this class.

        Args:
            obj: The object to parse.

        """
        return cls(RunwayTestDefinitionModel.parse_obj(obj))


class CfnLintRunwayTestDefinition(RunwayTestDefinition[CfnLintRunwayTestDefinitionModel]):
    """Runway cfn-lint test definition."""

    args: CfnLintRunwayTestArgs
    type: Literal["cfn-lint"] = "cfn-lint"

    def __init__(self, data: CfnLintRunwayTestDefinitionModel) -> None:
        """Instantiate class."""
        super().__init__(data)

    @classmethod
    def parse_obj(cls, obj: Any) -> CfnLintRunwayTestDefinition:
        """Parse a python object into this class.

        Args:
            obj: The object to parse.

        """
        return cls(CfnLintRunwayTestDefinitionModel.parse_obj(obj))


class ScriptRunwayTestDefinition(RunwayTestDefinition[ScriptRunwayTestDefinitionModel]):
    """Runway script test definition."""

    args: ScriptRunwayTestArgs
    type: Literal["script"] = "script"

    def __init__(self, data: ScriptRunwayTestDefinitionModel) -> None:
        """Instantiate class."""
        super().__init__(data)

    @classmethod
    def parse_obj(cls, obj: Any) -> ScriptRunwayTestDefinition:
        """Parse a python object into this class.

        Args:
            obj: The object to parse.

        """
        return cls(ScriptRunwayTestDefinitionModel.parse_obj(obj))


class YamlLintRunwayTestDefinition(RunwayTestDefinition[YamlLintRunwayTestDefinitionModel]):
    """Runway yamllint test definition."""

    type: Literal["yamllint"] = "yamllint"

    def __init__(self, data: YamlLintRunwayTestDefinitionModel) -> None:
        """Instantiate class."""
        super().__init__(data)

    @classmethod
    def parse_obj(cls, obj: Any) -> YamlLintRunwayTestDefinition:
        """Parse a python object into this class.

        Args:
            obj: The object to parse.

        """
        return cls(YamlLintRunwayTestDefinitionModel.parse_obj(obj))
