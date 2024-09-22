from decimal import Decimal

from bfbc2_masterserver.dataclasses.plasma.Service import PlasmaService
from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.enumerators.fesl.FESLTransaction import FESLTransaction
from bfbc2_masterserver.error import TransactionError
from bfbc2_masterserver.messages.plasma.ranking.GetDateRange import (
    GetDateRangeRequest,
    GetDateRangeResponse,
)
from bfbc2_masterserver.messages.plasma.ranking.GetRankedStatsForOwners import (
    GetRankedStatsForOwnersRequest,
    GetRankedStatsForOwnersResponse,
)
from bfbc2_masterserver.messages.plasma.ranking.GetRankedStatsRequest import (
    GetRankedStatsRequest,
    GetRankedStatsResponse,
)
from bfbc2_masterserver.messages.plasma.ranking.GetStats import (
    GetStatsRequest,
    GetStatsResponse,
)
from bfbc2_masterserver.messages.plasma.ranking.GetStatsForOwners import (
    GetStatsForOwnersRequest,
    GetStatsForOwnersResponse,
)
from bfbc2_masterserver.messages.plasma.ranking.GetTopN import (
    GetTopNRequest,
    GetTopNResponse,
)
from bfbc2_masterserver.messages.plasma.ranking.GetTopNAndMe import (
    GetTopNAndMeRequest,
    GetTopNAndMeResponse,
)
from bfbc2_masterserver.messages.plasma.ranking.GetTopNAndStats import (
    GetTopNAndStatsRequest,
    GetTopNAndStatsResponse,
    Leaderboard,
)
from bfbc2_masterserver.messages.plasma.ranking.UpdateStats import (
    UpdateStatsRequest,
    UpdateStatsResponse,
)
from bfbc2_masterserver.models.plasma.database.Ranking import Ranking
from bfbc2_masterserver.models.plasma.Stats import RankedOwnerStat, RankedStat, Stat


class RankingService(PlasmaService):

    def __init__(self, plasma) -> None:
        super().__init__(plasma)

        self.resolvers[FESLTransaction.GetStats] = (
            self.__handle_get_stats,
            GetStatsRequest,
        )

        self.resolvers[FESLTransaction.GetRankedStatsForOwners] = (
            self.__handle_get_ranked_stats_for_owners,
            GetRankedStatsForOwnersRequest,
        )

        self.resolvers[FESLTransaction.GetRankedStats] = (
            self.__handle_get_ranked_stats,
            GetRankedStatsRequest,
        )

        self.resolvers[FESLTransaction.GetTopNAndStats] = (
            self.__handle_get_top_n_and_stats,
            GetTopNAndStatsRequest,
        )

        self.resolvers[FESLTransaction.UpdateStats] = (
            self.__handle_update_stats,
            UpdateStatsRequest,
        )

        self.resolvers[FESLTransaction.GetStatsForOwners] = (
            self.__handle_get_stats_for_owners,
            GetStatsForOwnersRequest,
        )

        self.resolvers[FESLTransaction.GetTopN] = (
            self.__handle_get_top_n,
            GetTopNRequest,
        )

        self.resolvers[FESLTransaction.GetTopNAndMe] = (
            self.__handle_get_top_n_and_me,
            GetTopNAndMeRequest,
        )

        self.resolvers[FESLTransaction.GetDateRange] = (
            self.__handle_get_date_range,
            GetDateRangeRequest,
        )

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

    def __handle_get_stats(
        self, data: GetStatsRequest
    ) -> GetStatsResponse | TransactionError:
        if self.connection.persona is None:
            return TransactionError(ErrorCode.SYSTEM_ERROR)

        ranking: list[Ranking] = self.database.ranking_get(
            self.connection.persona.id, data.keys
        )

        stats: list[Stat] = [Stat(key=rank.key, value=rank.value) for rank in ranking]
        return GetStatsResponse(stats=stats)

    def __handle_get_ranked_stats_for_owners(
        self, data: GetRankedStatsForOwnersRequest
    ) -> GetRankedStatsForOwnersResponse:
        rankedStats = self.database.ranking_get_ranked_owners(
            [owner.ownerId for owner in data.owners], data.keys
        )

        stats: list[RankedOwnerStat] = []

        for owner in data.owners:
            stats.append(
                RankedOwnerStat(
                    ownerId=owner.ownerId,
                    ownerType=owner.ownerType,
                    rankedStats=[
                        RankedStat(
                            key=stat.key,
                            value=Decimal(min(stat.value, 250001)),
                            rank=rank,
                        )
                        for stat, rank in rankedStats
                        if stat.owner_id == owner.ownerId
                    ],
                )
            )

        return GetRankedStatsForOwnersResponse(rankedStats=stats)

    def __handle_get_ranked_stats(
        self, data: GetRankedStatsRequest
    ) -> GetRankedStatsResponse | TransactionError:
        if self.connection.persona is None:
            return TransactionError(ErrorCode.SYSTEM_ERROR)

        rankedStats = self.database.ranking_get_ranked(
            self.connection.persona.id, data.keys
        )

        stats = [
            RankedStat(key=stat.key, value=Decimal(min(stat.value, 250001)), rank=rank)
            for stat, rank in rankedStats
        ]

        return GetRankedStatsResponse(stats=stats)

    def __handle_get_top_n_and_stats(
        self, data: GetTopNAndStatsRequest
    ) -> GetTopNAndStatsResponse:
        ranking = self.database.ranking_leaderboard_get(
            data.key, data.minRank, data.maxRank
        )

        leaderboard = []

        for persona, rank in ranking:
            persona_stats = self.database.ranking_get(persona.owner.id, data.keys)

            leaderboard.append(
                Leaderboard(
                    addStats=[
                        Stat(key=stat.key, value=Decimal(min(stat.value, 250001)))
                        for stat in persona_stats
                    ],
                    owner=persona.owner.id,
                    name=persona.owner.name,
                    rank=rank,
                )
            )

        return GetTopNAndStatsResponse(stats=leaderboard)

    def __handle_update_stats(self, data: UpdateStatsRequest) -> UpdateStatsResponse:
        for request in data.u:
            for stat in request.s:
                self.database.ranking_set(request.o, stat.k, stat.v, stat.ut)

        return UpdateStatsResponse()

    def __handle_get_stats_for_owners(
        self, data: GetStatsForOwnersRequest
    ) -> GetStatsForOwnersResponse:
        raise NotImplementedError("GetStatsForOwners is not implemented")

    def __handle_get_top_n(self, data: GetTopNRequest) -> GetTopNResponse:
        raise NotImplementedError("GetTopN is not implemented")

    def __handle_get_top_n_and_me(
        self, data: GetTopNAndMeRequest
    ) -> GetTopNAndMeResponse:
        raise NotImplementedError("GetTopNAndMe is not implemented")

    def __handle_get_date_range(
        self, data: GetDateRangeRequest
    ) -> GetDateRangeResponse:
        raise NotImplementedError("GetDateRange is not implemented")
