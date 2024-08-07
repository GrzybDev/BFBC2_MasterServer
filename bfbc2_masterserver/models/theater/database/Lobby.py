from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from bfbc2_masterserver.enumerators.client.ClientLocale import ClientLocale

if TYPE_CHECKING:
    from bfbc2_masterserver.models.theater.database.Game import Game


class Lobby(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)

    name: str
    locale: ClientLocale
    maxGames: int = 10000

    games: list["Game"] = Relationship(back_populates="lobby")
