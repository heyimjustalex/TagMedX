from fastapi import HTTPException

# Our exceptions to raise IN SERVICES when there is no records or other error


class UserNotFoundException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)
        self.context = "User not found"
