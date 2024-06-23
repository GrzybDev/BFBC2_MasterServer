from datetime import datetime
from typing import Tuple

import bcrypt
from mongoengine import Q, connect
from pydantic import SecretStr
from redis import Redis

from bfbc2_masterserver.database.database import BaseDatabase
from bfbc2_masterserver.database.mongo.documents.Accounts import Accounts
from bfbc2_masterserver.database.mongo.documents.Entitlements import Entitlements
from bfbc2_masterserver.database.mongo.documents.Keys import Keys
from bfbc2_masterserver.database.mongo.documents.Personas import Personas
from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.enumerators.plasma.AssocationType import AssocationType
from bfbc2_masterserver.messages.Account import Account
from bfbc2_masterserver.messages.Persona import Persona
from bfbc2_masterserver.messages.plasma.Association import Association
from bfbc2_masterserver.messages.plasma.Entitlement import Entitlement


class MongoDB(BaseDatabase):

    redis: Redis

    def __init__(self, connection_string: str, redis: Redis):
        super().__init__(connection_string)

        self.redis = redis

        connect(host=connection_string)
        self.prepare_db()

    def register(self, **kwargs) -> bool | ErrorCode:
        if Accounts.objects(nuid=kwargs["nuid"]).first():
            return ErrorCode.ALREADY_REGISTERED

        hashed_password = bcrypt.hashpw(
            kwargs["password"].get_secret_value().encode("utf-8"), bcrypt.gensalt()
        )

        seq_account = self.redis.incr("seq:account")

        account = Accounts(
            id=seq_account,
            nuid=kwargs["nuid"],
            password=hashed_password.decode(),
            globalOptin=kwargs.get("globalOptin", False),
            thirdPartyOptin=kwargs.get("thirdPartyOptin", False),
            parentalEmail=kwargs.get("parentalEmail", None),
            DOBDay=kwargs.get("DOBDay", None),
            DOBMonth=kwargs.get("DOBMonth", None),
            DOBYear=kwargs.get("DOBYear", None),
            zipCode=kwargs.get("zipCode", None),
            country=kwargs.get("country", None),
            language=kwargs.get("language", None),
            tosVersion=kwargs.get("tosVersion", None),
            serviceAccount=kwargs.get("serviceAccount", False),
        ).save()

        return True

    def login(self, **kwargs) -> Account | ErrorCode:
        account = Accounts.objects(nuid=kwargs["nuid"]).first()

        if not account:
            return ErrorCode.USER_NOT_FOUND

        password = kwargs["password"]

        if password is None:
            return ErrorCode.INVALID_PASSWORD
        else:
            password = (
                password.get_secret_value()
                if isinstance(password, SecretStr)
                else password
            )

        if not bcrypt.checkpw(
            password.encode("utf-8"),
            account.password.encode("utf-8"),
        ):
            return ErrorCode.INVALID_PASSWORD

        return self.get_account(account.id)

    def get_account(self, account_id) -> Account | ErrorCode:
        account = Accounts.objects(id=account_id).first()

        if isinstance(account, Accounts) is False:
            return ErrorCode.USER_NOT_FOUND

        return Account(
            id=account.id,
            password=account.password,
            nuid=account.nuid,
            globalOptin=account.globalOptin,
            thirdPartyOptin=account.thirdPartyOptin,
            parentalEmail=account.parentalEmail,
            DOBDay=account.DOBDay,
            DOBMonth=account.DOBMonth,
            DOBYear=account.DOBYear,
            zipCode=account.zipCode,
            country=account.country,
            language=account.language,
            tosVersion=account.tosVersion,
            serviceAccount=account.serviceAccount,
        )

    def get_personas(self, account_id) -> list[str]:
        account = Accounts.objects(id=account_id).first()
        personas_list = []

        for persona in account.personas:
            personas_list.append(persona["name"])

        return personas_list

    def add_persona(self, account_id, name) -> bool | ErrorCode:
        account = Accounts.objects(id=account_id).first()

        if isinstance(account, Accounts) is False:
            return ErrorCode.USER_NOT_FOUND

        seq_persona = self.redis.incr("seq:persona")

        persona = Personas(
            id=seq_persona,
            name=name,
        ).save()

        account.personas.append(persona)
        account.save()

        return True

    def disable_persona(self, account_id, name) -> bool | ErrorCode:
        account = Accounts.objects(id=account_id).first()

        # Check if the persona belongs to the account
        if not account:
            return ErrorCode.USER_NOT_FOUND

        for persona in account.personas:
            if persona.name == name:
                Personas(name=name).delete()

        return True

    def get_persona(self, account_id, name) -> Persona | ErrorCode:
        account = Accounts.objects(id=account_id).first()

        if isinstance(account, Accounts) is False:
            return ErrorCode.USER_NOT_FOUND

        personas = account.personas

        for persona in personas:
            if persona.name == name:
                return Persona(id=persona.id, name=persona.name)

        return ErrorCode.USER_NOT_FOUND

    def get_persona_by_id(self, persona_id) -> Persona | ErrorCode:
        persona = Personas.objects(id=persona_id).first()

        if isinstance(persona, Personas) is False:
            return ErrorCode.USER_NOT_FOUND

        return Persona(id=persona.id, name=persona.name)

    def accept_tos(self, account_id, version) -> bool | ErrorCode:
        account = Accounts.objects(id=account_id).first()

        if isinstance(account, Accounts) is False:
            return ErrorCode.USER_NOT_FOUND

        account.tosVersion = version
        account.save()

        return True

    def is_entitled(self, account_id, entitlement_id) -> bool:
        account = Accounts.objects(id=account_id).first()

        if isinstance(account, Accounts) is False:
            return False

        for entitlement in account.entitlements:
            if entitlement.tag == entitlement_id:
                return True

        return False

    def entitle_game(self, account_id, key) -> bool | ErrorCode:
        account = Accounts.objects(id=account_id).first()

        if isinstance(account, Accounts) is False:
            return ErrorCode.USER_NOT_FOUND

        key = Keys.objects(key=key, active=True).first()

        if isinstance(key, Keys) is False:
            return ErrorCode.CODE_NOT_FOUND

        # Add the entitlement to the account
        for target in key.targets:
            entitlement = Entitlements(
                tag=target.tag,
                grant_date=datetime.now(),
                termination_date=None,
                group_name=target.group,
                product_id=target.product,
                version=0,
                is_game_entitlement=target.isGameEntitlement,
            )

            entitlement.save()

            account.entitlements.append(entitlement)
            account.save()

        if key.consumable:
            key.active = False
            key.save()

        return True

    def get_assocation(
        self, persona_id: int, association_type: AssocationType
    ) -> Tuple[str, list[Association]] | ErrorCode:
        persona = Personas.objects(id=persona_id).first()

        if isinstance(persona, Personas) is False:
            return ErrorCode.USER_NOT_FOUND

        match association_type:
            case AssocationType.PlasmaBlock:
                associations = persona.blocked
            case AssocationType.PlasmaFriends:
                associations = persona.friends
            case AssocationType.PlasmaMute:
                associations = persona.muted
            case AssocationType.PlasmaRecentPlayers:
                associations = persona.recent
            case _:
                raise ValueError("Invalid association type")

        associations = [
            Association(
                id=association.id,
                name=association.name,
                type=1,
                created=association.created_at,
                modified=association.updated_at,
            )
            for association in associations
        ]

        return persona.name, associations

    def get_entitlements(
        self, account_id, groupName, entitlementTag
    ) -> list[Entitlement] | ErrorCode:
        account = Accounts.objects(id=account_id).first()

        if isinstance(account, Accounts) is False:
            return ErrorCode.USER_NOT_FOUND

        filtered = []

        for entitlement in account.entitlements:
            # Filter out entitlements
            if entitlement.group_name == groupName or entitlement.tag == entitlementTag:
                filtered.append(entitlement)

        return [
            Entitlement(
                userId=account_id,
                entitlementId=entitlement.id,
                entitlementTag=entitlement.tag,
                grantDate=entitlement.grant_date,
                terminationDate=entitlement.termination_date,
                groupName=entitlement.group_name,
                productId=entitlement.product_id,
                version=entitlement.version,
                status="ACTIVE",
            )
            for entitlement in filtered
        ]

    def _add_key(self, data, consumable=True) -> None:
        key = Keys.objects(key=data["key"]).first()

        if key:
            return

        Keys(
            key=data["key"],
            targets=[
                {
                    "tag": target["tag"],
                    "group": target.get("group", None),
                    "product": target.get("product", None),
                    "isGameEntitlement": target.get("isGameEntitlement", False),
                }
                for target in data["targets"]
            ],
            consumable=consumable,
        ).save()
