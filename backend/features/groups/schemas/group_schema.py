from pydantic import BaseModel

class GroupBase(BaseModel):
    name: str
    description: str | None


class GroupCreate(BaseModel):
    name: str


class GroupUpdate(GroupBase):
    pass


class GroupResposne(GroupBase):
    id: int


class GroupWithRoleResponse(GroupResposne):
    role: str
    
class AdminGroupResponse(GroupWithRoleResponse):
    connection_string: str


class MembershipBase(BaseModel):
    id_user: int
    id_group: int
    role: str


class MembershipCreate(MembershipBase):
    pass


class MembershipResponse(MembershipBase):
    id: int
    
class GroupJoin(BaseModel):
    connection_string: str
