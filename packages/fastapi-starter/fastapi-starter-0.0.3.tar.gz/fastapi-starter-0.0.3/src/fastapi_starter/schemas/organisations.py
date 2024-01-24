"""Organisations Schemas."""


from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from . import HasOwner, InDatabase, Updatable


class PermissionType(str, Enum):
    """Permission types for organisations."""

    ADMIN = "ADMIN"
    WRITE = "WRITE"
    READ = "READ"


class OrganisationBase(BaseModel):
    """Base schema for organisations."""

    name: str
    """The name of the organisation."""
    permission: PermissionType
    """The permissions granted to the organisation."""


class OrganisationCreate(OrganisationBase):
    """Creation schema for organisations."""


class Organisation(HasOwner, InDatabase, Updatable, OrganisationBase):
    """Return schema for organisations."""

    def get_owner(self):
        return self.id

    model_config = ConfigDict(from_attributes=True)


class OrganisationUpdate(BaseModel):
    """Modification schema for organisations."""

    name: Optional[str] = Field(default=None)
    """The name of the organisation."""
    permission: Optional[PermissionType] = Field(default=None)
    """The permissions granted to the organisation."""
