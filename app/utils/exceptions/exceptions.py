from typing import Any, Dict, Optional
from fastapi import HTTPException, status

class DuplicatedError(HTTPException):
    def __init__(self, detail: Any = None, data: Any = None, headers: Optional[Dict[str, Any]] = None) -> None:
        # If data is provided, include it in the response detail
        if data:
            if isinstance(detail, dict):
                detail["data"] = data
            else:
                detail = {"message": detail, "data": data}
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail, headers=headers)

class AuthError(HTTPException):
    def __init__(self, detail: Any = None, data: Any = None, headers: Optional[Dict[str, Any]] = None) -> None:
        # If data is provided, include it in the response detail
        if data:
            if isinstance(detail, dict):
                detail["data"] = data
            else:
                detail = {"message": detail, "data": data}
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail, headers=headers)

class NotFoundError(HTTPException):
    def __init__(self, detail: Any = None, data: Any = None, headers: Optional[Dict[str, Any]] = None) -> None:
        # If data is provided, include it in the response detail
        if data:
            if isinstance(detail, dict):
                detail["data"] = data
            else:
                detail = {"message": detail, "data": data}
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail, headers=headers)

class ValidationError(HTTPException):
    def __init__(self, detail: Any = None, data: Any = None, headers: Optional[Dict[str, Any]] = None) -> None:
        # If data is provided, include it in the response detail
        if data:
            if isinstance(detail, dict):
                detail["data"] = data
            else:
                detail = {"message": detail, "data": data}
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail, headers=headers)
