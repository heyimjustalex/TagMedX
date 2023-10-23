from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    surname: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class GroupBase(BaseModel):
    name: str
    description: str


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupBase):
    pass


class Group(GroupBase):
    id: int


class MembershipBase(BaseModel):
    id_user: int
    id_group: int


class MembershipCreate(MembershipBase):
    pass


class Membership(MembershipBase):
    id: int
