from typing import Optional

from pydantic import BaseModel

from bfbc2_masterserver.enumerators.Transaction import Transaction


class PlasmaTransaction(BaseModel):
    TXN: Optional[Transaction] = None
