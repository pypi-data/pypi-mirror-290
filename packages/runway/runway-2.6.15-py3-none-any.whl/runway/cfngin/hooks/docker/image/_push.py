"""Docker image push hook.

Replicates the functionality of the ``docker image push`` CLI command.

"""

from __future__ import annotations

import logging
from typing import Any, List, Optional  # noqa: UP035

from pydantic import Field, validator

from .....context import CfnginContext
from .....utils import BaseModel
from ..data_models import (
    DockerImage,
    ElasticContainerRegistry,
    ElasticContainerRegistryRepository,
)
from ..hook_data import DockerHookData

LOGGER = logging.getLogger(__name__.replace("._", "."))


class ImagePushArgs(BaseModel):
    """Args passed to image.push."""

    _ctx: Optional[CfnginContext] = Field(default=None, alias="context", export=False)

    ecr_repo: Optional[ElasticContainerRegistryRepository] = None  # depends on _ctx
    """AWS Elastic Container Registry repository information.
    Providing this will automatically construct the repo URI.
    If provided, do not provide ``repo``.

    If using a private registry, only ``repo_name`` is required.
    If using a public registry, ``repo_name`` and ``registry_alias``.

    """

    image: Optional[DockerImage] = None
    """Image to push."""

    repo: Optional[str] = None  # depends on ecr_repo & image
    """URI of a non Docker Hub repository where the image will be stored."""

    tags: List[str] = []  # depends on image  # noqa: UP006
    """List of tags to push."""

    @validator("ecr_repo", pre=True, allow_reuse=True)  # type: ignore
    def _set_ecr_repo(cls, v: Any, values: dict[str, Any]) -> Any:  # noqa: N805
        """Set the value of ``ecr_repo``."""
        if v and isinstance(v, dict):
            return ElasticContainerRegistryRepository.parse_obj(
                {
                    "repo_name": v.get("repo_name"),
                    "registry": ElasticContainerRegistry.parse_obj(
                        {
                            "account_id": v.get("account_id"),
                            "alias": v.get("registry_alias"),
                            "aws_region": v.get("aws_region"),
                            "context": values.get("context"),
                        }
                    ),
                }
            )
        return v

    @validator("repo", pre=True, always=True, allow_reuse=True)  # type: ignore
    def _set_repo(cls, v: str | None, values: dict[str, Any]) -> str | None:  # noqa: N805
        """Set the value of ``repo``."""
        if v:
            return v

        image: DockerImage | None = values.get("image")
        if image:
            return image.repo

        ecr_repo: ElasticContainerRegistryRepository | None = values.get("ecr_repo")
        if ecr_repo:
            return ecr_repo.fqn

        return None

    @validator("tags", pre=True, always=True, allow_reuse=True)  # type: ignore
    def _set_tags(cls, v: list[str], values: dict[str, Any]) -> list[str]:  # noqa: N805
        """Set the value of ``tags``."""
        if v:
            return v

        image: DockerImage | None = values.get("image")
        if image:
            return image.tags

        return ["latest"]


def push(*, context: CfnginContext, **kwargs: Any) -> DockerHookData:
    """Docker image push hook.

    Replicates the functionality of ``docker image push`` CLI command.

    kwargs are parsed by :class:`~runway.cfngin.hooks.docker.image.ImagePushArgs`.

    """
    args = ImagePushArgs.parse_obj({"context": context, **kwargs})
    docker_hook_data = DockerHookData.from_cfngin_context(context)
    LOGGER.info("pushing image %s...", args.repo)
    for tag in args.tags:
        docker_hook_data.client.images.push(repository=args.repo, tag=tag)
        LOGGER.info("successfully pushed image %s:%s", args.repo, tag)
    return docker_hook_data.update_context(context)
