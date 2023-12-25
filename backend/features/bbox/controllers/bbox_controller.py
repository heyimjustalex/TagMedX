from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from connectionDB.session import get_db
from ..schemas.bbox_schema import BBoxCreate, BBoxResponse, BBoxUpdate
from features.authorization.services.token_service import TokenService, UserData
from ..services.bbox_service import BBoxService

router = APIRouter()


@router.post("/api/bbox", tags=["BBox"], response_model=BBoxResponse)
def create_bbox(
    bbox_create: BBoxCreate,
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    db: Annotated[Session, Depends(get_db)],
):
    bbox_service = BBoxService(db)

    # _ = bbox_service.check_user_is_assigned_to_package(user_data.id)

    bbox = bbox_service.create_bbox(
        bbox_create.id_examination,
        bbox_create.id_label,
        bbox_create.comment,
        bbox_create.x,
        bbox_create.y,
        bbox_create.width,
        bbox_create.height,
    )

    return BBoxResponse(
        id=bbox.id,
        id_examination=bbox.id_examination,
        id_label=bbox.id_label,
        comment=bbox.comment,
        x=bbox.x,
        y=bbox.y,
        width=bbox.width,
        height=bbox.height,
    )


@router.get("/api/get_bbox/{id_bbox}", tags=["BBox"], response_model=BBoxResponse)
def get_bbox(
    id_bbox: int,
    db: Annotated[Session, Depends(get_db)],
):
    bbox_service = BBoxService(db)
    bbox = bbox_service.get_bbox(id_bbox)

    return BBoxResponse(
        id=bbox.id,
        id_examination=bbox.id_examination,
        id_label=bbox.id_label,
        comment=bbox.comment,
        x=bbox.x,
        y=bbox.y,
        width=bbox.width,
        height=bbox.height,
    )


@router.get(
    "/api/get_bbox/by_examination/{id_bbox}",
    tags=["BBox"],
    response_model=list[BBoxResponse],
)
def get_bbox_by_examination(
    id_examination: int,
    db: Annotated[Session, Depends(get_db)],
):
    bbox_service = BBoxService(db)
    bbox_by_examination = bbox_service.get_examination_bboxes(id_examination)
    response: list[BBoxResponse] = []
    for bbox in bbox_by_examination:
        response.append(
            BBoxResponse(
                id=bbox.id,
                id_examination=bbox.id_examination,
                id_label=bbox.id_label,
                comment=bbox.comment,
                x=bbox.x,
                y=bbox.y,
                width=bbox.width,
                height=bbox.height,
            )
        )
    return response


@router.put("/api/bbox/{id_bbox}", tags=["BBox"], response_model=BBoxResponse)
async def update_bbox(
    id_bbox: int,
    bbox_update: BBoxUpdate,
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    db: Annotated[Session, Depends(get_db)],
):
    bbox_service = BBoxService(db)
    bbox = bbox_service.get_bbox(id_bbox)

    # _ = bbox_service.check_user_is_assigned_to_package(user_data.id)

    bbox = bbox_service.update_bbox(
        bbox,
        bbox_update.comment,
        bbox_update.x,
        bbox_update.y,
        bbox_update.width,
        bbox_update.height,
    )

    return BBoxResponse(
        id=bbox.id,
        id_examination=bbox.id_examination,
        id_label=bbox.id_label,
        comment=bbox.comment,
        x=bbox.x,
        y=bbox.y,
        width=bbox.width,
        height=bbox.height,
    )


@router.delete("/api/bbox/{id_bbox}", tags=["BBox"])
async def delete_bbox(
    id_bbox: int,
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    db: Annotated[Session, Depends(get_db)],
):
    bbox_service = BBoxService(db)
    # _ = bbox_service.check_user_is_assigned_to_package(user_data.id)
    bbox = bbox_service.get_bbox(id_bbox)
    bbox_service.delete_bbox(bbox)

    return {"message:" "BBox removed successfully"}
