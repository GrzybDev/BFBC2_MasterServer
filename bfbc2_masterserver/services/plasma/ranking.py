from bfbc2_masterserver.enumerators.Transaction import Transaction
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
)
from bfbc2_masterserver.messages.Stats import RankedStat, RankedStatReturn
from bfbc2_masterserver.services.service import Service


class RankingService(Service):

    def __init__(self, plasma) -> None:
        super().__init__(plasma)

        self.resolvers[Transaction.GetStats] = (
            self.__handle_get_stats,
            GetStatsRequest,
        )

        self.resolvers[Transaction.GetRankedStatsForOwners] = (
            self.__handle_get_ranked_stats_for_owners,
            GetRankedStatsForOwnersRequest,
        )

        self.resolvers[Transaction.GetRankedStats] = (
            self.__handle_get_ranked_stats,
            GetRankedStatsRequest,
        )

        self.resolvers[Transaction.GetTopNAndStats] = (
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
        return self.resolvers[Transaction(txn)]

    def _get_generator(self, txn):
        """
        Gets the generator for a given transaction.

        Parameters:
            txn (str): The name of the transaction.

        Returns:
            The generator function for the transaction.
        """
        return self.generators[Transaction(txn)]

    def __handle_get_stats(self, data: GetStatsRequest):
        stats = self.database.get_stats(self.plasma.userId, data.keys)
        return GetStatsResponse(stats=stats)

    def __handle_get_ranked_stats_for_owners(
        self, data: GetRankedStatsForOwnersRequest
    ):
        stats: list[RankedStatReturn] = []

        for owner in data.owners:
            ownerStats = self.database.get_ranked_stats(owner.ownerId, data.keys)

            stats.append(
                RankedStatReturn(
                    rankedStats=ownerStats,
                    ownerId=owner.ownerId,
                    ownerType=owner.ownerType,
                )
            )

        return GetRankedStatsForOwnersResponse(rankedStats=stats)

    def __handle_get_ranked_stats(self, data: GetRankedStatsRequest):
        stats = self.database.get_ranked_stats(self.plasma.userId, data.keys)
        return GetRankedStatsResponse(stats=stats)

    def __handle_get_top_n_and_stats(self, data: GetTopNAndStatsRequest):
        leaderboard = self.database.get_leaderboard(data.keys)
        return GetTopNAndStatsResponse(stats=leaderboard)
