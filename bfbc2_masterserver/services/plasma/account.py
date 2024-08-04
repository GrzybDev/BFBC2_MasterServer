import logging
import random
import string
from base64 import b64encode

from authlib.jose import jwt
from pydantic import SecretStr, ValidationError

from bfbc2_masterserver.dataclasses.Client import Client
from bfbc2_masterserver.dataclasses.plasma.Service import PlasmaService
from bfbc2_masterserver.enumerators.client.ClientType import ClientType
from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.enumerators.fesl.FESLTransaction import FESLTransaction
from bfbc2_masterserver.error import TransactionError
from bfbc2_masterserver.messages.plasma.account.GetCountryList import (
    GetCountryListRequest,
    GetCountryListResponse,
)
from bfbc2_masterserver.messages.plasma.account.GetLockerURL import (
    GetLockerURLRequest,
    GetLockerURLResponse,
)
from bfbc2_masterserver.messages.plasma.account.GetTelemetryToken import (
    GetTelemetryTokenRequest,
    GetTelemetryTokenResponse,
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
from bfbc2_masterserver.messages.plasma.account.NuEntitleUser import (
    NuEntitleUserRequest,
    NuEntitleUserResponse,
)
from bfbc2_masterserver.messages.plasma.account.NuGetEntitlements import (
    NuGetEntitlementsRequest,
    NuGetEntitlementsResponse,
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
from bfbc2_masterserver.models.plasma.database.Account import Account
from bfbc2_masterserver.models.plasma.database.Entitlement import Entitlement
from bfbc2_masterserver.tools.country_list import COUNTRY_LIST, getLocalizedCountryList
from bfbc2_masterserver.tools.terms_of_service import getLocalizedTOS

logger = logging.getLogger(__name__)


class AccountService(PlasmaService):

    def __init__(self, plasma) -> None:
        super().__init__(plasma)

        self.resolvers[FESLTransaction.GetCountryList] = (
            self.__handle_get_country_list,
            GetCountryListRequest,
        )
        self.resolvers[FESLTransaction.NuGetTos] = (
            self.__handle_nu_get_tos,
            NuGetTosRequest,
        )
        self.resolvers[FESLTransaction.NuAddAccount] = (
            self.__handle_nu_add_account,
            NuAddAccountRequest,
        )
        self.resolvers[FESLTransaction.NuLogin] = (
            self.__handle_nu_login,
            NuLoginRequest,
        )
        self.resolvers[FESLTransaction.NuGetPersonas] = (
            self.__handle_nu_get_personas,
            NuGetPersonasRequest,
        )

        self.resolvers[FESLTransaction.NuAddPersona] = (
            self.__handle_nu_add_persona,
            NuAddPersonaRequest,
        )

        self.resolvers[FESLTransaction.NuDisablePersona] = (
            self.__handle_nu_disable_persona,
            NuDisablePersonaRequest,
        )

        self.resolvers[FESLTransaction.NuLoginPersona] = (
            self.__handle_nu_login_persona,
            NuLoginPersonaRequest,
        )

        self.resolvers[FESLTransaction.NuEntitleGame] = (
            self.__handle_nu_entitle_game,
            NuEntitleGameRequest,
        )

        self.resolvers[FESLTransaction.GetTelemetryToken] = (
            self.__handle_get_telemetry_token,
            GetTelemetryTokenRequest,
        )

        self.resolvers[FESLTransaction.NuGetEntitlements] = (
            self.__handle_nu_get_entitlements,
            NuGetEntitlementsRequest,
        )

        self.resolvers[FESLTransaction.GetLockerURL] = (
            self.__handle_get_locker_url,
            GetLockerURLRequest,
        )

        self.resolvers[FESLTransaction.NuEntitleUser] = (
            self.__handle_nu_entitle_user,
            NuEntitleUserRequest,
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

    def __handle_get_country_list(
        self, data: GetCountryListRequest
    ) -> GetCountryListResponse:
        """
        Handles the GetCountryList transaction.

        Parameters:
            data (dict): The incoming data.

        Returns:
            The response to the transaction.
        """

        countryList = getLocalizedCountryList(self.plasma.connection.locale)
        return GetCountryListResponse(countryList=countryList)

    def __handle_nu_get_tos(self, data: NuGetTosRequest) -> NuGetTosResponse:
        """
        Handles the NuGetTos transaction.

        Parameters:
            data (dict): The incoming data.

        Returns:
            The response to the transaction.
        """

        # In theory everything shows that here we should send the TOS for the selected country code.
        # However, this doesn't seem to be the case. Original server sends the same TOS for every country code, only (game) language seems to have any effect.

        tos = getLocalizedTOS(self.plasma.connection.locale)
        return NuGetTosResponse(tos=tos["tos"], version=tos["version"])

    def __handle_nu_add_account(
        self, data: NuAddAccountRequest
    ) -> NuAddAccountResponse | TransactionError:
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

        registered: bool | ErrorCode = self.database.register(
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

    def __handle_nu_login(
        self, data: NuLoginRequest
    ) -> NuLoginResponse | TransactionError:
        if (not data.nuid or not data.password) and data.encryptedInfo:
            try:
                decoded_jwt = jwt.decode(
                    data.encryptedInfo.encode("utf-8"),
                    self.database.secret_key,
                )

                decoded_jwt.validate()
            except Exception as e:
                logger.error(f"Error decoding/validating JWT: {e}")
                return TransactionError(ErrorCode.SYSTEM_ERROR)

            data.nuid = decoded_jwt.get("nuid")
            data.password = decoded_jwt.get("password")

        if not data.nuid or not data.password:
            return TransactionError(ErrorCode.PARAMETERS_ERROR)

        account: Account | ErrorCode = self.database.login(
            nuid=data.nuid, password=data.password
        )

        if isinstance(account, ErrorCode):
            return TransactionError(account)

        client_type: ClientType = self.plasma.connection.type
        is_service_account: bool = account.serviceAccount

        # Allow login to service account only for servers
        if client_type == ClientType.Client:
            if is_service_account:
                return TransactionError(ErrorCode.SYSTEM_ERROR)
        else:
            if not is_service_account:
                return TransactionError(ErrorCode.SYSTEM_ERROR)

        encryptedLoginInfo: str | None = None

        if data.returnEncryptedInfo:
            encoded_jwt: bytes = jwt.encode(
                {"alg": self.database.algorithm},
                {
                    "nuid": data.nuid,
                    "password": (
                        data.password.get_secret_value()
                        if isinstance(data.password, SecretStr)
                        else data.password
                    ),
                },
                self.database.secret_key,
                check=False,
            )

            encryptedLoginInfo = encoded_jwt.decode("utf-8")

        # Check if this user already have session active
        user_session = self.redis.get(f"account:{account.id}")
        login_key: str = (
            "".join(
                random.choice(string.ascii_letters + string.digits + "-_")
                for _ in range(27)
            )
            + "."
        )

        if not is_service_account:
            # Logoff all other sessions
            if user_session:
                old_client: Client = self.plasma.manager.CLIENTS[account.id]
                old_client.plasma.disconnect(2)

            # Check whether this user accepted latest TOS
            if data.tosVersion:  # Update TOS version if provided
                self.database.accept_tos(account.id, data.tosVersion)
            else:
                tos = getLocalizedTOS(self.plasma.connection.locale)

                if account.tosVersion != tos["version"]:
                    return TransactionError(ErrorCode.TOS_OUT_OF_DATE)

            # Check whether this user is entitled to play the game
            is_entitled = self.database.is_entitled(
                account.id, self.plasma.connection.clientName
            )

            if not is_entitled:
                return TransactionError(ErrorCode.NOT_ENTITLED_TO_GAME)

        self.redis.set(f"account:{account.id}", login_key)
        self.redis.set(f"session:{login_key}", account.id)

        self.plasma.connection.accountId = account.id
        self.plasma.connection.accountLoginKey = login_key

        client = Client()
        client.plasma = self.plasma

        if client_type == ClientType.Client:
            self.plasma.manager.CLIENTS[account.id] = client

        response = NuLoginResponse(
            nuid=data.nuid,
            lkey=login_key,
            profileId=account.id,
            userId=account.id,
            encryptedLoginInfo=encryptedLoginInfo,
        )

        return response

    def __handle_nu_get_personas(
        self, data: NuGetPersonasRequest
    ) -> NuGetPersonasResponse:
        personas = self.database.get_personas(
            account_id=self.plasma.connection.accountId
        )
        return NuGetPersonasResponse(personas=personas)

    def __handle_nu_add_persona(
        self, data: NuAddPersonaRequest
    ) -> NuAddPersonaResponse | TransactionError:
        success = self.database.add_persona(
            account_id=self.plasma.connection.accountId, name=data.name
        )

        if isinstance(success, ErrorCode):
            return TransactionError(success)

        return NuAddPersonaResponse()

    def __handle_nu_disable_persona(
        self, data: NuDisablePersonaRequest
    ) -> NuDisablePersonaResponse | TransactionError:
        success = self.database.disable_persona(
            account_id=self.plasma.connection.accountId, name=data.name
        )

        if isinstance(success, ErrorCode):
            return TransactionError(success)

        return NuDisablePersonaResponse()

    def __handle_nu_login_persona(
        self, data: NuLoginPersonaRequest
    ) -> NuLoginPersonaResponse | TransactionError:
        persona = self.database.get_persona(
            account_id=self.plasma.connection.accountId, name=data.name
        )

        if isinstance(persona, ErrorCode):
            return TransactionError(ErrorCode.USER_NOT_FOUND)

        # Generate new login key for persona
        login_key = (
            "".join(
                random.choice(string.ascii_letters + string.digits + "-_")
                for _ in range(27)
            )
            + "."
        )

        self.plasma.connection.personaId = persona.id
        self.plasma.connection.personaLoginKey = login_key
        self.plasma.connection.personaName = persona.name

        self.redis.set(f"profile:{persona.id}", login_key)
        self.redis.set(f"persona:{login_key}", persona.id)

        response = NuLoginPersonaResponse(
            lkey=login_key,
            profileId=self.plasma.connection.accountId,
            userId=persona.id,
        )

        return response

    def __handle_nu_entitle_game(
        self, data: NuEntitleGameRequest
    ) -> NuEntitleGameResponse | TransactionError:
        account: Account | ErrorCode = self.database.login(
            nuid=data.nuid, password=data.password
        )

        if isinstance(account, ErrorCode):
            return TransactionError(account)

        success: bool | ErrorCode = self.database.entitle_game(
            account_id=account.id, key=data.key
        )

        if isinstance(success, ErrorCode):
            return TransactionError(success)

        response = NuEntitleGameResponse(
            nuid=data.nuid,
            lkey="",
            profileId=account.id,
            userId=account.id,
        )

        return response

    def __handle_get_telemetry_token(
        self, data: GetTelemetryTokenRequest
    ) -> GetTelemetryTokenResponse:
        token = "0.0.0.0,9946,"
        localeStr = self.plasma.connection.locale.value.replace("_", "")

        if len(localeStr) == 2:
            localeStr = localeStr + localeStr.upper()

        token += localeStr

        # Token also have some encoded data (for telemetry)
        # We don't need it, so we just fill it with zeros

        # Token length is 104 bytes (at least that's what I've seen in original server)
        token += "\0" * 104
        token = b64encode(token.encode("utf-8")).decode("utf-8")

        response = GetTelemetryTokenResponse(
            telemetryToken=token,
            enabled=",".join(COUNTRY_LIST.keys()),
            filters="",
            disabled="",
        )

        return response

    def __handle_nu_get_entitlements(
        self, data: NuGetEntitlementsRequest
    ) -> NuGetEntitlementsResponse | TransactionError:
        groupName: str = data.groupName
        entitlementTag: str | None = data.entitlementTag

        uid: int | None = (
            data.masterUserId
            if self.plasma.connection.type == ClientType.Server
            else self.plasma.connection.accountId
        )

        entitlements: list[Entitlement] | ErrorCode = self.database.get_entitlements(
            account_id=uid, groupName=groupName, entitlementTag=entitlementTag
        )

        if isinstance(entitlements, ErrorCode):
            return TransactionError(entitlements)

        return NuGetEntitlementsResponse(entitlements=entitlements)

    def __handle_get_locker_url(
        self, data: GetLockerURLRequest
    ) -> GetLockerURLResponse:
        return GetLockerURLResponse(
            url="http://bfbc2.gos.ea.com/fileupload/locker2.jsp"
        )

    def __handle_nu_entitle_user(
        self, data: NuEntitleUserRequest
    ) -> NuEntitleUserResponse | TransactionError:
        productList: list[Entitlement] | ErrorCode = self.database.entitle_user(
            account_id=self.plasma.connection.accountId, key=data.key
        )

        if isinstance(productList, ErrorCode):
            return TransactionError(productList)

        return NuEntitleUserResponse(productList=productList)
