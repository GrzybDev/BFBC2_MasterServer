from bfbc2_masterserver.dataclasses.plasma.Service import PlasmaService
from bfbc2_masterserver.enumerators.fesl.FESLTransaction import FESLTransaction
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
from bfbc2_masterserver.messages.plasma.ranking.GetTopNAndStats import (
    GetTopNAndStatsRequest,
    GetTopNAndStatsResponse,
    Leaderboard,
)
from bfbc2_masterserver.models.plasma.database.Stats import (
    RankedOwnerStat,
    RankedStat,
    Stat,
)


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

    def __handle_get_stats(self, data: GetStatsRequest) -> GetStatsResponse:
        stats: list[Stat] = self.database.get_stats(
            self.plasma.connection.personaId, data.keys
        )
        return GetStatsResponse(stats=stats)

    def __handle_get_ranked_stats_for_owners(
        self, data: GetRankedStatsForOwnersRequest
    ) -> GetRankedStatsForOwnersResponse:
        stats: list[RankedOwnerStat] = []

        for owner in data.owners:
            ownerStats: list[RankedStat] = self.database.get_ranked_stats(
                owner.ownerId, data.keys
            )

            stats.append(
                RankedOwnerStat(
                    rankedStats=ownerStats,
                    ownerId=owner.ownerId,
                    ownerType=owner.ownerType,
                )
            )

        return GetRankedStatsForOwnersResponse(rankedStats=stats)

    def __handle_get_ranked_stats(
        self, data: GetRankedStatsRequest
    ) -> GetRankedStatsResponse:
        stats: list[RankedStat] = self.database.get_ranked_stats(
            self.plasma.connection.personaId, data.keys
        )
        return GetRankedStatsResponse(stats=stats)

    def __handle_get_top_n_and_stats(
        self, data: GetTopNAndStatsRequest
    ) -> GetTopNAndStatsResponse:
        leaderboard: list[Leaderboard] = self.database.get_leaderboard(data.keys)
        return GetTopNAndStatsResponse(stats=leaderboard)
