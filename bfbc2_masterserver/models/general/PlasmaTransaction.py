from typing import Optional

from pydantic import BaseModel

from bfbc2_masterserver.enumerators.fesl.FESLTransaction import FESLTransaction


class PlasmaTransaction(BaseModel):
    TXN: Optional[FESLTransaction] = None
