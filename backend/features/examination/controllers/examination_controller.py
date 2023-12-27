from typing import Annotated
from fastapi import APIRouter, Depends
from ...authorization.services.token_service import UserData, TokenService
from features.bbox.services.bbox_service import BBoxService
from features.samples.services.sample_service import SampleService
from features.packages.services.package_service import PackageService
from features.groups.services.group_service import GroupService
from connectionDB.session import get_db
from sqlalchemy.orm import Session
from ..services.examination_service import ExaminationService
from ...label.services.label_service import LabelService
from ...bbox.schemas.bbox_schema import ExtendedBBoxResponse
from ...label.schemas.label_schema import LabelResponse
from ..schemas.examination_schema import ExaminationCreate, ExtendedExaminationResponse
from repositories.group_repository import Roles

router = APIRouter()


@router.put(
    "/api/examinations",
    tags=["Examinations"],
    response_model=ExtendedExaminationResponse,
)
async def create_or_update_examinations(
    examination_create: ExaminationCreate,
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    db: Annotated[Session, Depends(get_db)],
):
    examination_service = ExaminationService(db)
    sample_service = SampleService(db)
    bbox_service = BBoxService(db)
    group_service = GroupService(db)
    package_service = PackageService(db)
    label_service = LabelService(db)

    sample = sample_service.get_sample(examination_create.id_sample)

    role = group_service.get_role_in_group(user_data.id, sample.Package.Set.id_group)

    if role != Roles.ADMIN:
        package_service.check_if_assigned_to_user(user_data.id, sample.Package)

    for bbox_create in examination_create.BBox:
        label_service.check_if_label_exists_and_belongs_to_set(
            bbox_create.id_label, sample.Package.id_set
        )

    examination = sample.Examination

    if examination:
        examination_service.update_examination(
            examination, user_data.id, examination_create.tentative
        )

        bbox_service.delete_examination_bboxes(examination.id)
    else:
        examination = examination_service.create_examination(
            user_data.id, sample.id, examination_create.tentative
        )

    user = ""

    if examination.User.title:
        user += f"{examination.User.title} "

    if examination.User.name:
        user += f"{examination.User.name} "

    if examination.User.surname:
        user += f"{examination.User.surname}"

    user_role = group_service.get_role_in_group(
        examination.User.id, sample.Package.Set.id_group
    )

    response = ExtendedExaminationResponse(
        id=examination.id,
        user=user,
        role=user_role,
        id_user=examination.id_user,
        id_sample=examination.id_sample,
        tentative=examination.tentative,
        bboxes=[],
    )

    for bbox_create in examination_create.BBox:
        bbox = bbox_service.create_bbox(
            id_examination=examination.id,
            id_label=bbox_create.id_label,
            comment=bbox_create.comment,
            x=bbox_create.x,
            y=bbox_create.y,
            width=bbox_create.width,
            height=bbox_create.height,
        )

        response.bboxes.append(
            ExtendedBBoxResponse(
                id=bbox.id,
                id_examination=bbox.id_examination,
                id_label=bbox.id_label,
                comment=bbox.comment,
                x=bbox.x,
                y=bbox.y,
                width=bbox.width,
                height=bbox.height,
                label=LabelResponse(
                    id=bbox.Label.id,
                    id_set=bbox.Label.id_set,
                    name=bbox.Label.name,
                    description=bbox.Label.description,
                    color=bbox.Label.color,
                ),
            )
        )

    if package_service.all_samples_examinated(sample.Package):
        _ = package_service.mark_as_ready(sample.Package)

    return response


@router.delete("/api/examinations/{id_examination}", tags=["Examinations"])
async def delete_examination(
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    id_examination: int,
    db: Annotated[Session, Depends(get_db)],
):
    examination_service = ExaminationService(db)
    group_service = GroupService(db)
    package_service = PackageService(db)

    examination = examination_service.get_examination(id_examination)

    role = group_service.get_role_in_group(
        user_data.id, examination.Sample.Package.Set.id_group
    )

    if role != Roles.ADMIN:
        package_service.check_if_assigned_to_user(
            user_data.id, examination.Sample.Package
        )

    examination_service.delete_examination(examination)
    package_service.mark_as_unready(examination.Sample.Package)

    return {"message": "Examination deleted successfully"}
