import bcrypt
from bson import ObjectId
from pymongo import MongoClient
from pymongo.database import Database

from bfbc2_masterserver.database.database import BaseDatabase
from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode


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
            kwargs["password"].get_secret_value().encode("utf-8"), bcrypt.gensalt()
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
            kwargs["password"].get_secret_value().encode("utf-8"),
            account["password"].encode("utf-8"),
        ):
            return ErrorCode.INVALID_PASSWORD

        return account

    def get_personas(self, account_id):
        personas = self.database["personas"]

        account_personas = list(personas.find({"account": ObjectId(account_id)}))
        personas_list = []

        for persona in account_personas:
            personas_list.append(persona["name"])

        return personas_list

    def add_persona(self, account_id, name):
        personas = self.database["personas"]

        if personas.find_one({"name": name}):
            return ErrorCode.ALREADY_REGISTERED

        personas.insert_one({"account": ObjectId(account_id), "name": name})
        return True

    def disable_persona(self, account_id, name):
        personas = self.database["personas"]
        return personas.delete_one({"account": ObjectId(account_id), "name": name})

    def get_persona(self, account_id, name):
        personas = self.database["personas"]
        return personas.find_one({"account": ObjectId(account_id), "name": name})

    def accept_tos(self, account_id, version):
        accounts = self.database["accounts"]
        return accounts.update_one(
            {"_id": ObjectId(account_id)}, {"$set": {"tosVersion": version}}
        )

    def is_entitled(self, account_id, entitlement_id):
        accounts = self.database["accounts"]
        account = accounts.find_one({"_id": ObjectId(account_id)})

        if not account:
            return False

        entitlements = account.get("entitlements", [])
        global_entitlements = self.database["entitlements"]

        user_entitlements = [
            entitlement["entitlement"]
            for entitlement in list(
                global_entitlements.find({"_id": {"$in": entitlements}})
            )
        ]

        return entitlement_id in user_entitlements

    def entitle_game(self, account_id, key):
        accounts = self.database["accounts"]
        entitlements = self.database["entitlements"]

        # Check if the key is valid
        entitlement = entitlements.find_one({"key": key, "used_by": None})
        if not entitlement:
            return ErrorCode.CODE_NOT_FOUND

        if not entitlement.get("isGameEntitlement", False):
            return ErrorCode.CODE_NOT_FOUND

        account = accounts.find_one({"_id": ObjectId(account_id)})
        if not account:
            return ErrorCode.USER_NOT_FOUND

        # Add the entitlement to the account
        user_entitlements = account.get("entitlements", [])
        user_entitlements.append(entitlement["_id"])
        accounts.update_one(
            {"_id": ObjectId(account_id)}, {"$set": {"entitlements": user_entitlements}}
        )

        # Mark the key as used
        if entitlement.get("consumable", True):
            entitlements.update_one(
                {"key": key}, {"$set": {"used_by": ObjectId(account_id)}}
            )

        return True
