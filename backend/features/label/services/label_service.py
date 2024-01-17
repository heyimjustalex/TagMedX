from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from repositories.label_repository import LabelRepository
from repositories.sample_repository import SampleRepository
from models.models import Label, Sample
from datetime import datetime


def export_to_coco(samples: list[Sample]):
    current_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    current_year = datetime.now().year

    coco_data = {
        "info": {
            "year": current_year,
            "version": "1.0",
            "description": "",
            "contributor": "",
            "url": "",
            "date_created": current_date,
        },
        "images": [],
        "licenses": [{"id": "", "name": "", "url": ""}],
        "annotations": [],
        "categories": [],
    }

    label_id_mapping = {}

    category_id = 1
    for sample in samples:
        for bbox in sample.Examination.BBox:
            label_id = bbox.Label.id
            if label_id not in label_id_mapping:
                label_id_mapping[label_id] = category_id
                coco_data["categories"].append(
                    {"id": category_id, "name": bbox.Label.name, "supercategory": ""}
                )
                category_id += 1

    annotation_id = 1
    for sample in samples:
        image_id = sample.id
        sample_path = sample.path
        image_info = {
            "id": image_id,
            "width": "",
            "height": "",
            "file_name": sample_path,
            "license": "",
            "flickr_url": "",
            "coco_url": "",
            "date_captured": "",
        }
        coco_data["images"].append(image_info)

        for bbox in sample.Examination.BBox:
            label_id = bbox.Label.id
            category_id = label_id_mapping[label_id]

            x, y, width, height = bbox.x, bbox.y, bbox.width, bbox.height

            bbox_info = [x, y, width, height]

            annotation_info = {
                "id": annotation_id,
                "image_id": image_id,
                "category_id": category_id,
                "segmentation": "",
                "area": width * height,
                "bbox": bbox_info,
                "iscrowd": 0,
            }
            coco_data["annotations"].append(annotation_info)
            annotation_id += 1

    return coco_data


class LabelService:
    def __init__(self, db: Session):
        self.repository = LabelRepository(db)
        self.repository_sample = SampleRepository(db)

    def create_label(
        self,
        id_set: int,
        name: str | None = None,
        desc: str | None = None,
        color: str | None = None,
    ) -> Label:
        label = Label()
        label.id_set = id_set
        label.name = name
        label.description = desc
        label.color = color

        self.repository.create_label(label)
        return label

    def update_label(
        self,
        id_label: int,
        name: str | None = None,
        description: str | None = None,
        color: str | None = None,
    ) -> Label:
        label = self.get_label(id_label)

        if name:
            label.name = name

        if description:
            label.description = description

        label.color = color

        self.repository.update()
        return label

    def delete_label(self, id_label: int):
        label = self.get_label(id_label)
        self.repository.delete_label(label)

    def get_label(self, id_label: int) -> Label:
        label = self.repository.get_label_by_id(id_label)
        if not label:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Label not found"
            )
        return label

    def get_labels_for_set(self, id_set: int) -> list[Label]:
        return self.repository.get_labels_by_set(id_set)

    def get_labels_in_group(self, id_group: int) -> list[Label]:
        return self.repository.get_labels_by_group(id_group)

    def check_if_label_exists_and_belongs_to_set(self, id_label: int, id_set: int):
        label = self.get_label(id_label)
        if label.id_set != id_set:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"Label {id_label} does not belong to the set",
            )

    def export_annotations_from_package_to_coco(self, package_id: int):
        samples_data = self.repository_sample.get_samples_by_package(package_id)
        coco_data = export_to_coco(samples_data)
        return coco_data

    def export_annotations_from_set_to_coco(self, set_id: int):
        samples_data = self.repository_sample.get_samples_from_set(set_id)
        coco_data = export_to_coco(samples_data)
        return coco_data
