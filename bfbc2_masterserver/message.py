import logging
import re
from datetime import datetime
from enum import Enum
from typing import Any, MutableMapping
from urllib.parse import quote, unquote

from pydantic import SecretStr

# Define constants for the offsets and lengths of the service, kind, and length fields in the message
SERVICE_OFFSET, SERVICE_LENGTH = (0x0, 0x4)
KIND_OFFSET, KIND_LENGTH = (SERVICE_OFFSET + SERVICE_LENGTH, 0x4)
LENGTH_OFFSET, LENGTH_LENGTH = (KIND_OFFSET + KIND_LENGTH, 0x4)
HEADER_LENGTH = 0xC

logger = logging.getLogger(__name__)


# Define the Message class
class Message:
    """
    The Message class represents a single message in a communication system.

    Attributes:
        service (str): The service associated with the message.
        type (int): The type of the message.
        data (dict): The data contained in the message.
        __length (int): The length of the message. This is a private attribute.

    Methods:
        __init__(self, **kwargs): The constructor for the Message class.
        __str__(self): Returns a string representation of the Message object.
        compile(self): Compiles the message into a packet.
    """

    service: str
    type: int
    data: Any = {}

    fragmented: bool = False

    length: int = 0

    def __init__(self, **kwargs):
        """
        The constructor for the Message class.

        If raw_data is provided in kwargs, the message is created from bytes (used to parse incoming messages).
        Otherwise, the message is created from arguments (used to create outgoing messages).

        Parameters:
            kwargs: Arbitrary keyword arguments. Expected keys are "raw_data", "service", "type", and "data".
        """

        raw_data = kwargs.get("raw_data", None)

        if raw_data is not None:
            # Create message from bytes (used to parse incoming messages)
            self.data.clear()  # Clear the data dictionary before parsing
            self.__parse_raw_data(raw_data)
        else:
            # Create message from arguments (used to create outgoing messages)
            self.service = kwargs.get("service", None)
            self.type = kwargs.get("type", None)
            data = kwargs.get("data", {})

            if isinstance(data, str):
                self.__read_data(data.encode("utf-8"), 0)
            else:
                self.data = data

    def __str__(self) -> str:
        """
        Returns a string representation of the Message object.

        The string includes the service, type (in hexadecimal), length (in bytes), and data.

        Returns:
            str: A string representation of the Message object.
        """

        length: int = len(self.compile()) if self.length == 0 else self.length
        return f"{self.service} {hex(self.type)} ({length} bytes) {self.data}"

    # Method to compile the message into a packet
    def compile(self):
        """
        Compile the message into a packet.

        The packet starts with the service encoded as bytes, followed by the type as a 4-byte integer.
        The data is then converted to a string and its length, along with the length of the header, is added as a 4-byte integer.
        Finally, the data is added to the packet encoded as bytes.

        Returns:
            bytes: The compiled packet.
        """

        # Start with the service encoded as bytes
        temp_packet: bytes = self.service.encode()

        # Add the type as a 4-byte integer
        temp_packet += int.to_bytes(self.type, 4, byteorder="big")

        # Convert the data to a string
        temp_data = self.__convert_data()

        # Add the length of the header and data as a 4-byte integer
        temp_packet += int.to_bytes(HEADER_LENGTH + len(temp_data), 4, byteorder="big")

        # Add the data encoded as bytes
        temp_packet += temp_data.encode()

        # Return the compiled packet
        return temp_packet

    # Method to parse raw data into a message
    def __parse_raw_data(self, raw_data: bytes) -> None:
        received_length: int = len(raw_data)

        # If the length of the raw data is less than the length of the header, raise an exception
        if received_length < HEADER_LENGTH:
            raise Exception(
                f"Packet is too short to be valid (Expected at least 12 bytes, got {received_length})"
            )

        # Extract the service from the raw data
        self.service = raw_data[
            SERVICE_OFFSET : SERVICE_OFFSET + SERVICE_LENGTH
        ].decode("utf-8")

        # Extract the type from the raw data
        self.type = int.from_bytes(
            raw_data[KIND_OFFSET : KIND_OFFSET + KIND_LENGTH], byteorder="big"
        )

        # Extract the length from the raw data
        self.length = int.from_bytes(
            raw_data[LENGTH_OFFSET : LENGTH_OFFSET + LENGTH_LENGTH], byteorder="big"
        )

        # If the received length does not match the extracted length, raise an exception
        if received_length < self.length:
            raise Exception(
                f"Packet length does not match (Received: {received_length}, Expected: {self.length})"
            )
        elif received_length > self.length:
            self.fragmented = True
            return

        # Read the data from the raw data
        self.__read_data(raw_data, HEADER_LENGTH)

    # Method to read data from raw data
    def __read_data(self, raw_data, offset) -> None:
        # Split the raw data into lines
        transaction_data = raw_data[offset:].decode("utf-8").split("\n")

        # If transaction data is null terminated, remove null terminator before parsing
        if transaction_data[-1] == "\0":
            transaction_data = transaction_data[:-1]

        # Make key-value pairs from the transaction data
        tokens = self.__make_key_value_pairs(transaction_data)
        tree = {}

        # Add each key-value pair to the tree
        for key, value in tokens:
            tree = self.__add_branch(tree, key.split("."), self.__parse_value(value))

        # Parse the transaction data
        self.__parse_transaction_data(tree)

    # Method to make key-value pairs from transaction data
    def __make_key_value_pairs(self, transaction_data):
        final = []

        # For each line in the transaction data
        for data in transaction_data:
            # Split the line into a key-value pair
            pair = data.split("=", 1)

            # If the pair is not valid, ignore it
            if len(pair) != 2:
                continue

            # Add the valid pair to the final list
            final.append(pair)

        # Return the final list of key-value pairs
        return final

    # Method to add a branch to the tree
    def __add_branch(self, tree, vector, value):
        key = vector[0]  # Get the first element of the vector as the key

        # If the vector has only one element, assign the value to the key in the tree
        # Otherwise, recursively add a branch to the tree
        tree[key] = (
            value
            if len(vector) == 1
            else self.__add_branch(tree[key] if key in tree else {}, vector[1:], value)
        )

        # Return the updated tree
        return tree

    # Method to parse transaction data
    def __parse_transaction_data(self, data):
        def handle_nested_arrays(value):
            if isinstance(value, dict) and "[]" in value:
                length = value.pop("[]")
                temp_array = []

                for item in value:
                    temp_array.append(handle_nested_arrays(value[item]))

                if length != len(temp_array):
                    logger.warning(
                        f"Array length does not match (Expected: {length}, Got: {len(temp_array)})"
                    )

                return temp_array
            elif isinstance(value, dict):
                return {k: handle_nested_arrays(v) for k, v in value.items()}
            else:
                return value

        for key, value in data.items():
            self.data[key] = handle_nested_arrays(value)

    # Method to parse a value from a string
    def __parse_value(self, value: str) -> int | str:
        # If the value is a digit, return it as an integer
        # Otherwise, return the unquoted value
        if value.isdigit():
            return int(value)
        else:
            return unquote(value)

    # Method to encode a string
    def __encode_string(self, value) -> str:
        # If the value is a datetime object, format it as a string and quote it
        # Otherwise, convert the value to a string and quote it
        if isinstance(value, datetime):
            temp_value: str = quote(value.strftime("%b-%d-%Y %H:%M:%S UTC"))
        elif isinstance(value, SecretStr):
            temp_value: str = quote(value.get_secret_value())
        else:
            temp_value: str = quote(str(value))

        # Replace "%20" with a space in the quoted string
        temp_value = temp_value.replace("%20", " ")

        # If the quoted string contains a space, enclose it in quotes
        if temp_value.find(" ") != -1:
            temp_value = '"' + temp_value + '"'

        # Convert all uppercase hexadecimal characters in the quoted string to lowercase
        return re.sub(r"%[0-9A-F]{2}", lambda pat: pat.group(0).lower(), temp_value)

    # Function to flatten a nested dictionary
    def __flatten(self, d, parent_key="", sep="."):
        items = []  # List to store the flattened key-value pairs

        # Iterate over each key-value pair in the dictionary
        for k, v in d.items():
            # Create a new key by appending the current key to the parent key
            new_key = parent_key + sep + str(k) if parent_key else k

            # If the value is a dictionary, recursively flatten it
            if isinstance(v, MutableMapping):
                items.extend(self.__flatten(v, new_key, sep=sep).items())
            else:
                # If the value is not a dictionary, add the key-value pair to the items list
                items.append((new_key, v))

        # Return a new dictionary created from the items list
        return dict(items)

    # Method to convert the data to a string
    def __convert_data(self):
        final_data = ""

        if isinstance(self.data, dict):
            temp_data = self.__flatten(self.data)
        else:
            temp_data = self.__flatten(
                self.data.model_dump(exclude_none=True, by_alias=True)
            )

        # For each key-value pair in the flattened data
        for key in temp_data:
            value = temp_data[key]  # Get the value

            # If the value is an Enum, add the key and value to the final data
            if isinstance(value, Enum):
                final_data += key + "=" + str(value.value) + "\n"
            # If the value is a list, add the key and length of the list to the final data, and process the list
            elif isinstance(value, list):
                final_data += key + ".[]=" + str(len(value)) + "\n"
                final_data += self.__process_dict(key, value)
            # Otherwise, add the key and encoded value to the final data
            else:
                final_data += "%s=%s\n" % (key, self.__encode_string(value))

        # EA uses the final NULL delimiter so we set the last char from the data to NULL
        final_data = final_data[:-1]  # Remove last new line char
        final_data += "\0"  # Append NULL

        return final_data

    # Method to process a dictionary
    def __process_dict(self, key, values, skip_idx=False):
        processed_dict = ""

        # For each value in the list of values
        for x in range(len(values)):
            # If the value is a dictionary
            if isinstance(values[x], dict):
                # For each key-value pair in the dictionary
                for y in values[x]:
                    # If the value is a list
                    if isinstance(values[x][y], list):
                        # Add the key and length of the list to the processed dictionary
                        processed_dict += (
                            f"{key}.{x}.{y}" + ".[]=" + str(len(values[x][y])) + "\n"
                        )

                        # Process the list
                        processed_dict += self.__process_dict(
                            f"{key}.{x}.{y}", values[x][y]
                        )
                    # If the value is a dictionary
                    elif isinstance(values[x][y], dict):
                        # Process the dictionary
                        processed_dict += self.__process_dict(
                            f"{key}.{x}.{y}", [values[x][y]], True
                        )
                    else:
                        # If skip_idx is True, add the key and encoded value to the processed dictionary
                        # Otherwise, add the key, index, and encoded value to the processed dictionary
                        if skip_idx:
                            processed_dict += (
                                key
                                + "."
                                + y
                                + "="
                                + self.__encode_string(values[x][y])
                                + "\n"
                            )
                        else:
                            processed_dict += (
                                key
                                + "."
                                + str(x)
                                + "."
                                + y
                                + "="
                                + self.__encode_string(values[x][y])
                                + "\n"
                            )
            else:
                # If the value is a list
                if isinstance(values[x], list):
                    # Add the key and length of the list to the processed dictionary
                    processed_dict += f"{key}.{x}" + ".[]=" + str(len(values[x])) + "\n"
                    # Process the list
                    processed_dict += self.__process_dict(f"{key}.{x}", values[x])
                # If the value is a dictionary
                elif isinstance(values[x], dict):
                    # Process the dictionary
                    processed_dict += self.__process_dict(
                        f"{key}.{x}", [values[x]], True
                    )
                else:
                    # If skip_idx is True, add the key and encoded value to the processed dictionary
                    # Otherwise, add the key, index, and encoded value to the processed dictionary
                    if skip_idx:
                        processed_dict += (
                            key + "=" + self.__encode_string(values[x]) + "\n"
                        )
                    else:
                        processed_dict += (
                            key
                            + "."
                            + str(x)
                            + "="
                            + self.__encode_string(values[x])
                            + "\n"
                        )

        # Return the processed dictionary
        return processed_dict
