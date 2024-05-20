import bcrypt
from pymongo import MongoClient
from pymongo.database import Database

from bfbc2_masterserver.database.database import BaseDatabase
from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.error import TransactionError


class MongoDB(BaseDatabase):

    client: MongoClient
    database: Database

    def __init__(self, connection_string: str):
        super().__init__(connection_string)

        self.client = MongoClient(connection_string)

        try:
            self.client.admin.command("ping")
        except Exception as e:
            raise ConnectionError(f"Unable to connect to MongoDB: {e}")

        self.database = self.client["bfbc2emu"]
        self.prepare_db()

    def register(self, **kwargs):
        accounts = self.database["accounts"]

        if accounts.find_one({"nuid": kwargs["nuid"]}):
            return ErrorCode.ALREADY_REGISTERED

        hashed_password = bcrypt.hashpw(
            kwargs["password"].encode("utf-8"), bcrypt.gensalt()
        )

        accounts.insert_one(
            {
                "nuid": kwargs["nuid"],
                "password": hashed_password.decode(),
                "globalOptin": kwargs.get("globalOptin", False),
                "thirdPartyOptin": kwargs.get("thirdPartyOptin", False),
                "parentalEmail": kwargs.get("parentalEmail", None),
                "DOBDay": kwargs.get("DOBDay", None),
                "DOBMonth": kwargs.get("DOBMonth", None),
                "DOBYear": kwargs.get("DOBYear", None),
                "zipCode": kwargs.get("zipCode", None),
                "country": kwargs.get("country", None),
                "language": kwargs.get("language", None),
                "tosVersion": kwargs.get("tosVersion", None),
                "serviceAccount": kwargs.get("serviceAccount", False),
            }
        )

        return True

    def login(self, **kwargs):
        accounts = self.database["accounts"]

        account = accounts.find_one({"nuid": kwargs["nuid"]})

        if not account:
            return ErrorCode.USER_NOT_FOUND

        if not bcrypt.checkpw(
            kwargs["password"].encode("utf-8"), account["password"].encode("utf-8")
        ):
            return ErrorCode.INVALID_PASSWORD

        return account
