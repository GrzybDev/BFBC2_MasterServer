from bfbc2_masterserver.enumerators.Transaction import Transaction
from bfbc2_masterserver.messages.plasma.ranking.GetStats import (
    GetStatsRequest,
    GetStatsResponse,
)
from bfbc2_masterserver.services.service import Service


class RankingService(Service):

    def __init__(self, plasma) -> None:
        super().__init__(plasma)

        self.resolvers[Transaction.GetStats] = (
            self.__handle_get_stats,
            GetStatsRequest,
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
