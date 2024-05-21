import os
import random
import string
from operator import is_

from jose import jwt
from pydantic import ValidationError

from bfbc2_masterserver.enumerators.client.ClientType import ClientType
from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.enumerators.Transaction import Transaction
from bfbc2_masterserver.error import TransactionError
from bfbc2_masterserver.message import Message
from bfbc2_masterserver.messages.Client import Client
from bfbc2_masterserver.messages.plasma.account.GetCountryList import (
    GetCountryListRequest,
    GetCountryListResponse,
)
from bfbc2_masterserver.messages.plasma.account.NuAddAccount import (
    NuAddAccountRequest,
    NuAddAccountResponse,
)
from bfbc2_masterserver.messages.plasma.account.NuAddPersona import (
    NuAddPersonaRequest,
    NuAddPersonaResponse,
)
from bfbc2_masterserver.messages.plasma.account.NuDisablePersona import (
    NuDisablePersonaRequest,
    NuDisablePersonaResponse,
)
from bfbc2_masterserver.messages.plasma.account.NuEntitleGame import (
    NuEntitleGameRequest,
    NuEntitleGameResponse,
)
from bfbc2_masterserver.messages.plasma.account.NuGetPersonas import (
    NuGetPersonasRequest,
    NuGetPersonasResponse,
)
from bfbc2_masterserver.messages.plasma.account.NuGetTos import (
    NuGetTosRequest,
    NuGetTosResponse,
)
from bfbc2_masterserver.messages.plasma.account.NuLogin import (
    NuLoginRequest,
    NuLoginResponse,
)
from bfbc2_masterserver.messages.plasma.account.NuLoginPersona import (
    NuLoginPersonaRequest,
    NuLoginPersonaResponse,
)
from bfbc2_masterserver.services.service import Service
from bfbc2_masterserver.tools.country_list import getLocalizedCountryList
from bfbc2_masterserver.tools.terms_of_service import getLocalizedTOS


class AccountService(Service):

    def __init__(self, plasma) -> None:
        super().__init__(plasma)

        self.resolvers[Transaction.GetCountryList] = (
            self.__handle_get_country_list,
            GetCountryListRequest,
        )
        self.resolvers[Transaction.NuGetTos] = self.__handle_nu_get_tos, NuGetTosRequest
        self.resolvers[Transaction.NuAddAccount] = (
            self.__handle_nu_add_account,
            NuAddAccountRequest,
        )
        self.resolvers[Transaction.NuLogin] = self.__handle_nu_login, NuLoginRequest
        self.resolvers[Transaction.NuGetPersonas] = (
            self.__handle_nu_get_personas,
            NuGetPersonasRequest,
        )

        self.resolvers[Transaction.NuAddPersona] = (
            self.__handle_nu_add_persona,
            NuAddPersonaRequest,
        )

        self.resolvers[Transaction.NuDisablePersona] = (
            self.__handle_nu_disable_persona,
            NuDisablePersonaRequest,
        )

        self.resolvers[Transaction.NuLoginPersona] = (
            self.__handle_nu_login_persona,
            NuLoginPersonaRequest,
        )

        self.resolvers[Transaction.NuEntitleGame] = (
            self.__handle_nu_entitle_game,
            NuEntitleGameRequest,
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

    def __handle_get_country_list(self, data: GetCountryListRequest):
        """
        Handles the GetCountryList transaction.

        Parameters:
            data (dict): The incoming data.

        Returns:
            The response to the transaction.
        """

        countryList = getLocalizedCountryList(self.plasma.clientLocale)

        return GetCountryListResponse(countryList=countryList)

    def __handle_nu_get_tos(self, data: NuGetTosRequest):
        """
        Handles the NuGetTos transaction.

        Parameters:
            data (dict): The incoming data.

        Returns:
            The response to the transaction.
        """

        # In theory everything shows that here we should send the TOS for the selected country code.
        # However, this doesn't seem to be the case. Original server sends the same TOS for every country code, only (game) language seems to have any effect.

        tos = getLocalizedTOS(self.plasma.clientLocale)
        return NuGetTosResponse(tos=tos["tos"], version=tos["version"])

    def __handle_nu_add_account(self, data: NuAddAccountRequest | ValidationError):
        if isinstance(data, ValidationError):
            errContainer = []

            for error in data.errors():
                if error["loc"]:
                    errContainer.append(
                        {
                            "fieldName": (
                                error["loc"][0]
                                if error["loc"][0] != "nuid"
                                else "email"
                            ),
                            "fieldError": 6,
                            "value": "INVALID_VALUE",
                        }
                    )
                else:
                    errContainer.append(
                        {
                            "fieldName": "dob",
                            "fieldError": 15,
                        }
                    )

            return TransactionError(ErrorCode.PARAMETERS_ERROR, errContainer)

        registered = self.database.register(
            nuid=data.nuid,
            password=data.password,
            globalOptin=data.globalOptin,
            thirdPartyOptin=data.thirdPartyOptin,
            parentalEmail=data.parentalEmail,
            DOBDay=data.DOBDay,
            DOBMonth=data.DOBMonth,
            DOBYear=data.DOBYear,
            zipCode=data.zipCode,
            country=data.country,
            language=data.language,
            tosVersion=data.tosVersion,
        )

        if isinstance(registered, ErrorCode):
            return TransactionError(registered)

        return NuAddAccountResponse()

    def __handle_nu_login(self, data: NuLoginRequest):
        account = self.database.login(nuid=data.nuid, password=data.password)

        if isinstance(account, ErrorCode):
            return TransactionError(account)

        account_id = int(account["_id"])
        client_type = self.plasma.clientType
        is_service_account = account.get("serviceAccount", False)

        # Allow login to service account only for servers
        if client_type == ClientType.Client:
            if is_service_account:
                return TransactionError(ErrorCode.SYSTEM_ERROR)
        else:
            if not is_service_account:
                return TransactionError(ErrorCode.SYSTEM_ERROR)

        encryptedLoginInfo = None

        if data.returnEncryptedInfo:
            encoded_jwt = jwt.encode(
                {"nuid": data.nuid},
                self.database.secret_key,
                algorithm=self.database.algorithm,
            )

            encryptedLoginInfo = encoded_jwt

        # Check if this user already have session active
        user_session = self.redis.get(f"account:{account_id}")
        login_key = (
            "".join(
                random.choice(string.ascii_letters + string.digits + "-_")
                for _ in range(27)
            )
            + "."
        )

        if not is_service_account:
            # Logoff all other sessions
            if user_session:
                old_client: Client = self.plasma.manager.CLIENTS[account_id]
                old_client.plasma.disconnect(2)

            # Check whether this user accepted latest TOS
            if data.tosVersion:  # Update TOS version if provided
                self.database.accept_tos(account_id, data.tosVersion)
            else:
                tos = getLocalizedTOS(self.plasma.clientLocale)

                if account.get("tosVersion", None) != tos["version"]:
                    return TransactionError(ErrorCode.TOS_OUT_OF_DATE)

            # Check whether this user is entitled to play the game
            is_entitled = self.database.is_entitled(
                account_id, self.plasma.clientString
            )

            if not is_entitled:
                return TransactionError(ErrorCode.NOT_ENTITLED_TO_GAME)

        self.redis.set(f"account:{account_id}", login_key)
        self.redis.set(f"session:{login_key}", account_id)

        self.plasma.accountID = account_id
        self.plasma.loginKey = login_key

        if client_type == ClientType.Client:
            self.plasma.manager.CLIENTS[account_id] = Client(plasma=self.plasma)
        else:
            self.plasma.manager.SERVERS[account_id] = Client(plasma=self.plasma)

        response = NuLoginResponse(
            nuid=data.nuid,
            lkey=login_key,
            profileId=account_id,
            userId=account_id,
            encryptedLoginInfo=encryptedLoginInfo,
        )

        return response

    def __handle_nu_get_personas(self, data: NuGetPersonasRequest):
        personas = self.database.get_personas(account_id=self.plasma.accountID)
        return NuGetPersonasResponse(personas=personas)

    def __handle_nu_add_persona(self, data: NuAddPersonaRequest):
        success = self.database.add_persona(
            account_id=self.plasma.accountID, name=data.name
        )

        if isinstance(success, ErrorCode):
            return TransactionError(success)

        return NuAddPersonaResponse()

    def __handle_nu_disable_persona(self, data: NuDisablePersonaRequest):
        success = self.database.disable_persona(
            account_id=self.plasma.accountID, name=data.name
        )

        if not success:
            return TransactionError(ErrorCode.TRANSACTION_DATA_NOT_FOUND)

        return NuDisablePersonaResponse()

    def __handle_nu_login_persona(self, data: NuLoginPersonaRequest):
        persona = self.database.get_persona(
            account_id=self.plasma.accountID, name=data.name
        )

        if not persona:
            return TransactionError(ErrorCode.USER_NOT_FOUND)

        # Generate new login key for persona
        login_key = (
            "".join(
                random.choice(string.ascii_letters + string.digits + "-_")
                for _ in range(27)
            )
            + "."
        )

        persona_id = int(persona["_id"])

        self.plasma.personaID = persona_id
        self.plasma.personaLoginKey = login_key

        self.redis.set(f"profile:{persona_id}", login_key)
        self.redis.set(f"persona:{login_key}", persona_id)

        response = NuLoginPersonaResponse(
            lkey=login_key,
            profileId=persona_id,
            userId=self.plasma.accountID,
        )
        return response

    def __handle_nu_entitle_game(self, data: NuEntitleGameRequest):
        account = self.database.login(nuid=data.nuid, password=data.password)

        if isinstance(account, ErrorCode):
            return TransactionError(account)

        success = self.database.entitle_game(account=account, key=data.key)

        if isinstance(success, ErrorCode):
            return TransactionError(success)

        response = NuEntitleGameResponse(
            nuid=data.nuid,
            lkey="",
            profileId=account["_id"],
            userId=account["_id"],
        )

        return response
