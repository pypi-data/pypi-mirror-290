"""AWS SSM Parameter Store hooks."""

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Any, List, Optional, cast  # noqa: UP035

from pydantic import Extra, validator
from typing_extensions import Literal, TypedDict

from ....compat import cached_property
from ....utils import BaseModel, JsonEncoder
from ..protocols import CfnginHookProtocol
from ..utils import TagDataModel

if TYPE_CHECKING:
    from mypy_boto3_ssm.client import SSMClient
    from mypy_boto3_ssm.literals import ParameterTierType
    from mypy_boto3_ssm.type_defs import ParameterTypeDef, TagTypeDef

    from ...._logging import RunwayLogger
    from ....context import CfnginContext
else:
    ParameterTierType = Literal["Advanced", "Intelligent-Tiering", "Standard"]

LOGGER = cast("RunwayLogger", logging.getLogger(__name__))


# PutParameterResultTypeDef but without metadata
class _PutParameterResultTypeDef(TypedDict):
    Tier: ParameterTierType
    Version: int


class ArgsDataModel(BaseModel):
    """Parameter hook args.

    Attributes:
        allowed_pattern: A regular expression used to validate the parameter value.
        data_type: The data type for a String parameter. Supported data types
            include plain text and Amazon Machine Image IDs.
        description: Information about the parameter.
        force: Skip checking the current value of the parameter, just put it.
            Can be used alongside ``overwrite`` to always update a parameter.
        key_id: The KMS Key ID that you want to use to encrypt a parameter.
            Either the default AWS Key Management Service (AWS KMS) key automatically
            assigned to your AWS account or a custom key.
            Required for parameters that use the ``SecureString`` data type.
        name: The fully qualified name of the parameter that you want to add to
            the system.
        overwrite: Allow overwriting an existing parameter.
        policies: One or more policies to apply to a parameter.
            This field takes a JSON array.
        tags: Optional metadata that you assign to a resource.
        tier: The parameter tier to assign to a parameter.
        type: The type of parameter.
        value: The parameter value that you want to add to the system.
            Standard parameters have a value limit of 4 KB.
            Advanced parameters have a value limit of 8 KB.

    """

    allowed_pattern: Optional[str] = None
    data_type: Optional[Literal["aws:ec2:image", "text"]] = None
    description: Optional[str] = None
    force: bool = False
    key_id: Optional[str] = None
    name: str
    overwrite: bool = True
    policies: Optional[str] = None
    tags: Optional[List[TagDataModel]] = None  # noqa: UP006
    tier: ParameterTierType = "Standard"
    type: Literal["String", "StringList", "SecureString"]
    value: Optional[str] = None

    class Config:
        """Model configuration."""

        allow_population_by_field_name = True
        extra = Extra.ignore
        fields = {
            "allowed_pattern": {"alias": "AllowedPattern"},
            "data_type": {"alias": "DataType"},
            "description": {"alias": "Description"},
            "key_id": {"alias": "KeyId"},
            "name": {"alias": "Name"},
            "overwrite": {"alias": "Overwrite"},
            "policies": {"alias": "Policies"},
            "tags": {"alias": "Tags"},
            "tier": {"alias": "Tier"},
            "type": {"alias": "Type"},
            "value": {"alias": "Value"},
        }

    @validator("policies", allow_reuse=True, pre=True)  # type: ignore
    def _convert_policies(cls, v: list[dict[str, Any]] | str | Any) -> str:  # noqa: N805
        """Convert policies to acceptable value."""
        if isinstance(v, str):
            return v
        if isinstance(v, list):
            return json.dumps(v, cls=JsonEncoder)
        raise TypeError(f"unexpected type {type(v)}; permitted: list[dict[str, Any]] | str | None")

    @validator("tags", allow_reuse=True, pre=True)  # type: ignore
    def _convert_tags(
        cls, v: dict[str, str] | list[dict[str, str]] | Any  # noqa: N805
    ) -> list[dict[str, str]]:
        """Convert tags to acceptable value."""
        if isinstance(v, list):
            return v
        if isinstance(v, dict):
            return [{"Key": k, "Value": v} for k, v in v.items()]
        raise TypeError(
            f"unexpected type {type(v)}; permitted: dict[str, str] | list[dict[str, str] | None"
        )


class _Parameter(CfnginHookProtocol):
    """AWS SSM Parameter Store Parameter."""

    args: ArgsDataModel

    def __init__(
        self,
        context: CfnginContext,
        *,
        name: str,
        type: Literal["String", "StringList", "SecureString"],  # noqa: A002
        **kwargs: Any,
    ) -> None:
        """Instantiate class.

        Args:
            context: CFNgin context object.
            name: The fully qualified name of the parameter that you want to add to
                the system.
            type: The type of parameter.
            **kwargs: Arbitrary keyword arguments.

        """
        self.args = ArgsDataModel.parse_obj({"name": name, "type": type, **kwargs})
        self.ctx = context

    @cached_property
    def client(self) -> SSMClient:
        """AWS SSM client."""
        return self.ctx.get_session().client("ssm")

    def delete(self) -> bool:
        """Delete parameter."""
        try:
            self.client.delete_parameter(Name=self.args.name)
            LOGGER.info("deleted SSM Parameter %s", self.args.name)
        except self.client.exceptions.ParameterNotFound:
            LOGGER.info("delete parameter skipped; %s not found", self.args.name)
        return True

    def get(self) -> ParameterTypeDef:
        """Get parameter."""
        if self.args.force:  # bypass getting current value
            return {}
        try:
            return self.client.get_parameter(Name=self.args.name, WithDecryption=True).get(
                "Parameter", {}
            )
        except self.client.exceptions.ParameterNotFound:
            LOGGER.verbose("parameter %s does not exist", self.args.name)
            return {}

    def get_current_tags(self) -> list[TagTypeDef]:
        """Get Tags currently applied to Parameter."""
        try:
            return self.client.list_tags_for_resource(
                ResourceId=self.args.name, ResourceType="Parameter"
            ).get("TagList", [])
        except (
            self.client.exceptions.InvalidResourceId,
            self.client.exceptions.ParameterNotFound,
        ):
            return []

    def post_deploy(self) -> _PutParameterResultTypeDef:
        """Run during the *post_deploy* stage."""
        result = self.put()
        self.update_tags()
        return result

    def post_destroy(self) -> bool:
        """Run during the *post_destroy* stage."""
        return self.delete()

    def pre_deploy(self) -> _PutParameterResultTypeDef:
        """Run during the *pre_deploy* stage."""
        result = self.put()
        self.update_tags()
        return result

    def pre_destroy(self) -> bool:
        """Run during the *pre_destroy* stage."""
        return self.delete()

    def put(self) -> _PutParameterResultTypeDef:
        """Put parameter."""
        if not self.args.value:
            LOGGER.info(
                "skipped putting SSM Parameter; value provided for %s is falsy",
                self.args.name,
            )
            return {"Tier": self.args.tier, "Version": 0}
        current_param = self.get()
        if current_param.get("Value") != self.args.value:
            try:
                result = self.client.put_parameter(
                    **self.args.dict(by_alias=True, exclude_none=True, exclude={"force", "tags"})
                )
            except self.client.exceptions.ParameterAlreadyExists:
                LOGGER.warning(
                    "parameter %s already exists; to overwrite it's value, "
                    'set the overwrite field to "true"',
                    self.args.name,
                )
                return {
                    "Tier": current_param.get("Tier", self.args.tier),
                    "Version": current_param.get("Version", 0),
                }
        else:
            result: _PutParameterResultTypeDef = {
                "Tier": current_param.get("Tier", self.args.tier),
                "Version": current_param.get("Version", 0),
            }
        LOGGER.info("put SSM Parameter %s", self.args.name)
        return result

    def update_tags(self) -> None:
        """Update tags."""
        current_tags = self.get_current_tags()
        if self.args.tags and current_tags:
            diff_tag_keys = list({i["Key"] for i in current_tags} ^ {i.key for i in self.args.tags})
        elif self.args.tags:
            diff_tag_keys = []
        else:
            diff_tag_keys = [i["Key"] for i in current_tags]

        try:
            if diff_tag_keys:
                diff_tag_keys.sort()
                self.client.remove_tags_from_resource(
                    ResourceId=self.args.name,
                    ResourceType="Parameter",
                    TagKeys=diff_tag_keys,
                )
                LOGGER.debug("removed tags for parameter %s: %s", self.args.name, diff_tag_keys)

            if self.args.tags:
                tags_to_add = [
                    cast("TagTypeDef", tag.dict(by_alias=True)) for tag in self.args.tags
                ]
                self.client.add_tags_to_resource(
                    ResourceId=self.args.name,
                    ResourceType="Parameter",
                    Tags=tags_to_add,
                )
                LOGGER.debug(
                    "added tags to parameter %s: %s",
                    self.args.name,
                    [tag["Key"] for tag in tags_to_add],
                )
        except self.client.exceptions.InvalidResourceId:
            LOGGER.info("skipped updating tags; parameter %s does not exist", self.args.name)
        else:
            LOGGER.info("updated tags for parameter %s", self.args.name)


class SecureString(_Parameter):
    """AWS SSM Parameter Store SecureString Parameter."""

    def __init__(
        self,
        context: CfnginContext,
        *,
        name: str,
        **kwargs: Any,
    ) -> None:
        """Instantiate class.

        Args:
            context: CFNgin context object.
            name: The fully qualified name of the parameter that you want to add to
                the system.
            **kwargs: Arbitrary keyword arguments.

        """
        for k in ["Type", "type"]:  # ensure neither of these are set
            kwargs.pop(k, None)
        super().__init__(context, name=name, type="SecureString", **kwargs)
