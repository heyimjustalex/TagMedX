from pydantic import BaseModel
from ...users.schemas.user_schema import UserResponse


class GroupCreate(BaseModel):
    name: str


class GroupUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    connection_string: str | None = None


class GroupResposne(BaseModel):
    id: int
    name: str
    description: str | None = None


class GroupWithRoleResponse(GroupResposne):
    role: str


class AdminGroupResponse(GroupWithRoleResponse):
    connection_string: str


class GroupStatsResponse(GroupWithRoleResponse):
    sets: int
    detection_sets: int
    classification_sets: int
    packages: int
    ready_packages: int
    user_packages: int
    user_ready_packages: int
    samples: int
    examinated_samples: int
    user_samples: int
    user_examinated_samples: int
    tentative_examinations: int
    user_tentative_examinations: int


class MembershipCreate(BaseModel):
    id_user: int
    id_group: int
    role: str


class GroupMemberResponse(UserResponse):
    role: str


class GroupJoin(BaseModel):
    connection_string: str
