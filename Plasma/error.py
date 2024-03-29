from enum import Enum


class TransactionSkip:
    pass


class TransactionException(Exception):
    pass


class TransactionError:
    class Code(Enum):
        SESSION_NOT_AUTHORIZED = 20
        PARAMETERS_ERROR = 21
        NOT_INITIALIZED = 22
        SYSTEM_ERROR = 99
        USER_NOT_FOUND = 101
        TRANSACTION_DATA_NOT_FOUND = 104
        NOT_ENTITLED_TO_GAME = 120
        INVALID_PASSWORD = 122
        ALREADY_REGISTERED = 160
        CODE_ALREADY_USED = 180
        CODE_NOT_FOUND = 181
        TOS_OUT_OF_DATE = 260
        RECORD_NOT_FOUND = 5000

    errorCode: int
    localizedMessage: str
    errorContainer: dict

    def __init__(self, code: Code, container: dict = {}):
        self.errorCode = code.value
        self.localizedMessage = self.__get_localized_message(code)
        self.errorContainer = container

    def __get_localized_message(self, code: Code):
        match code:
            case self.Code.PARAMETERS_ERROR:
                return "The required parameters for this call are missing or invalid"
            case self.Code.NOT_INITIALIZED:
                return "The client did not send up the initial hello packet"
            case self.Code.ALREADY_REGISTERED:
                return "That account name is already taken"
            case self.Code.INVALID_PASSWORD:
                return "The password the user specified is incorrect"
            case self.Code.TOS_OUT_OF_DATE:
                return "The TOS Content is out of date."
            case self.Code.NOT_ENTITLED_TO_GAME:
                return "The user is not entitled to access this game"
            case self.Code.CODE_ALREADY_USED:
                return "That code has already been used"
            case self.Code.USER_NOT_FOUND:
                return "The user was not found"
            case self.Code.SYSTEM_ERROR:
                return "System Error"
            case self.Code.CODE_NOT_FOUND:
                return "The code is not valid for registering this game"
            case self.Code.SESSION_NOT_AUTHORIZED:
                return "Session Not Authorized"
            case self.Code.TRANSACTION_DATA_NOT_FOUND:
                return "The data necessary for this transaction was not found"
            case self.Code.RECORD_NOT_FOUND:
                return "Record not found"

        return "Unknown error"
