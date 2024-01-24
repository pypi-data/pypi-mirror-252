"""Organisation Router."""


from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..controllers import organisations as controller
from ..controllers.auth import get_current_user
from ..dependencies.database import database
from ..dependencies.owner import Owner
from ..models.organisations import OrganisationModel
from ..schemas.organisations import Organisation, OrganisationCreate, OrganisationUpdate

OWNER_DEPENDENCY = Depends(Owner(OrganisationModel, Organisation))
"""The dependency used to determine if a user owns a resource."""

router = APIRouter(
    prefix="/organisations",
    tags=["Organisations"],
    dependencies=[Depends(get_current_user)],
)


@router.get(
    "/",
    response_model=list[Organisation],
)
def get_organisations(session: Session = Depends(database)):
    """Returns all organisations."""
    return controller.get_organisations(session)


@router.get(
    "/{id}",
    dependencies=[OWNER_DEPENDENCY],
    response_model=Organisation,
)
def get_organisation(id: UUID, session: Session = Depends(database)):
    """Returns the organisation specified by the given ID."""
    return controller.get_organisation(session, id)


@router.post(
    "/",
    response_model=Organisation,
)
def create_organisation(item: OrganisationCreate, session: Session = Depends(database)):
    """Creates a new organisation."""
    return controller.create_organisation(session, item)


@router.put(
    "/{id}",
    dependencies=[OWNER_DEPENDENCY],
    response_model=Organisation,
)
def update_organisation(
    id: UUID, item: OrganisationUpdate, session: Session = Depends(database)
):
    """Updates the organisation specified by the given ID."""
    return controller.update_organisation(session, id, item)


@router.delete(
    "/{id}",
    dependencies=[OWNER_DEPENDENCY],
)
def delete_organisation(id: UUID, session: Session = Depends(database)):
    """Deletes the organisation specified by the given ID."""
    return controller.delete_organisation(session, id)
