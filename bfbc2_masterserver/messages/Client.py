from typing import Any, Optional

from pydantic import BaseModel


class Client(BaseModel):
    plasma: Any
    theater: Optional[Any] = None
