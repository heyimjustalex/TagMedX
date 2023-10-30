from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    surname: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class GroupBase(BaseModel):
    name: str
    description: str
    connection_string: str


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupBase):
    pass


class Group(GroupBase):
    id: int


class MembershipBase(BaseModel):
    id_user: int
    id_group: int
    role: str


class MembershipCreate(MembershipBase):
    pass


class Membership(MembershipBase):
    id: int
