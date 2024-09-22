import logging
import random
import string
import token
from base64 import b64encode

from authlib.jose import jwt
from pydantic import SecretStr, ValidationError

from bfbc2_masterserver.dataclasses.Client import Client
from bfbc2_masterserver.dataclasses.plasma.Service import PlasmaService
from bfbc2_masterserver.enumerators.client.ClientType import ClientType
from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.enumerators.fesl.FESLTransaction import FESLTransaction
from bfbc2_masterserver.error import TransactionError
from bfbc2_masterserver.messages.plasma.account.GameSpyPreAuth import (
    GameSpyPreAuthRequest,
    GameSpyPreAuthResponse,
)
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
from bfbc2_masterserver.messages.plasma.account.NuCreateEncryptedToken import (
    NuCreateEncryptedTokenRequest,
    NuCreateEncryptedTokenResponse,
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
from bfbc2_masterserver.messages.plasma.account.NuGetAccount import (
    NuGetAccountRequest,
    NuGetAccountResponse,
)
from bfbc2_masterserver.messages.plasma.account.NuGetAccountByNuid import (
    NuGetAccountByNuidRequest,
    NuGetAccountByNuidResponse,
)
from bfbc2_masterserver.messages.plasma.account.NuGetAccountByPS3Ticket import (
    NuGetAccountByPS3TicketRequest,
    NuGetAccountByPS3TicketResponse,
)
from bfbc2_masterserver.messages.plasma.account.NuGetEntitlementCount import (
    NuGetEntitlementCountRequest,
    NuGetEntitlementCountResponse,
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
from bfbc2_masterserver.messages.plasma.account.NuGrantEntitlement import (
    NuGrantEntitlementRequest,
    NuGrantEntitlementResponse,
)
from bfbc2_masterserver.messages.plasma.account.NuLogin import (
    NuLoginRequest,
    NuLoginResponse,
)
from bfbc2_masterserver.messages.plasma.account.NuLoginPersona import (
    NuLoginPersonaRequest,
    NuLoginPersonaResponse,
)
from bfbc2_masterserver.messages.plasma.account.NuLookupUserInfo import (
    NuLookupUserInfoRequest,
    NuLookupUserInfoResponse,
)
from bfbc2_masterserver.messages.plasma.account.NuPS3AddAccount import (
    NuPS3AddAccountRequest,
    NuPS3AddAccountResponse,
)
from bfbc2_masterserver.messages.plasma.account.NuPS3Login import (
    NuPS3LoginRequest,
    NuPS3LoginResponse,
)
from bfbc2_masterserver.messages.plasma.account.NuSearchOwners import (
    NuSearchOwnersRequest,
    NuSearchOwnersResponse,
)
from bfbc2_masterserver.messages.plasma.account.NuSuggestPersonas import (
    NuSuggestPersonasRequest,
    NuSuggestPersonasResponse,
)
from bfbc2_masterserver.messages.plasma.account.NuUpdateAccount import (
    NuUpdateAccountRequest,
    NuUpdateAccountResponse,
)
from bfbc2_masterserver.messages.plasma.account.NuUpdatePassword import (
    NuUpdatePasswordRequest,
    NuUpdatePasswordResponse,
)
from bfbc2_masterserver.messages.plasma.account.NuXBL360AddAccount import (
    NuXBL360AddAccountRequest,
    NuXBL360AddAccountResponse,
)
from bfbc2_masterserver.messages.plasma.account.NuXBL360Login import (
    NuXBL360LoginRequest,
    NuXBL360LoginResponse,
)
from bfbc2_masterserver.models.plasma.database.Account import Account
from bfbc2_masterserver.models.plasma.database.Persona import Persona
from bfbc2_masterserver.models.plasma.Entitlement import Entitlement
from bfbc2_masterserver.models.plasma.Owner import Owner
from bfbc2_masterserver.models.plasma.UserInfo import UserInfo
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

        self.resolvers[FESLTransaction.NuLookupUserInfo] = (
            self.__handle_nu_lookup_user_info,
            NuLookupUserInfoRequest,
        )

        self.resolvers[FESLTransaction.NuGrantEntitlement] = (
            self.__handle_nu_grant_entitlement,
            NuGrantEntitlementRequest,
        )

        self.resolvers[FESLTransaction.NuCreateEncryptedToken] = (
            self.__handle_nu_create_encrypted_token,
            NuCreateEncryptedTokenRequest,
        )

        self.resolvers[FESLTransaction.NuUpdatePassword] = (
            self.__handle_nu_update_password,
            NuUpdatePasswordRequest,
        )

        self.resolvers[FESLTransaction.NuGetAccount] = (
            self.__handle_nu_get_account,
            NuGetAccountRequest,
        )

        self.resolvers[FESLTransaction.NuGetAccountByNuid] = (
            self.__handle_nu_get_account_by_nuid,
            NuGetAccountByNuidRequest,
        )

        self.resolvers[FESLTransaction.NuGetAccountByPS3Ticket] = (
            self.__handle_nu_get_account_by_ps3_ticket,
            NuGetAccountByPS3TicketRequest,
        )

        self.resolvers[FESLTransaction.NuUpdateAccount] = (
            self.__handle_nu_update_account,
            NuUpdateAccountRequest,
        )

        self.resolvers[FESLTransaction.GameSpyPreAuth] = (
            self.__handle_gamespy_pre_auth,
            GameSpyPreAuthRequest,
        )

        self.resolvers[FESLTransaction.NuXBL360Login] = (
            self.__handle_nu_xbl360_login,
            NuXBL360LoginRequest,
        )

        self.resolvers[FESLTransaction.NuXBL360AddAccount] = (
            self.__handle_nu_xbl360_add_account,
            NuXBL360AddAccountRequest,
        )

        self.resolvers[FESLTransaction.NuPS3Login] = (
            self.__handle_nu_ps3_login,
            NuPS3LoginRequest,
        )

        self.resolvers[FESLTransaction.NuPS3AddAccount] = (
            self.__handle_nu_ps3_add_account,
            NuPS3AddAccountRequest,
        )

        self.resolvers[FESLTransaction.NuSearchOwners] = (
            self.__handle_nu_search_owners,
            NuSearchOwnersRequest,
        )

        self.resolvers[FESLTransaction.NuGetEntitlementCount] = (
            self.__handle_nu_get_entitlement_count,
            NuGetEntitlementCountRequest,
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

        countryList = getLocalizedCountryList(self.connection.locale)
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

        tos = getLocalizedTOS(self.connection.locale)
        return NuGetTosResponse(tos=tos["tos"], version=tos["version"])

    def __handle_nu_add_account(
        self, data: NuAddAccountRequest | ValidationError
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

        registered: bool = self.database.account_register(
            Account(
                nuid=data.nuid,
                password=data.password.get_secret_value(),
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
        )

        if not registered:
            return TransactionError(ErrorCode.ALREADY_REGISTERED)

        return NuAddAccountResponse()

    def __handle_nu_login(
        self, data: NuLoginRequest
    ) -> NuLoginResponse | TransactionError:
        if (not data.nuid or not data.password) and data.encryptedInfo:
            try:
                decoded_jwt = jwt.decode(
                    data.encryptedInfo.encode("utf-8"),
                    self.database._secret_key,
                )

                decoded_jwt.validate()
            except Exception as e:
                logger.error(f"Error decoding/validating JWT: {e}")
                return TransactionError(ErrorCode.SYSTEM_ERROR)

            data.nuid = decoded_jwt.get("nuid")
            data.password = SecretStr(decoded_jwt.get("password", ""))

        if not data.nuid or not data.password:
            return TransactionError(ErrorCode.PARAMETERS_ERROR)

        account: Account | ErrorCode = self.database.account_login(
            nuid=data.nuid, password=data.password.get_secret_value()
        )

        if isinstance(account, ErrorCode):
            return TransactionError(account)

        # Allow login to service account only for servers
        if self.connection.type == ClientType.Client:
            if account.serviceAccount:
                return TransactionError(ErrorCode.SYSTEM_ERROR)
        else:
            if not account.serviceAccount:
                return TransactionError(ErrorCode.SYSTEM_ERROR)

        encryptedLoginInfo: str | None = None

        if data.returnEncryptedInfo:
            encoded_jwt: bytes = jwt.encode(
                {"alg": self.database._algorithm},
                {
                    "nuid": data.nuid,
                    "password": (
                        data.password.get_secret_value()
                        if isinstance(data.password, SecretStr)
                        else data.password
                    ),
                },
                self.database._secret_key,
                check=False,
            )

            encryptedLoginInfo = encoded_jwt.decode("utf-8")

        # Check if this user already have session active
        login_key: str = (
            "".join(
                random.choice(string.ascii_letters + string.digits + "-_")
                for _ in range(27)
            )
            + "."
        )

        if not account.serviceAccount:
            # Logoff all other sessions
            if account.id in self.plasma.manager.CLIENTS:
                old_client: Client = self.plasma.manager.CLIENTS[account.id]
                old_client.plasma.disconnect(2)

            # Check whether this user accepted latest TOS
            if data.tosVersion:  # Update TOS version if provided
                self.database.account_accept_tos(account.id, data.tosVersion)
            else:
                tos = getLocalizedTOS(self.connection.locale)

                if account.tosVersion != tos["version"]:
                    return TransactionError(ErrorCode.TOS_OUT_OF_DATE)

            # Check whether this user is entitled to play the game
            if not self.connection.clientName:
                return TransactionError(ErrorCode.SYSTEM_ERROR)

            is_entitled = self.database.account_is_entitled(
                account.id, self.connection.clientName
            )

            if not is_entitled:
                return TransactionError(ErrorCode.NOT_ENTITLED_TO_GAME)

        self.connection.account = account
        self.connection.accountSession = login_key

        if self.connection.type == ClientType.Client:
            self.plasma.manager.CLIENTS[account.id] = self.plasma.client

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
    ) -> NuGetPersonasResponse | TransactionError:
        if self.connection.account is None:
            return TransactionError(ErrorCode.SYSTEM_ERROR)

        personas: list[Persona] | ErrorCode = self.database.persona_get_all(
            self.connection.account.id
        )

        if isinstance(personas, ErrorCode):
            return TransactionError(personas)

        return NuGetPersonasResponse(personas=[persona.name for persona in personas])

    def __handle_nu_add_persona(
        self, data: NuAddPersonaRequest
    ) -> NuAddPersonaResponse | TransactionError:
        if self.connection.account is None:
            return TransactionError(ErrorCode.SYSTEM_ERROR)

        new_persona = Persona(
            owner=self.connection.account,
            name=data.name,
        )

        success = self.database.persona_add(
            self.connection.account.id,
            new_persona,
        )

        if not success:
            return TransactionError(ErrorCode.SYSTEM_ERROR)

        return NuAddPersonaResponse()

    def __handle_nu_disable_persona(
        self, data: NuDisablePersonaRequest
    ) -> NuDisablePersonaResponse | TransactionError:
        if self.connection.account is None:
            return TransactionError(ErrorCode.SYSTEM_ERROR)

        persona = self.database.persona_get(self.connection.account.id, data.name)

        if isinstance(persona, ErrorCode):
            return TransactionError(persona)

        success = self.database.persona_delete(self.connection.account.id, persona.id)

        if not success:
            return TransactionError(ErrorCode.SYSTEM_ERROR)

        return NuDisablePersonaResponse()

    def __handle_nu_login_persona(
        self, data: NuLoginPersonaRequest
    ) -> NuLoginPersonaResponse | TransactionError:
        if self.connection.account is None:
            return TransactionError(ErrorCode.SYSTEM_ERROR)

        persona = self.database.persona_get(self.connection.account.id, data.name)

        if isinstance(persona, ErrorCode):
            return TransactionError(persona)

        # Generate new login key for persona
        login_key = (
            "".join(
                random.choice(string.ascii_letters + string.digits + "-_")
                for _ in range(27)
            )
            + "."
        )

        self.connection.persona = persona
        self.connection.personaSession = login_key

        if self.connection.type == ClientType.Client:
            self.plasma.manager.redis.set("client:" + login_key, persona.id)

        response = NuLoginPersonaResponse(
            lkey=login_key,
            profileId=self.connection.account.id,
            userId=persona.id,
        )

        return response

    def __handle_nu_entitle_game(
        self, data: NuEntitleGameRequest
    ) -> NuEntitleGameResponse | TransactionError:
        if (not data.nuid or not data.password) and data.encryptedInfo:
            try:
                decoded_jwt = jwt.decode(
                    data.encryptedInfo.encode("utf-8"),
                    self.database._secret_key,
                )

                decoded_jwt.validate()
            except Exception as e:
                logger.error(f"Error decoding/validating JWT: {e}")
                return TransactionError(ErrorCode.SYSTEM_ERROR)

            data.nuid = decoded_jwt.get("nuid")
            data.password = SecretStr(decoded_jwt.get("password", ""))

        if not data.nuid or not data.password:
            return TransactionError(ErrorCode.PARAMETERS_ERROR)

        account: Account | ErrorCode = self.database.account_login(
            nuid=data.nuid, password=data.password.get_secret_value()
        )

        if isinstance(account, ErrorCode):
            return TransactionError(account)

        success = self.database.account_entitle(account.id, data.key)

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
    ) -> GetTelemetryTokenResponse | TransactionError:
        token = "0.0.0.0,9946,"

        if self.connection.locale is None:
            return TransactionError(ErrorCode.SYSTEM_ERROR)

        localeStr = self.connection.locale.value.replace("_", "")

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
        if self.connection.account is None:
            return TransactionError(ErrorCode.SYSTEM_ERROR)

        groupName: str | None = data.groupName
        entitlementTag: str | None = data.entitlementTag

        if self.connection.type == ClientType.Server:
            if data.masterUserId:
                uid = data.masterUserId
            else:
                uid = 0
        else:
            uid = self.connection.account.id

        entitlements = self.database.account_get_entitlements(
            uid,
            groupName,
            entitlementTag,
        )

        if isinstance(entitlements, ErrorCode):
            return TransactionError(entitlements)

        return NuGetEntitlementsResponse(
            entitlements=[
                Entitlement(
                    userId=entitlement.owner.id,
                    groupName=entitlement.groupName,
                    entitlementId=entitlement.id,
                    entitlementTag=entitlement.tag,
                    productId=entitlement.productId,
                    version=entitlement.version,
                    grantDate=entitlement.grantDate,
                    terminationDate=entitlement.terminationDate,
                    status="ACTIVE",
                )
                for entitlement in entitlements
            ]
        )

    def __handle_get_locker_url(
        self, data: GetLockerURLRequest
    ) -> GetLockerURLResponse:
        return GetLockerURLResponse(
            url="http://bfbc2.gos.ea.com/fileupload/locker2.jsp"
        )

    def __handle_nu_entitle_user(
        self, data: NuEntitleUserRequest
    ) -> NuEntitleUserResponse | TransactionError:
        if self.connection.account is None:
            return TransactionError(ErrorCode.SYSTEM_ERROR)

        productList = self.database.account_entitle(
            self.connection.account.id, data.key
        )

        if isinstance(productList, ErrorCode):
            return TransactionError(productList)

        return NuEntitleUserResponse(
            productList=[
                Entitlement(
                    userId=product.owner.id,
                    groupName=product.groupName,
                    entitlementId=product.id,
                    entitlementTag=product.tag,
                    productId=product.productId,
                    version=product.version,
                    grantDate=product.grantDate,
                    terminationDate=product.terminationDate,
                    status="ACTIVE",
                )
                for product in productList
            ]
        )

    def __handle_nu_lookup_user_info(
        self, data: NuLookupUserInfoRequest
    ) -> NuLookupUserInfoResponse | TransactionError:
        response: list[UserInfo] = []

        for request in data.userInfo:
            userInfo = self.database.persona_get_by_name(request.userName)

            if isinstance(userInfo, ErrorCode):
                return TransactionError(ErrorCode.TRANSACTION_DATA_NOT_FOUND)

            response.append(
                UserInfo(
                    userName=userInfo.name,
                    namespace="battlefield",
                    userId=userInfo.id,
                    masterUserId=userInfo.owner.id,
                )
            )

        return NuLookupUserInfoResponse(userInfo=response)

    def __handle_nu_grant_entitlement(
        self, data: NuGrantEntitlementRequest
    ) -> NuGrantEntitlementResponse | TransactionError:
        self.database.account_grant_entitlement(data)
        return NuGrantEntitlementResponse()

    def __handle_nu_create_encrypted_token(
        self, data: NuCreateEncryptedTokenRequest
    ) -> NuCreateEncryptedTokenResponse | TransactionError:
        # I don't know what is the expected response for this transaction
        # Name suggest that it should create new session? But I don't think it's ever called by the client
        raise NotImplementedError("NuCreateEncryptedToken is not implemented")

    def __handle_nu_suggest_personas(
        self, data: NuSuggestPersonasRequest
    ) -> NuSuggestPersonasResponse | TransactionError:
        # Is this ever called from the client?

        # Not sure what "name" is here, but I assume it's the name of the currently logged persona
        if not self.connection.persona:
            return TransactionError(ErrorCode.SESSION_NOT_AUTHORIZED)

        if self.connection.persona.name != data.name:
            return TransactionError(ErrorCode.SYSTEM_ERROR)

        # I don't know what is the expected response for this transaction
        raise NotImplementedError("NuSuggestPersonas is not implemented")

    def __handle_nu_update_password(
        self, data: NuUpdatePasswordRequest
    ) -> NuUpdatePasswordResponse | TransactionError:
        # Is this ever called from the client?
        raise NotImplementedError("NuUpdatePassword is not implemented")

    def __handle_nu_get_account(
        self, data: NuGetAccountRequest
    ) -> NuGetAccountResponse | TransactionError:
        # Is this ever called from the client?
        raise NotImplementedError("NuGetAccount is not implemented")

    def __handle_nu_get_account_by_nuid(
        self, data: NuGetAccountByNuidRequest
    ) -> NuGetAccountByNuidResponse | TransactionError:
        # Is this ever called from the client?
        raise NotImplementedError("NuGetAccountByNuid is not implemented")

    def __handle_nu_get_account_by_ps3_ticket(
        self, data: NuGetAccountByPS3TicketRequest
    ) -> NuGetAccountByPS3TicketResponse | TransactionError:
        # Is this ever called from the client?
        raise NotImplementedError("NuGetAccountByPS3Ticket is not implemented")

    def __handle_nu_update_account(
        self, data: NuUpdateAccountRequest
    ) -> NuUpdateAccountResponse | TransactionError:
        # Is this ever called from the client?
        raise NotImplementedError("NuUpdateAccount is not implemented")

    def __handle_gamespy_pre_auth(
        self, data: GameSpyPreAuthRequest
    ) -> GameSpyPreAuthResponse | TransactionError:
        # Is this ever called from the client?
        raise NotImplementedError("GameSpyPreAuth is not implemented")

    def __handle_nu_xbl360_login(
        self, data: NuXBL360LoginRequest
    ) -> NuXBL360LoginResponse | TransactionError:
        # Is this ever called from the client?
        raise NotImplementedError("NuXBL360Login is not implemented")

    def __handle_nu_xbl360_add_account(
        self, data: NuXBL360AddAccountRequest
    ) -> NuXBL360AddAccountResponse | TransactionError:
        # Is this ever called from the client?
        raise NotImplementedError("NuXBL360AddAccount is not implemented")

    def __handle_nu_ps3_login(
        self, data: NuPS3LoginRequest
    ) -> NuPS3LoginResponse | TransactionError:
        # Is this ever called from the client?
        raise NotImplementedError("NuPS3Login is not implemented")

    def __handle_nu_ps3_add_account(
        self, data: NuPS3AddAccountRequest
    ) -> NuPS3AddAccountResponse | TransactionError:
        # Is this ever called from the client?
        raise NotImplementedError("NuPS3AddAccount is not implemented")

    def __handle_nu_search_owners(
        self, data: NuSearchOwnersRequest
    ) -> NuSearchOwnersResponse | TransactionError:
        owners = self.database.persona_search(data.screenName)
        return NuSearchOwnersResponse(
            users=[Owner(id=owner.id, name=owner.name, type=1) for owner in owners],
            nameSpaceId="battlefield",
        )

    def __handle_nu_get_entitlement_count(
        self, data: NuGetEntitlementCountRequest
    ) -> NuGetEntitlementCountResponse | TransactionError:
        # Is this ever called from the client?
        raise NotImplementedError("NuGetEntitlementCount is not implemented")
