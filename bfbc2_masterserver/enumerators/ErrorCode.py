from enum import Enum


class ErrorCode(Enum):
    """
    The ErrorCode class is a subclass of the Enum class from the enum module.

    This class represents various error codes that can be returned by the system. Each error code is represented by a unique integer value.

    Attributes:
        SESSION_NOT_AUTHORIZED (int): The session is not authorized.
        PARAMETERS_ERROR (int): There is an error with the parameters.
        NOT_INITIALIZED (int): The system is not initialized.
        SYSTEM_ERROR (int): There is a system error.
        USER_NOT_FOUND (int): The user was not found.
        TRANSACTION_DATA_NOT_FOUND (int): The transaction data was not found.
        NOT_ENTITLED_TO_GAME (int): The user is not entitled to the game.
        INVALID_PASSWORD (int): The password is invalid.
        ALREADY_REGISTERED (int): The user is already registered.
        CODE_ALREADY_USED (int): The code has already been used.
        CODE_NOT_FOUND (int): The code was not found.
        TOS_OUT_OF_DATE (int): The terms of service are out of date.
        RECORD_NOT_FOUND (int): The record was not found.
    """

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
