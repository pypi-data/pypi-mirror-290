"""Runway static site Module options."""

# ruff: noqa: UP006, UP035
from __future__ import annotations

from pathlib import Path
from typing import Any, List, Optional, cast

from pydantic import Extra, root_validator

from ....config.models.base import ConfigProperty


class RunwayStaticSiteExtraFileDataModel(ConfigProperty):
    """Model for Runway static site Module extra_files option item.

    Attributes:
        content_type: An explicit content type for the file. If not provided,
            will attempt to determine based on the name provided.
        content: Inline content that will be used as the file content.
            This or ``file`` must be provided.
        file: Path to an existing file. The content of this file will be uploaded
            to the static site S3 bucket using the name as the object key.
            This or ``content`` must be provided.
        name: The destination name of the file to create.

    """

    content_type: Optional[str] = None
    content: Any = None
    file: Optional[Path] = None
    name: str

    class Config(ConfigProperty.Config):
        """Model configuration."""

        extra = Extra.forbid
        title = "Runway static site Module extra_files option item."

    @root_validator  # type: ignore
    def _autofill_content_type(cls, values: dict[str, Any]) -> dict[str, Any]:  # noqa: N805
        """Attempt to fill content_type if not provided."""
        if values.get("content_type"):
            return values
        name = cast(str, values.get("name", ""))
        if name.endswith(".json"):
            values["content_type"] = "application/json"
        elif name.endswith((".yaml", ".yml")):
            values["content_type"] = "text/yaml"
        return values

    @root_validator(pre=True)  # type: ignore
    def _validate_content_or_file(cls, values: dict[str, Any]) -> dict[str, Any]:  # noqa: N805
        """Validate that content or file is provided."""
        if all(i in values and values[i] for i in ["content", "file"]):
            raise ValueError("only one of content or file can be provided")
        if not any(i in values for i in ["content", "file"]):
            raise ValueError("one of content or file must be provided")
        return values


class RunwayStaticSitePreBuildStepDataModel(ConfigProperty):
    """Model for Runway static site Module pre_build_steps option item.

    Attributes:
        command: The command to run.
        cwd: The working directory for the subprocess running the command.
            If not provided, the current working directory is used.

    """

    command: str
    cwd: Path = Path.cwd()

    class Config(ConfigProperty.Config):
        """Model configuration."""

        extra = Extra.forbid
        title = "Runway static site Module pre_build_steps option item."


class RunwayStaticSiteSourceHashingDirectoryDataModel(ConfigProperty):
    """Model for Runway static site Module source_hashing.directory option item.

    Attributes:
        exclusions: List of gitignore formatted globs to ignore when calculating
            the hash.
        path: Path to files to include in the hash.

    """

    exclusions: List[str] = []
    path: Path

    class Config(ConfigProperty.Config):
        """Model configuration."""

        extra = Extra.forbid
        title = "Runway static site Module source_hashing.directories option item."


class RunwayStaticSiteSourceHashingDataModel(ConfigProperty):
    """Model for Runway static site Module source_hashing option.

    Attributes:
        directories: Explicitly provide the directories to use when calculating
            the hash. If not provided, will default to the root of the module.
        enabled: Enable source hashing. If not enabled, build and upload will
            occur on every deploy.
        parameter: SSM parameter where the hash of each build is stored.

    """

    directories: List[RunwayStaticSiteSourceHashingDirectoryDataModel] = [
        RunwayStaticSiteSourceHashingDirectoryDataModel(path="./")  # type: ignore
    ]
    enabled: bool = True
    parameter: Optional[str] = None

    class Config(ConfigProperty.Config):
        """Model configuration."""

        extra = Extra.forbid
        title = "Runway static site Module source_hashing option."


class RunwayStaticSiteModuleOptionsDataModel(ConfigProperty):
    """Model for Runway static site Module options.

    Attributes:
        build_output: Directory where build output is placed. Defaults to current
            working directory.
        build_steps: List of commands to run to build the static site.
        extra_files: List of files that should be uploaded to S3 after the build.
            Used to dynamically create or select file.
        pre_build_steps: Commands to be run prior to the build process.
        source_hashing: Overrides for source hash calculation and tracking.

    """

    build_output: str = "./"
    build_steps: List[str] = []
    extra_files: List[RunwayStaticSiteExtraFileDataModel] = []
    pre_build_steps: List[RunwayStaticSitePreBuildStepDataModel] = []
    source_hashing: RunwayStaticSiteSourceHashingDataModel = (
        RunwayStaticSiteSourceHashingDataModel()
    )

    class Config(ConfigProperty.Config):
        """Model configuration."""

        extra = Extra.ignore
        title = "Runway static site Module options."
