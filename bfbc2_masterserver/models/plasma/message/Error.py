from typing import Optional

from pydantic import BaseModel


class Error(BaseModel):
    fieldName: str
    fieldError: int
    value: Optional[str] = None
