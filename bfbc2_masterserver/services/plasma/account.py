import random
import string

from jose import jwt
from pydantic import ValidationError

from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode
from bfbc2_masterserver.enumerators.Transaction import Transaction
from bfbc2_masterserver.error import TransactionError
from bfbc2_masterserver.message import Message
from bfbc2_masterserver.messages.plasma.account.GetCountryList import (
    GetCountryListRequest,
    GetCountryListResponse,
)
from bfbc2_masterserver.messages.plasma.account.NuAddAccount import (
    NuAddAccountRequest,
    NuAddAccountResponse,
)
from bfbc2_masterserver.messages.plasma.account.NuGetTos import (
    NuGetTosRequest,
    NuGetTosResponse,
)
from bfbc2_masterserver.messages.plasma.account.NuLogin import (
    NuLoginRequest,
    NuLoginResponse,
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

        response = GetCountryListResponse(
            countryList=getLocalizedCountryList(self.plasma.clientLocale)
        )

        return Message(data=response.model_dump(exclude_none=True))

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

        response = NuGetTosResponse(tos=tos["tos"], version=tos["version"])
        return Message(data=response.model_dump(exclude_none=True))

    def __handle_nu_add_account(self, data: NuAddAccountRequest):
        try:
            data = NuAddAccountRequest.model_validate(data)
        except ValidationError as e:
            errContainer = []

            for error in e.errors():
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

        registered = self.plasma.db.register(
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

        response = NuAddAccountResponse()
        return Message(data=response.model_dump(exclude_none=True))

    def __handle_nu_login(self, data: NuLoginRequest):
        account = self.plasma.db.login(nuid=data.nuid, password=data.password)
        account_id = str(account["_id"])

        if isinstance(account, ErrorCode):
            return TransactionError(account)

        encryptedLoginInfo = None

        if data.returnEncryptedInfo:
            encoded_jwt = jwt.encode(
                {"nuid": data.nuid},
                self.plasma.db.secret_key,
                algorithm=self.plasma.db.algorithm,
            )

            encryptedLoginInfo = encoded_jwt

        # Check if this user already have session active
        user_session = self.plasma.redis.get(f"session:{account_id}")
        login_key = (
            "".join(
                random.choice(string.ascii_letters + string.digits + "-_")
                for _ in range(27)
            )
            + "."
        )

        if user_session and not account.get("serviceAccount", False):
            # TODO: Log out the user from the previous session
            pass

        self.plasma.redis.set(f"session:{account_id}", login_key)

        response = NuLoginResponse(
            nuid=data.nuid,
            lkey=login_key,
            profileId=account_id,
            userId=account_id,
            encryptedLoginInfo=encryptedLoginInfo,
        )

        return Message(data=response.model_dump(exclude_none=True))
