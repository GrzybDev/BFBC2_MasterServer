from dataclasses import dataclass
from typing import TYPE_CHECKING

from bfbc2_masterserver.dataclasses.Connection import BaseConnection

if TYPE_CHECKING:
    from bfbc2_masterserver.dataclasses.Handler import (
        BasePlasmaHandler,
        BaseTheaterHandler,
    )


class Client:
    connection: BaseConnection

    plasma: "BasePlasmaHandler"
    theater: "BaseTheaterHandler"
