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


class MembershipCreate(BaseModel):
    id_user: int
    id_group: int
    role: str


class GroupMemberResponse(UserResponse):
    role: str


class GroupMemberListResponse(BaseModel):
    members: list[GroupMemberResponse]


class GroupJoin(BaseModel):
    connection_string: str
