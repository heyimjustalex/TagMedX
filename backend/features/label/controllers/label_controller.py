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
)
from fastapi.responses import StreamingResponse
import json

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
        label_create.id_set,
        label_create.name,
        label_create.description,
        label_create.color,
    )

    return LabelResponse(
        id=label.id,
        id_set=label.id_set,
        name=label.name,
        description=label.description,
        color=label.color,
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
        id=label.id,
        id_set=label.id_set,
        name=label.name,
        description=label.description,
        color=label.color,
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
                color=label.color,
            )
        )

    return response


@router.get(
    "/api/labels/group/{id_group}", tags=["Labels"], response_model=list[LabelResponse]
)
def get_labels_in_group(
    id_group: int,
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    db: Annotated[Session, Depends(get_db)],
):
    group_service = GroupService(db)
    _ = group_service.get_membership(id_group, user_data.id)

    label_service = LabelService(db)
    labels = label_service.get_labels_in_group(id_group)

    response: list[LabelResponse] = []
    for label in labels:
        response.append(
            LabelResponse(
                id=label.id,
                id_set=label.id_set,
                name=label.name,
                description=label.description,
                color=label.color,
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
        label.id, label_update.name, label_update.description, label_update.color
    )

    return LabelResponse(
        id=label.id,
        id_set=label.id_set,
        name=label.name,
        description=label.description,
        color=label.color,
    )


@router.delete("/api/labels/{id_label}", tags=["Labels"])
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

    return {"message": "Label removed successfully"}


@router.post("/api/export/package/coco/{package_id}", tags=["Export"])
def export_annotations_from_package_to_coco(
    package_id: int, db: Session = Depends(get_db)
):
    label_service = LabelService(db)
    coco_data = label_service.export_annotations_from_package_to_coco(package_id)

    def generate():
        yield json.dumps(coco_data, indent=2).encode()

    return StreamingResponse(
        generate(),
        media_type="application/json",
        headers={
            "Content-Disposition": f"attachment;filename=package_{package_id}_coco.json"
        },
    )


@router.post("/api/export/set/coco/{set_id}", tags=["Export"])
def export_annotations_from_set_to_coco(set_id: int, db: Session = Depends(get_db)):
    label_service = LabelService(db)
    coco_data = label_service.export_annotations_from_set_to_coco(set_id)

    def generate():
        yield json.dumps(coco_data, indent=2).encode()

    return StreamingResponse(
        generate(),
        media_type="application/json",
        headers={"Content-Disposition": f"attachment;filename=set_{set_id}_coco.json"},
    )
