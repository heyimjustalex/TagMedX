from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from repositories.set_repository import SetRepository
from models.models import Set


class SetService:
    def __init__(self, db: Session):
        self.repository = SetRepository(db)

    def create_set(
        self,
        id_group: int,
        package_size: int,
        name: str | None = None,
        desc: str | None = None,
        type: str | None = None,
    ) -> Set:
        set = Set()
        set.id_group = id_group
        set.package_size = package_size
        set.name = name
        set.description = desc
        set.type = type

        self.repository.create_set(set)
        return set

    def update_set(
        self,
        id_set: int,
        name: str | None = None,
        description: str | None = None,
        type: str | None = None,
    ) -> Set:
        set = self.get_set(id_set)

        if name:
            set.name = name

        if description:
            set.description = description

        if type:
            set.type = type

        self.repository.update()
        return set

    def delete_set(self, id_set: int):
        set = self.get_set(id_set)
        self.repository.delete_set(set)

    def get_set(self, id_set: int) -> Set:
        set = self.repository.get_set_by_id(id_set)
        if not set:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Set not found"
            )
        return set

    def get_sets_in_group(self, id_group: int) -> list[Set]:
        return self.repository.get_sets_by_group(id_group)

    def get_sets_by_type(self, type: str) -> list[Set]:
        return self.repository.get_sets_by_type(type)
