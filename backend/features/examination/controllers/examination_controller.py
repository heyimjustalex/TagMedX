from fastapi import APIRouter, Depends, HTTPException
from ...authorization.services.token_service import UserData, TokenService
from features.bbox.services.bbox_service import BBoxService
from connectionDB.session import get_db
from sqlalchemy.orm import Session
from ..services.examination_service import ExaminationService
from ..schemas.examination_schema import ExaminationCreate, BBoxCreate

router = APIRouter()


@router.put(
    "/api/examinations", tags=["Examinations"], response_model=ExaminationCreate
)
async def create_or_update_examinations(
    examination_data: ExaminationCreate,
    user_data: UserData = Depends(TokenService.get_user_data),
    db: Session = Depends(get_db),
):
    bbox_service = BBoxService(db)
    examination_service = ExaminationService(db)
    created_examinations = []

    existing_examination = examination_service.get_examination_by_sample(
        examination_data.id_sample,
    )

    if existing_examination:
        existing_examination.tentative = examination_data.tentative

        bbox_service.delete_bboxes_by_examination(existing_examination.id)

    else:
        existing_examination = examination_service.create_examination(
            user_data.id,
            examination_data.id_sample,
            examination_data.tentative,
        )

    bbox_list = []
    if examination_data.BBox is not None:
        for bbox_data in examination_data.BBox:
            bbox = bbox_service.create_bbox(
                existing_examination.id,
                bbox_data.id_label,
                bbox_data.comment,
                bbox_data.x,
                bbox_data.y,
                bbox_data.width,
                bbox_data.height,
            )
            bbox_instance = BBoxCreate(
                id_label=bbox.id_label,
                comment=bbox.comment,
                x=bbox.x,
                y=bbox.y,
                width=bbox.width,
                height=bbox.height,
            )
            bbox_list.append(bbox_instance)

    created_examinations.append(
        ExaminationCreate(
            id_sample=existing_examination.id_sample,
            tentative=existing_examination.tentative,
            BBox=bbox_list,
        )
    )

    return created_examinations[0]


@router.delete("/api/examinations/{examination_id}", tags=["Examinations"])
async def delete_examination_and_bboxes(
    examination_id: int, db: Session = Depends(get_db)
):
    examination_service = ExaminationService(db)
    bbox_service = BBoxService(db)

    _ = examination_service.get_examination_by_id(examination_id)

    bbox_service.delete_bboxes_by_examination(examination_id)
    examination_service.delete_examination(examination_id)

    return {"message": "Examination and associated BBoxes deleted successfully"}
