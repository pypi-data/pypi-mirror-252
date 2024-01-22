from fastapi import HTTPException


class InternalBaseException(HTTPException):
    STATUS_CODE: int = None
    DETAIL: str = None

    def __init__(self):
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL)
