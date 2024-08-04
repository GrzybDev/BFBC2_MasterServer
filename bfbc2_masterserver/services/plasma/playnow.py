import asyncio

from h11 import Response

from bfbc2_masterserver.dataclasses.plasma.Service import PlasmaService
from bfbc2_masterserver.enumerators.fesl.FESLService import FESLService
from bfbc2_masterserver.enumerators.fesl.FESLTransaction import FESLTransaction
from bfbc2_masterserver.messages.plasma.playnow.Start import StartRequest, StartResponse
from bfbc2_masterserver.messages.plasma.playnow.Status import (
    StatusRequest,
    StatusResponse,
)


class PlayNowService(PlasmaService):

    def __init__(self, plasma) -> None:
        super().__init__(plasma)

        self.resolvers[FESLTransaction.Start] = (
            self.__handle_start,
            StartRequest,
        )

        self.generators[FESLTransaction.Status] = self.__create_status

    def _get_resolver(self, txn):
        """
        Gets the resolver for a given transaction.

        Parameters:
            txn (str): The name of the transaction.

        Returns:
            The resolver function for the transaction.
        """
        return self.resolvers[FESLTransaction(txn)]

    def _get_generator(self, txn):
        """
        Gets the generator for a given transaction.

        Parameters:
            txn (str): The name of the transaction.

        Returns:
            The generator function for the transaction.
        """
        return self.generators[FESLTransaction(txn)]

    def __handle_start(self, data: StartRequest) -> StartResponse:
        matchmakingId = self.redis.incr("matchmakingId")

        # Create a new matchmaking session
        # It seems that we never have the ability to have more than one player here
        params = data.players[0].props

        loop = asyncio.get_event_loop()
        loop.create_task(
            self.__matchmaking(matchmakingId, params),
        )

        return StartResponse(
            id={
                "id": matchmakingId,
                "partition": data.partition.partition,
            }
        )

    async def __matchmaking(self, matchmakingId, params):
        # These are the only parameters that seem that client can modify
        # TODO: Make a more proper matchmaking system
        prefGamemode = params.get("prefGamemode")
        prefLevel = params.get("prefLevel")

        game = self.database.find_game(prefGamemode, prefLevel)

        if game:
            self.plasma.start_transaction(
                FESLService.PlayNowService,
                FESLTransaction.Status,
                StatusRequest(
                    id=matchmakingId,
                    gid=game.GID,
                    lid=game.LID,
                ),
            )
        else:
            self.plasma.start_transaction(
                FESLService.PlayNowService,
                FESLTransaction.Status,
                StatusRequest(id=matchmakingId),
            )

    def __create_status(self, data: StatusRequest):
        games = []

        if data.gid:
            games.append({"fit": 1001, "gid": data.gid, "lid": data.lid})

        return StatusResponse(
            id={"id": data.id, "partition": "/eagames/BFBC2"},
            props={"{resultType}": "JOIN", "{games}": games},
            sessionState="COMPLETE",
        )
