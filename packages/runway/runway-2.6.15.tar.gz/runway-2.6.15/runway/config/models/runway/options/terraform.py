"""Runway Terraform Module options."""

# ruff: noqa: UP006, UP035
from __future__ import annotations

from typing import List, Optional, Union

from pydantic import Extra, Field, validator

from ...base import ConfigProperty


class RunwayTerraformArgsDataModel(ConfigProperty):
    """Model for Runway Terraform Module args option."""

    apply: List[str] = []
    init: List[str] = []
    plan: List[str] = []

    class Config(ConfigProperty.Config):
        """Model configuration."""

        extra = Extra.forbid
        title = "Runway Terraform Module args option"


class RunwayTerraformBackendConfigDataModel(ConfigProperty):
    """Model for Runway Terraform Module terraform_backend_config option."""

    bucket: Optional[str] = None
    dynamodb_table: Optional[str] = None
    region: Optional[str] = None
    workspace_key_prefix: Optional[str] = None

    class Config(ConfigProperty.Config):
        """Model configuration."""

        extra = Extra.forbid
        title = "Runway Terraform Module terraform_backend_config option"

    def __bool__(self) -> bool:
        """Evaluate the boolean value of the object instance."""
        data = self.dict(exclude_none=True)
        return "bucket" in data or "dynamodb_table" in data


class RunwayTerraformModuleOptionsDataModel(ConfigProperty):
    """Model for Runway Terraform Module options."""

    args: RunwayTerraformArgsDataModel = RunwayTerraformArgsDataModel()
    backend_config: RunwayTerraformBackendConfigDataModel = Field(
        default=RunwayTerraformBackendConfigDataModel(),
        alias="terraform_backend_config",
    )
    version: Optional[str] = Field(default=None, alias="terraform_version")
    workspace: Optional[str] = Field(default=None, alias="terraform_workspace")
    write_auto_tfvars: bool = Field(default=False, alias="terraform_write_auto_tfvars")

    class Config(ConfigProperty.Config):
        """Model configuration."""

        extra = Extra.ignore
        title = "Runway Terraform Module options"

    @validator("args", pre=True)  # type: ignore
    def _convert_args(
        cls, v: Union[list[str], dict[str, list[str]]]  # noqa: N805
    ) -> dict[str, list[str]]:
        """Convert args from list to dict."""
        if isinstance(v, list):
            return {"apply": v}
        return v
