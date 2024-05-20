from bfbc2_masterserver.enumerators.ErrorCode import ErrorCode


class TransactionSkip:
    """
    The TransactionSkip class is used to indicate that a transaction should be skipped (no response).
    """


# Exception class for transaction errors
class TransactionException(Exception):
    """
    The TransactionException class is a subclass of the Exception class.

    This class is used to represent exceptions that occur during transactions.
    """


class TransactionError:
    """
    The TransactionError class is used to represent a transaction error.

    Attributes:
        errorCode (int): The error code associated with the error.
        localizedMessage (str): The localized message for the error.
        errorContainer (dict): The container for additional error data.

    Methods:
        __init__(self, code: ErrorCode, container: dict = {}): Initializes a new instance of the TransactionError class.
        __get_localized_message(self, code: ErrorCode): Returns the localized message for a given error code.
    """

    errorCode: int
    localizedMessage: str
    errorContainer: list

    def __init__(self, code: ErrorCode, container: list = []):
        self.errorCode = code.value
        self.localizedMessage = self.__get_localized_message(code)
        self.errorContainer = container

    def __get_localized_message(self, code: ErrorCode):
        match code:
            case ErrorCode.PARAMETERS_ERROR:
                return "The required parameters for this call are missing or invalid"
            case ErrorCode.NOT_INITIALIZED:
                return "The client did not send up the initial hello packet"
            case ErrorCode.ALREADY_REGISTERED:
                return "That account name is already taken"
            case ErrorCode.INVALID_PASSWORD:
                return "The password the user specified is incorrect"
            case ErrorCode.TOS_OUT_OF_DATE:
                return "The TOS Content is out of date."
            case ErrorCode.NOT_ENTITLED_TO_GAME:
                return "The user is not entitled to access this game"
            case ErrorCode.CODE_ALREADY_USED:
                return "That code has already been used"
            case ErrorCode.USER_NOT_FOUND:
                return "The user was not found"
            case ErrorCode.SYSTEM_ERROR:
                return "System Error"
            case ErrorCode.CODE_NOT_FOUND:
                return "The code is not valid for registering this game"
            case ErrorCode.SESSION_NOT_AUTHORIZED:
                return "Session Not Authorized"
            case ErrorCode.TRANSACTION_DATA_NOT_FOUND:
                return "The data necessary for this transaction was not found"
            case ErrorCode.RECORD_NOT_FOUND:
                return "Record not found"

        return "Unknown error"
