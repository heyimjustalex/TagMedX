from fastapi import HTTPException


class GroupNotFoundException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)
        self.context = "Group not found"


class UserNotFoundException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)
        self.context = "User not found"
