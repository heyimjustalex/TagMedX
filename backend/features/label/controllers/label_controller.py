from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from connectionDB.session import get_db
from ..services.label_service import LabelService
from ...sets.services.set_service import SetService
from ...groups.services.group_service import GroupService
from features.authorization.services.token_service import TokenService, UserData
from ..schemas.label_schema import (
    LabelCreate,
    LabelResponse,
    LabelUpdate,
    LabelDeleteResposne,
)

router = APIRouter()


@router.post("/api/labels", tags=["Labels"], response_model=LabelResponse)
def create_label(
    label_create: LabelCreate,
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    db: Annotated[Session, Depends(get_db)],
):
    set_service = SetService(db)
    set = set_service.get_set(label_create.id_set)

    group_service = GroupService(db)
    _ = group_service.check_if_admin(user_data.id, set.id_group)

    label_service = LabelService(db)
    label = label_service.create_label(
        label_create.id_set, label_create.name, label_create.description
    )

    return LabelResponse(
        id=label.id, id_set=label.id_set, name=label.name, description=label.description
    )


@router.get("/api/labels/{id_label}", tags=["Labels"], response_model=LabelResponse)
def get_label(
    id_label: int,
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    db: Annotated[Session, Depends(get_db)],
):
    label_service = LabelService(db)
    label = label_service.get_label(id_label)

    group_service = GroupService(db)
    _ = group_service.get_membership(label.Set.id_group, user_data.id)

    return LabelResponse(
        id=label.id, id_set=label.id_set, name=label.name, description=label.description
    )


@router.get(
    "/api/labels/set/{id_set}", tags=["Labels"], response_model=list[LabelResponse]
)
def get_labels_for_set(
    id_set: int,
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    db: Annotated[Session, Depends(get_db)],
):
    set_service = SetService(db)
    set = set_service.get_set(id_set)

    group_service = GroupService(db)
    _ = group_service.get_membership(set.id_group, user_data.id)

    label_service = LabelService(db)
    labels = label_service.get_labels_for_set(set.id)

    response: list[LabelResponse] = []
    for label in labels:
        response.append(
            LabelResponse(
                id=label.id,
                id_set=label.id_set,
                name=label.name,
                description=label.description,
            )
        )

    return response


@router.put("/api/labels/{id_label}", tags=["Labels"], response_model=LabelResponse)
def update_label(
    id_label: int,
    label_update: LabelUpdate,
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    db: Annotated[Session, Depends(get_db)],
):
    label_service = LabelService(db)
    label = label_service.get_label(id_label)

    group_service = GroupService(db)
    _ = group_service.check_if_admin(user_data.id, label.Set.id_group)

    label = label_service.update_label(
        label.id, label_update.name, label_update.description
    )

    return LabelResponse(
        id=label.id, id_set=label.id_set, name=label.name, description=label.description
    )


@router.delete(
    "/api/labels/{id_label}", tags=["Labels"], response_model=LabelDeleteResposne
)
def delete_label(
    id_label: int,
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    db: Annotated[Session, Depends(get_db)],
):
    label_service = LabelService(db)
    label = label_service.get_label(id_label)

    group_service = GroupService(db)
    _ = group_service.check_if_admin(user_data.id, label.Set.id_group)

    label_service.delete_label(id_label)

    return LabelDeleteResposne(message="Label removed successfully")
