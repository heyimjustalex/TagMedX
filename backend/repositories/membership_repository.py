from sqlalchemy.orm import Session
from models.models import Membership


class MembershipRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_membership(self, membership: Membership):
        self.db.add(membership)
        self.db.commit()

    def update(self):
        self.db.commit()

    def delete_membership(self, membership: Membership):
        self.db.delete(membership)
        self.db.commit()

    def get_membership(self, user_id: int, group_id: int) -> Membership | None:
        return (
            self.db.query(Membership)
            .filter(Membership.id_user == user_id, Membership.id_group == group_id)
            .first()
        )
