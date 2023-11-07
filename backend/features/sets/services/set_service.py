from fastapi import HTTPException
from sqlalchemy.orm import Session
from repositories.set_repository import SetRepository
from ..schemas.set_schema import SetCreate
from features.exceptions.definitions.definitions import PermissionDenied


class SetService:
    def __init__(self, db: Session):
        self.db = db
        self.set_repository = SetRepository(db)

    def create_set_with_permission_check(
        self, set_data: SetCreate, current_user_id: int
    ):
        group_id = set_data.id_group

        if not self.set_repository.is_user_admin_in_group(current_user_id, group_id):
            raise PermissionDenied(status_code=403, detail="Permission denied")

        set = self.set_repository.create_set(set_data)
        return set

    def get_set_by_id(self, set_id):
        set = self.set_repository.get_set_by_id(set_id)
        if not set:
            raise HTTPException(status_code=404, detail="Set not found")
        return set

    def get_user_sets(self, user_id: int):
        return self.set_repository.get_user_sets(user_id)

    def update_set(self, set_id: int, new_set_data):
        update_set = self.set_repository.update_set(set_id, new_set_data)
        if not update_set:
            raise HTTPException(status_code=404, detail="Set not found")
        return update_set

    def delete_set(self, set_id: int):
        return self.set_repository.delete_set(set_id)
