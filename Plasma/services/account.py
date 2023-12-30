import csv
import json
import os
import random
import string
from base64 import b64decode, b64encode
from datetime import date
from enum import Enum
from pathlib import Path

from asgiref.sync import sync_to_async
from channels.auth import database_sync_to_async, get_user, login
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from django.core.cache import cache
from django.core.exceptions import ValidationError
from email_validator import EmailNotValidError, validate_email

from BFBC2_MasterServer.packet import Packet
from BFBC2_MasterServer.service import Service
from BFBC2_MasterServer.tools import legacy_b64encode
from Plasma.enumerators.ActivationResult import ActivationResult
from Plasma.enumerators.ClientType import ClientType
from Plasma.error import TransactionError
from Plasma.models import Account, Entitlement, Persona


class TXN(Enum):
    NuLogin = "NuLogin"
    NuAddAccount = "NuAddAccount"
    NuAddPersona = "NuAddPersona"
    NuDisablePersona = "NuDisablePersona"
    GetCountryList = "GetCountryList"
    NuGetTos = "NuGetTos"
    NuCreateEncryptedToken = "NuCreateEncryptedToken"
    NuSuggestPersonas = "NuSuggestPersonas"
    NuLoginPersona = "NuLoginPersona"
    NuUpdatePassword = "NuUpdatePassword"
    NuGetAccount = "NuGetAccount"
    NuGetAccountByNuid = "NuGetAccountByNuid"
    NuGetAccountByPS3Ticket = "NuGetAccountByPS3Ticket"
    NuGetPersonas = "NuGetPersonas"
    NuUpdateAccount = "NuUpdateAccount"
    GameSpyPreAuth = "GameSpyPreAuth"
    NuXBL360Login = "NuXBL360Login"
    NuXBL360AddAccount = "NuXBL360AddAccount"
    NuPS3Login = "NuPS3Login"
    NuPS3AddAccount = "NuPS3AddAccount"
    TransactionException = "TransactionException"
    NuLookupUserInfo = "NuLookupUserInfo"
    NuSearchOwners = "NuSearchOwners"
    GetTelemetryToken = "GetTelemetryToken"
    NuGetEntitlements = "NuGetEntitlements"
    NuGetEntitlementCount = "NuGetEntitlementCount"
    NuEntitleGame = "NuEntitleGame"
    NuEntitleUser = "NuEntitleUser"
    NuGrantEntitlement = "NuGrantEntitlement"
    GetLockerURL = "GetLockerURL"


class AccountService(Service):
    ENCRYPTED_PREFIX = "Ciyvab0tregdVsBtboIpeChe4G6uzC1v5_-SIxmvSL"

    countryListPath = os.path.join(settings.BASE_DIR, "Plasma/data/CountryList")
    tosPath = os.path.join(settings.BASE_DIR, "Plasma/data/TOS")

    countryConfigOverrides = {}
    validCountryCodes = []

    def __init__(self, connection) -> None:
        super().__init__(connection)

        self.resolver_map[TXN.NuLogin] = self.__handle_login
        self.resolver_map[TXN.NuAddAccount] = self.__handle_add_account
        self.resolver_map[TXN.NuAddPersona] = self.__handle_add_persona
        self.resolver_map[TXN.NuDisablePersona] = self.__handle_disable_persona
        self.resolver_map[TXN.GetCountryList] = self.__handle_get_country_list
        self.resolver_map[TXN.NuGetTos] = self.__handle_get_tos
        self.resolver_map[
            TXN.NuCreateEncryptedToken
        ] = self.__handle_create_encrypted_token
        self.resolver_map[TXN.NuSuggestPersonas] = self.__handle_suggest_personas
        self.resolver_map[TXN.NuLoginPersona] = self.__handle_login_persona
        self.resolver_map[TXN.NuUpdatePassword] = self.__handle_update_password
        self.resolver_map[TXN.NuGetAccount] = self.__handle_get_account
        self.resolver_map[TXN.NuGetAccountByNuid] = self.__handle_get_account_by_nuid
        self.resolver_map[
            TXN.NuGetAccountByPS3Ticket
        ] = self.__handle_get_account_by_ps3_ticket
        self.resolver_map[TXN.NuGetPersonas] = self.__handle_get_personas
        self.resolver_map[TXN.NuUpdateAccount] = self.__handle_update_account
        self.resolver_map[TXN.GameSpyPreAuth] = self.__handle_gamespy_preauth
        self.resolver_map[TXN.NuXBL360Login] = self.__handle_xbl360_login
        self.resolver_map[TXN.NuXBL360AddAccount] = self.__handle_xbl360_add_account
        self.resolver_map[TXN.NuPS3Login] = self.__handle_ps3_login
        self.resolver_map[TXN.NuPS3AddAccount] = self.__handle_ps3_add_account
        self.resolver_map[
            TXN.TransactionException
        ] = self.__handle_transaction_exception
        self.resolver_map[TXN.NuLookupUserInfo] = self.__handle_lookup_user_info
        self.resolver_map[TXN.NuSearchOwners] = self.__handle_search_owners
        self.resolver_map[TXN.GetTelemetryToken] = self.__handle_get_telemetry_token
        self.resolver_map[TXN.NuGetEntitlements] = self.__handle_get_entitlements
        self.resolver_map[
            TXN.NuGetEntitlementCount
        ] = self.__handle_get_entitlement_count
        self.resolver_map[TXN.NuEntitleGame] = self.__handle_entitle_game
        self.resolver_map[TXN.NuEntitleUser] = self.__handle_entitle_user
        self.resolver_map[TXN.NuGrantEntitlement] = self.__handle_grant_entitlement
        self.resolver_map[TXN.GetLockerURL] = self.__handle_get_locker_url

    def _get_resolver(self, txn):
        return self.resolver_map[TXN(txn)]

    def _get_creator(self, txn):
        return self.creator_map[TXN(txn)]

    def __get_locale(self):
        locale = self.connection.locale.value

        if settings.DEBUG:
            locale = "test"

        return locale

    def __get_tos(self):
        """Get TOS"""

        locale = self.__get_locale()

        tosFilename = "TOS.txt"

        if Path(
            os.path.join(self.tosPath, tosFilename.replace(".", f".{locale}."))
        ).exists():
            tosFilename = tosFilename.replace(".", f".{locale}.")

        finalPath = os.path.join(self.tosPath, tosFilename)

        with open(finalPath, "r", encoding="utf-8") as file:
            tos_content = file.read()

        with open(finalPath.replace(".txt", ".version"), "r", encoding="utf-8") as file:
            tos_version = file.read()

        return tos_content, tos_version

    async def __internal_login(self, data: Packet, allow_unentitled=False):
        """Internal login handler"""

        nuid = data.Get("nuid")
        password = data.Get("password")
        encryptedInfo = data.Get("encryptedInfo")

        if not ((nuid or password) or encryptedInfo):
            return TransactionError(TransactionError.Code.PARAMETERS_ERROR)

        if encryptedInfo:
            encryptedInfo = encryptedInfo.replace(self.ENCRYPTED_PREFIX, "")
            encryptedInfo = encryptedInfo.replace("-", "=").replace(
                "_", "="
            )  # Bring string into proper format again

            decryptedInfo = b64decode(encryptedInfo).decode("utf-8")

            if pos := decryptedInfo.find("\f"):
                nuid = decryptedInfo[:pos]
                password = decryptedInfo[pos + 1 :]

        umodel = get_user_model()

        if not await umodel.objects.user_exists(nuid):
            return TransactionError(TransactionError.Code.USER_NOT_FOUND)

        user = await sync_to_async(authenticate)(nuid=nuid, password=password)

        if not user:
            # Authentication failed, invalid password
            return TransactionError(TransactionError.Code.INVALID_PASSWORD)
        else:
            # Authentication successful, check if user logged to server account and if so check if client is server

            if user.isServerAccount and self.connection.clientType != ClientType.SERVER:
                return TransactionError(TransactionError.Code.USER_NOT_FOUND)

        await sync_to_async(update_last_login)(None, user)

        if not user.isServerAccount:
            # This is normal user, check whether user is entitled an accepted latest TOS
            tosVersion = data.Get("tosVersion")

            # User sent TOS version in request, that means he has accepted latest TOS
            if tosVersion:
                await umodel.objects.accept_tos(user, tosVersion)

            _, tos_version = self.__get_tos()

            if tos_version != user.tosVersion:
                return TransactionError(TransactionError.Code.TOS_OUT_OF_DATE)

            is_entitled = await Entitlement.objects.is_entitled_for_game(
                user, self.connection.clientString
            )

            if not is_entitled:
                if not allow_unentitled:
                    return TransactionError(TransactionError.Code.NOT_ENTITLED_TO_GAME)

            active_session = cache.get(f"userSession:{user.id}")

            if active_session:
                if active_session != self.connection.channel_name:
                    self.connection.logger.warning(
                        f"User {user.id} has active session, destroying it"
                    )

                    await self.connection.start_remote_transaction(
                        user.id, "fsys", "Goodbye", {"reason": 2}
                    )

            cache.set(
                f"userSession:{user.id}", self.connection.channel_name, timeout=None
            )

        encryptedLoginInfo = None

        if data.Get("returnEncryptedInfo"):
            # Store the user name and password as a base64 encoded string and put the chunk in front of it (so we have a similar format to the original one)
            loginInfo = f"{nuid}\f{password}"
            loginInfo = self.ENCRYPTED_PREFIX + b64encode(
                loginInfo.encode("utf-8")
            ).decode("utf-8")
            loginInfo = loginInfo.replace("=", "_")

            encryptedLoginInfo = loginInfo

        user_lkey = cache.get(f"userLoginKey:{user.id}")

        if not user_lkey:
            # Generate new login key, because user doesn't have one (or previous one expired)
            user_lkey = (
                "".join(
                    random.choice(string.ascii_letters + string.digits + "-_")
                    for _ in range(27)
                )
                + "."
            )

            # Save login key that never expires (we set expiration time when user logs out)
            cache.set(f"userLoginKey:{user.id}", user_lkey, timeout=None)
        else:
            # User already has login key, so we need to delete it from cache
            cache.touch(f"userLoginKey:{user.id}", timeout=None)

        self.connection.loggedUser = user
        self.connection.loggedUserKey = user_lkey

        await login(self.connection.scope, user)
        await database_sync_to_async(self.connection.scope["session"].save)()

        return user, user_lkey, encryptedLoginInfo

    async def __handle_login(self, data):
        response_data = await self.__internal_login(data)

        if isinstance(response_data, TransactionError):
            return response_data

        # Login successful
        # This packet is kind of interesting, because "successful" login (for game at least) doesn't require any data to be sent back (except for the TXN of course)
        # But, original server sends back nuid, lkey, profileId, userId and encryptedInfo (if requested)
        # So, we are doing the same
        #
        # The game will overwrite internally all data we will send below when user will log on to the persona
        # "profileId" and "userId" are the same (just like in original server responses)
        # Additionally "profileId" is not read by the game at all in NuLogin response

        user, user_lkey, encryptedLoginInfo = response_data
        response = Packet()
        response.Set("nuid", user.nuid)
        response.Set("lkey", user_lkey)
        response.Set("profileId", user.id)
        response.Set("userId", user.id)

        if encryptedLoginInfo:
            response.Set("encryptedLoginInfo", encryptedLoginInfo)

        return response

    async def __handle_add_account(self, data):
        """Add a new account"""

        errContainer = []
        umodel = get_user_model()

        # Check if nuid and password are provided
        nuid = data.Get("nuid")
        password = data.Get("password")

        if not nuid or not password:
            return TransactionError(TransactionError.Code.PARAMETERS_ERROR)

        try:
            validation = validate_email(nuid, check_deliverability=True)
            nuid = validation.email
        except EmailNotValidError as e:
            self.connection.logger.error(f"-- Not a valid email address. ({e})")

            errContainer.append(
                {
                    "fieldName": "email",
                    "fieldError": 6,
                    "value": "INVALID_VALUE",
                }
            )

            return TransactionError(
                TransactionError.Code.PARAMETERS_ERROR, errContainer
            )

        try:
            validate_password(password)
        except ValidationError as e:
            self.connection.logger.error(f"-- Not a valid password. ({e})")

            errContainer.append(
                {
                    "fieldName": "password",
                    "fieldError": 6,
                    "value": "INVALID_VALUE",
                }
            )

            return TransactionError(
                TransactionError.Code.PARAMETERS_ERROR, errContainer
            )

        dateOfBirth = date(
            data.Get("DOBYear"), data.Get("DOBMonth"), data.Get("DOBDay")
        )

        dateToday = date.today()

        age = (
            dateToday.year
            - dateOfBirth.year
            - ((dateToday.month, dateToday.day) < (dateOfBirth.month, dateOfBirth.day))
        )

        countryConfig = self.countryConfigOverrides.get(data.Get("country"), {})
        errContainer = []

        if countryConfig.get("registrationAgeLimit", 13) > age:
            # New user is too young to register
            errContainer.append(
                {
                    "fieldName": "dob",
                    "fieldError": 15,
                }
            )

            return TransactionError(
                TransactionError.Code.PARAMETERS_ERROR, errContainer
            )
        elif await umodel.objects.user_exists(nuid):
            # User already exists
            return TransactionError(TransactionError.Code.ALREADY_REGISTERED)

        # Create user
        await umodel.objects.create_user(
            nuid=nuid,
            password=password,
            globalOptin=data.Get("globalOptin"),
            thirdPartyOptin=data.Get("thirdPartyOptin"),
            parentalEmail=data.Get("parentalEmail"),
            dateOfBirth=dateOfBirth,
            firstName=data.Get("first_Name"),
            lastName=data.Get("last_Name"),
            gender=data.Get("gender"),
            address=data.Get("street"),
            address2=data.Get("street2"),
            city=data.Get("city"),
            state=data.Get("state"),
            zipCode=data.Get("zipCode"),
            country=data.Get("country"),
            language=data.Get("language"),
            tosVersion=data.Get("tosVersion"),
        )

        # Create response
        response = Packet()
        return response

    async def __handle_add_persona(self, data):
        """Add a new persona"""

        user = await get_user(self.connection.scope)
        name = data.Get("name")

        if not name:
            return TransactionError(TransactionError.Code.PARAMETERS_ERROR)

        success = await Persona.objects.create_persona(user, name)

        if not success:
            return TransactionError(TransactionError.Code.ALREADY_REGISTERED)

        response = Packet()
        return response

    async def __handle_disable_persona(self, data):
        """Remove a persona"""

        user = await get_user(self.connection.scope)
        name = data.Get("name")

        if not name:
            return TransactionError(TransactionError.Code.PARAMETERS_ERROR)

        success = await Persona.objects.delete_persona(user, name)

        if not success:
            return TransactionError(TransactionError.Code.TRANSACTION_DATA_NOT_FOUND)
        else:
            response = Packet()
            return response

    async def __handle_get_country_list(self, data):
        """Get the list of countries"""

        locale = self.__get_locale()

        countryList = []
        countryListFilename = "CountryList.csv"

        if Path(
            os.path.join(
                self.countryListPath, countryListFilename.replace(".", f".{locale}.")
            )
        ).exists():
            countryListFilename = countryListFilename.replace(".", f".{locale}.")

        with open(os.path.join(self.countryListPath, "overrides.json"), "r", encoding="utf-8") as file:
            overrides = json.load(file)

            if settings.DEBUG:
                overrides["DBG"] = {
                    "allowEmailsDefaultValue": 0,
                    "parentalControlAgeLimit": 18,
                    "registrationAgeLimit": 13,
                }

            self.countryConfigOverrides = overrides

        with open(os.path.join(self.countryListPath, countryListFilename), "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                iso_code = row["ISOCode"]

                if iso_code in overrides:
                    for key in overrides[iso_code]:
                        row[key] = overrides[iso_code][key]

                self.validCountryCodes.append(iso_code)
                countryList.append(row)

        # This is simple packet, example country looks like this:
        # {
        #     "ISOCode": "DBG",
        #     "description": "Example Country",
        # }
        #
        # ISOCode is the country code, description is the country name (visible in game)
        # ISOCode is usually 2 letters, but can be up to 3 letters (like DBG above)
        #
        # Each country can specify optional fields:
        # allowEmailsDefaultValue: 0 or 1 (default is 0)
        # parentalControlAgeLimit: int (default is 18)
        # registrationAgeLimit: int (default is 13)
        #

        response = Packet()
        response.Set("countryList", countryList)

        return response

    async def __handle_get_tos(self, data):
        """Get the Terms of Service"""

        selected_country_code = data.Get("countryCode")

        if (
            selected_country_code is not None
            and selected_country_code not in self.validCountryCodes
        ):
            raise ValueError(
                f"{selected_country_code} is not valid country code for NuGetTos."
            )

        # In theory everything shows that here we should send the TOS for the selected country code.
        # However, this doesn't seem to be the case. Original server sends the same TOS for every country code, only (game) language seems to have any effect.

        tos_content, tos_version = self.__get_tos()

        response = Packet()
        response.Set("tos", tos_content)
        response.Set("version", tos_version)

        return response

    async def __handle_create_encrypted_token(self, data):
        """Create an encrypted token (?)"""

        # Is this ever called from the client?

        # Transaction content is:
        # {
        #    "TXN": "NuCreateEncryptedToken",
        #    "expires": integer,
        #    "attributes": [
        #        {
        #           "name": string,
        #           "value": string
        #        }
        #     ]
        # }

        # Couldn't find any response for this transaction in my poor RE effort
        raise NotImplementedError("NuCreateEncryptedToken is not implemented")

    async def __handle_suggest_personas(self, data):
        """Suggest personas"""

        # Is this ever called from the client?

        # Transaction content is:
        # {
        #    "TXN": "NuSuggestPersonas",
        #    "name": string
        #    "maxSuggestions": integer
        #    "keywords": [strings array]
        # }
        #
        # Response is:
        # {
        #    "TXN": "NuSuggestPersonas",
        #    "names": [strings array]
        # }

        # Not sure what "name" is here, but let's say it's the currently logged persona name
        user = await get_user(self.connection.scope)

        keywords = data.Get("keywords")
        max_suggestions = data.Get("maxSuggestions")

        if not keywords or not max_suggestions:
            return TransactionError(TransactionError.Code.PARAMETERS_ERROR)

        personas = await Persona.objects.suggest_personas(
            user, keywords, max_suggestions
        )

        response = Packet()
        response.Set("names", personas)

        return response

    async def __handle_login_persona(self, data):
        """Login a persona"""

        user = await get_user(self.connection.scope)
        name = data.Get("name")

        if not name:
            return TransactionError(TransactionError.Code.PARAMETERS_ERROR)

        persona = await Persona.objects.get_persona(user, name)

        if persona is None:
            return TransactionError(TransactionError.Code.USER_NOT_FOUND)

        persona_lkey = cache.get(f"personaLoginKey:{user.id}")

        if not persona_lkey:
            # Generate new login key, because user doesn't have one (or previous one expired)
            persona_lkey = (
                "".join(
                    random.choice(string.ascii_letters + string.digits + "-_")
                    for _ in range(27)
                )
                + "."
            )

            # Save login key that never expires (we set expiration time when user logs out)
            cache.set(f"personaLoginKey:{user.id}", persona_lkey, timeout=None)
            cache.set(f"lkeyMap:{persona_lkey}", persona.id, timeout=None)
        else:
            # User already has login key, so we need to delete it from cache
            cache.touch(f"personaLoginKey:{user.id}", timeout=None)
            cache.touch(f"lkeyMap:{persona_lkey}", timeout=None)

        self.connection.loggedPersona = persona
        self.connection.loggedPersonaKey = persona_lkey

        response = Packet()
        response.Set("lkey", persona_lkey)
        response.Set(
            "profileId", persona.id
        )  # Again, game doesn't seem to care about this
        response.Set("userId", user.id)

        return response

    async def __handle_update_password(self, data):
        """Update a user's password"""

        user = await get_user(self.connection.scope)

        data.Set("nuid", user.nuid)  # Add nuid so we can test login
        new_password = data.Get("newPassword")

        login_data = await self.__internal_login(data)

        if isinstance(login_data, TransactionError):
            return login_data

        try:
            validate_password(new_password)
        except ValidationError as e:
            self.connection.logger.error(f"-- Not a valid password. ({e})")

            errContainer = [
                {
                    "fieldName": "password",
                    "fieldError": 6,
                    "value": "INVALID_VALUE",
                }
            ]

            return TransactionError(
                TransactionError.Code.PARAMETERS_ERROR, errContainer
            )

        user.set_password(new_password)
        data.Set("password", new_password)  # Overwrite password with new password

        login_data = await self.__internal_login(data)

        if isinstance(login_data, TransactionError):
            return login_data

        user, _, encryptedLoginInfo = login_data

        response = Packet()

        if encryptedLoginInfo:
            response.Set("encryptedLoginInfo", encryptedLoginInfo)

        return response

    async def __handle_get_account(self, data, nuid=None):
        """Get a user's account information"""

        if nuid is None:
            user = await get_user(self.connection.scope)
        else:
            umodel = get_user_model()
            user = await umodel.objects.get_user_by_nuid(nuid)

        response = Packet()
        response.Set("nuid", user.nuid)

        if user.parentalEmail:
            response.Set("parentalEmail", user.parentalEmail)

        if user.firstName:
            response.Set("firstName", user.firstName)

        if user.lastName:
            response.Set("lastName", user.lastName)

        if user.address:
            response.Set("street", user.address)

        if user.address2:
            response.Set("street2", user.address2)

        if user.city:
            response.Set("city", user.city)

        if user.state:
            response.Set("state", user.state)

        if user.zipCode:
            response.Set("zip", user.zipCode)

        if user.country:
            response.Set("country", user.country)

        if user.language:
            response.Set("language", user.language)

        if user.gender:
            response.Set("gender", user.gender)

        response.Set("userId", user.id)

        if user.dateOfBirth:
            response.Set("dOBMonth", user.dateOfBirth.month)
            response.Set("dOBDay", user.dateOfBirth.day)
            response.Set("dOBYear", user.dateOfBirth.year)

        response.Set("globalCommOptin", user.globalOptin)
        response.Set("thirdPartyMailFlag", user.thirdPartyOptin)

        return response

    async def __handle_get_account_by_nuid(self, data):
        """Get a user's account information by nuid"""

        nuid = data.Get("nuid")

        if not nuid:
            return TransactionError(TransactionError.Code.PARAMETERS_ERROR)

        # Should we allow to get account info of other users? This seems what this transaction is supposed to do
        # But it looks like security risk to me, so if nuid is not equal to current user's nuid, we return error
        # Else, we return account info of current user

        user = await get_user(self.connection.scope)

        if nuid != user.nuid:
            return TransactionError(TransactionError.Code.TRANSACTION_DATA_NOT_FOUND)

        return await self.__handle_get_account(data, nuid)

    async def __handle_get_account_by_ps3_ticket(self, data):
        """Get a user's account information by ps3 ticket"""

        # {
        #     "ticket": binary data,
        # }

        return NotImplementedError(
            "NuGetAccountByPs3Ticket is PS3 specific transaction, it's not supported by this server implementation"
        )

    async def __handle_get_personas(self, data):
        """Get the list of personas"""

        user = await get_user(self.connection.scope)
        personas = await Persona.objects.list_personas(user)

        response = Packet()
        response.Set("personas", personas)

        return response

    async def __handle_update_account(self, data):
        """Update a user's account information"""

        user = await get_user(self.connection.scope)

        nuid = data.Get("nuid")
        password = data.Get("password")
        globalOptin = data.Get("globalOptin")
        thirdPartyOptin = data.Get("thirdPartyOptin")

        if (
            nuid is None
            or password is None
            or globalOptin is None
            or thirdPartyOptin is None
        ):
            return TransactionError(TransactionError.Code.PARAMETERS_ERROR)

        user.nuid = nuid
        user.set_password(password)
        user.globalOptin = globalOptin
        user.thirdPartyOptin = thirdPartyOptin

        if data.Get("parentalEmail"):
            user.parentalEmail = data.Get("parentalEmail")

        if data.Get("DOBDay"):
            user.dateOfBirth = date(
                data.Get("DOBYear"), data.Get("DOBMonth"), data.Get("DOBDay")
            )

        if data.Get("first_Name"):
            user.firstName = data.Get("first_Name")

        if data.Get("last_Name"):
            user.lastName = data.Get("last_Name")

        if data.Get("gender"):
            user.gender = data.Get("gender")

        if data.Get("street"):
            user.address = data.Get("street")

        if data.Get("street2"):
            user.address2 = data.Get("street2")

        if data.Get("city"):
            user.city = data.Get("city")

        if data.Get("state"):
            user.state = data.Get("state")

        if data.Get("zipCode"):
            user.zipCode = data.Get("zipCode")

        if data.Get("country"):
            user.country = data.Get("country")

        if data.Get("language"):
            user.language = data.Get("language")

        await user.save()
        return Packet()

    async def __handle_gamespy_preauth(self, data):
        """Gamespy preauth"""

        # {}

        raise NotImplementedError(
            "NuGamespyPreauth is Gamespy specific transaction, it's not supported by this server implementation"
        )

    async def __handle_xbl360_login(self, data):
        """Xbox (Live) 360 login"""

        # {
        #    "macAddr": string,
        #    "consoleId": "012345678", # Seems to be set to "012345678" in all requests, at least in server code
        # }
        # Optional "tosVersion" parameter (same as in NuLogin)

        raise NotImplementedError(
            "NuXbl360Login is Xbox 360 specific transaction, it's not supported by this server implementation"
        )

    async def __handle_xbl360_add_account(self, data):
        """Xbox (Live) 360 add account"""

        # Seems to be identical to NuAddAccount
        return await self.__handle_add_account(data)

    async def __handle_ps3_login(self, data):
        """Playstation 3 login"""

        # {
        #     "ticket": binary data,
        #     "macAddr": string,
        #     "consoleId": "012345678", # Seems to be set to "012345678" in all requests, at least in server code
        # }
        # Optional "tosVersion" parameter (same as in NuLogin)

        raise NotImplementedError(
            "NuPs3Login is PS3 specific transaction, it's not supported by this server implementation"
        )

    async def __handle_ps3_add_account(self, data):
        """Playstation 3 add account"""

        # Seems to be identical to NuAddAccount
        return await self.__handle_add_account(data)

    async def __handle_transaction_exception(self, data):
        """Transaction exception"""

        raise NotImplementedError(
            "TransactionException is not supported by this server implementation"
        )

    async def __handle_lookup_user_info(self, data):
        """Lookup user info"""

        users_to_lookup = data.Get("userInfo")

        if not users_to_lookup:
            return TransactionError(TransactionError.Code.PARAMETERS_ERROR)

        users_info = []

        for userInfo in users_to_lookup:
            user_info = await Persona.objects.get_user_info(userInfo.get("userName"))

            if not user_info:
                return TransactionError(
                    TransactionError.Code.TRANSACTION_DATA_NOT_FOUND
                )

            users_info.append(user_info)

        response = Packet()
        response.Set("userInfo", users_info)

        return response

    async def __handle_search_owners(self, data):
        """Friend search"""

        user = await get_user(self.connection.scope)

        screenName = data.Get("screenName")

        if not screenName:
            return TransactionError(TransactionError.Code.PARAMETERS_ERROR)

        owners = await Persona.objects.search_personas(user, screenName)

        response = Packet()
        response.Set("users", owners)
        response.Set("nameSpaceId", "battlefield")

        return response

    async def __handle_get_telemetry_token(self, data):
        """Get telemetry token"""
        token = "0.0.0.0,9946,"

        locale = str(self.connection.locale.value).replace("_", "")

        if len(locale) == 2:
            locale = locale + locale.upper()

        token += locale

        # Token also have some encoded data (for telemetry)
        # We don't need it, so we just fill it with zeros

        token += (
            "\0" * 104
        )  # Token length is 104 bytes (at least that's what I've seen in original server)
        token = legacy_b64encode(token).decode("utf-8")

        response = Packet()
        response.Set("telemetryToken", token)
        response.Set(
            "enabled",
            "CA,MX,PR,US,VI,AD,AF,AG,AI,AL,AM,AN,AO,AQ,AR,AS,AW,AX,AZ,BA,BB,BD,BF,BH,BI,BJ,BM,BN,BO,BR,BS,BT,BV,BW,BY,BZ,CC,CD,CF,CG,CI,CK,CL,CM,CN,CO,CR,CU,CV,CX,DJ,DM,DO,DZ,EC,EG,EH,ER,ET,FJ,FK,FM,FO,GA,GD,GE,GF,GG,GH,GI,GL,GM,GN,GP,GQ,GS,GT,GU,GW,GY,HM,HN,HT,ID,IL,IM,IN,IO,IQ,IR,IS,JE,JM,JO,KE,KG,KH,KI,KM,KN,KP,KR,KW,KY,KZ,LA,LB,LC,LI,LK,LR,LS,LY,MA,MC,MD,ME,MG,MH,ML,MM,MN,MO,MP,MQ,MR,MS,MU,MV,MW,MY,MZ,NA,NC,NE,NF,NG,NI,NP,NR,NU,OM,PA,PE,PF,PG,PH,PK,PM,PN,PS,PW,PY,QA,RE,RS,RW,SA,SB,SC,clntSock,SG,SH,SJ,SL,SM,SN,SO,SR,ST,SV,SY,SZ,TC,TD,TF,TG,TH,TJ,TK,TL,TM,TN,TO,TT,TV,TZ,UA,UG,UM,UY,UZ,VA,VC,VE,VG,VN,VU,WF,WS,YE,YT,ZM,ZW,ZZ",
        )
        response.Set("filters", "")
        response.Set("disabled", "")

        return response

    async def __handle_get_entitlements(self, data):
        """Get the list of entitlements"""

        groupName = data.Get("groupName")
        entitlementTag = data.Get("entitlementTag")

        if self.connection.clientType == ClientType.SERVER:
            uid = data.Get("masterUserId")
            user = await Account.objects.get_user_by_id(uid)
        else:
            user = await get_user(self.connection.scope)

        entitlements = await Entitlement.objects.list_entitlements(
            user, groupName=groupName, entitlementTag=entitlementTag
        )

        response = Packet()
        response.Set("entitlements", entitlements)

        return response

    async def __handle_get_entitlement_count(self, data):
        """Get the count of entitlements"""

        user = await get_user(self.connection.scope)

        filter_data = {
            "entitlementId": data.Get("entitlementId"),
            "entitlementTag": data.Get("entitlementTag"),
            "masterUserId": data.Get("masterUserId"),
            "userId": data.Get("userId"),
            "global": data.Get("global"),
            "status": data.Get("status"),
            "groupName": data.Get("groupName"),
            "productCatalog": data.Get("productCatalog"),
            "productId": data.Get("productId"),
            "grantStartDate": data.Get("grantStartDate"),
            "grantEndDate": data.Get("grantEndDate"),
            "projectId": data.Get("projectId"),
            "entitlementType": data.Get("entitlementType"),
            "devicePhysicalId": data.Get("devicePhysicalId"),
        }

        count = await Entitlement.objects.count_entitlements(user, filter_data)

        response = Packet()
        response.Set("entitlementCount", count)

        return response

    async def __handle_entitle_game(self, data):
        """Entitle game (user enters game key while login)"""

        response_data = await self.__internal_login(data, allow_unentitled=True)

        if isinstance(response_data, TransactionError):
            return response_data

        user, user_lkey, encryptedLoginInfo = response_data

        key = data.Get("key")
        activation_result, _ = await Entitlement.objects.activate_key(user, key)

        if activation_result == ActivationResult.INVALID_KEY:
            return TransactionError(TransactionError.Code.CODE_NOT_FOUND)
        elif activation_result == ActivationResult.ALREADY_USED:
            return TransactionError(TransactionError.Code.CODE_ALREADY_USED)

        response = Packet()
        response.Set("nuid", user.nuid)
        response.Set("lkey", user_lkey)
        response.Set("profileId", user.id)
        response.Set("userId", user.id)

        if encryptedLoginInfo:
            response.Set("encryptedLoginInfo", encryptedLoginInfo)

        return response

    async def __handle_entitle_user(self, data):
        """User enters key"""

        user = await get_user(self.connection.scope)
        key = data.Get("key")

        activation_result, activated_products = await Entitlement.objects.activate_key(
            user, key
        )

        if activation_result == ActivationResult.INVALID_KEY:
            return TransactionError(TransactionError.Code.CODE_NOT_FOUND)
        elif activation_result == ActivationResult.ALREADY_USED:
            return TransactionError(TransactionError.Code.CODE_ALREADY_USED)

        response = Packet()
        response.Set("productList", activated_products)

        return response

    async def __handle_grant_entitlement(self, data):
        """Grant entitlement"""

        # Is this ever called from client?

        # Input (all optional):
        # {
        #     "entitlementTag": "string",
        #     "groupName": "string",
        #     "productCatalog": "string",
        #     "productId": "string",
        #     "grantStartDate": "string",
        #     "grantEndDate": "string",
        #     "entitlementType": "string",
        #     "devicePhysicalId": "string",
        #     "deviceType": "string",
        #     "gamerTag": "string",
        #     "masterId": "string",
        #     "personaId": "string",
        # }

        if self.connection.clientType != ClientType.SERVER:
            return TransactionError(TransactionError.Code.SESSION_NOT_AUTHORIZED)

        user = await get_user(self.connection.scope)

        await Entitlement.objects.add_entitlement(
            user,
            tag=data.Get("entitlementTag"),
            grantDate=data.Get("grantStartDate"),
            terminationDate=data.Get("grantEndDate"),
            groupName=data.Get("groupName"),
            productId=data.Get("productId"),
        )

        return Packet()

    async def __handle_get_locker_url(self, data):
        """Get locker URL"""

        # Original server URL is http://bfbc2.gos.ea.com/easo/fileupload/locker2.jsp
        # I modified it so it'll target "fileupload_locker" view in "easo" app
        # See: easo/urls.py and easo/views.py

        response = Packet()
        response.Set("URL", f"http://bfbc2.gos.ea.com/easo/fileupload/locker2.jsp")

        return response
