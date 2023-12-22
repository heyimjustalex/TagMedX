from fastapi import APIRouter, Depends, HTTPException
from ...authorization.services.token_service import UserData, TokenService
from features.bbox.services.bbox_service import BBoxService
from features.samples.services.sample_service import SampleService
from features.packages.services.package_service import PackageService
from features.sets.services.set_service import SetService
from connectionDB.session import get_db
from sqlalchemy.orm import Session
from ..services.examination_service import ExaminationService
from ..schemas.examination_schema import (
    ExaminationCreate,
    BBoxCreate,
    ExaminationCreateResponse,
)

router = APIRouter()


@router.put(
    "/api/examinations", tags=["Examinations"], response_model=ExaminationCreateResponse
)
async def create_or_update_examinations(
    examination_data: ExaminationCreate,
    user_data: UserData = Depends(TokenService.get_user_data),
    db: Session = Depends(get_db),
):
    bbox_service = BBoxService(db)
    examination_service = ExaminationService(db)
    sample_service = SampleService(db)
    package_service = PackageService(db)
    set_service = SetService(db)
    created_examinations = []

    existing_examination = examination_service.get_examination_by_sample(
        examination_data.id_sample,
    )

    if existing_examination:
        existing_examination.id_user = user_data.id
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
        ExaminationCreateResponse(
            id=existing_examination.id,
            id_sample=existing_examination.id_sample,
            tentative=existing_examination.tentative,
            BBox=bbox_list,
        )
    )

    sample = sample_service.get_sample(existing_examination.id_sample)
    package = package_service.get_package(sample.id_package)
    set_info = set_service.get_set(package.id_set)
    _ = package_service.update_package_is_ready(sample, package, set_info)

    return created_examinations[0]


@router.delete("/api/examinations/{examination_id}", tags=["Examinations"])
async def delete_examination_and_bboxes(
    examination_id: int, db: Session = Depends(get_db)
):
    examination_service = ExaminationService(db)
    bbox_service = BBoxService(db)
    package_service = PackageService(db)

    examination = examination_service.get_examination_by_id(examination_id)

    bbox_service.delete_bboxes_by_examination(examination_id)
    _ = package_service.update_package_is_ready_false(examination.id_sample)
    examination_service.delete_examination(examination_id)

    return {"message": "Examination and associated BBoxes deleted successfully"}
