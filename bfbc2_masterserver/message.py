import logging
import re
from datetime import datetime
from enum import Enum
from urllib.parse import quote, unquote

from bfbc2_masterserver.helpers import flatten

SERVICE_OFFSET, SERVICE_LENGTH = (0x0, 0x4)
KIND_OFFSET, KIND_LENGTH = (SERVICE_OFFSET + SERVICE_LENGTH, 0x4)
LENGTH_OFFSET, LENGTH_LENGTH = (KIND_OFFSET + KIND_LENGTH, 0x4)
HEADER_LENGTH = 0xC

logger = logging.getLogger(__name__)


class Message:
    service: str
    type: int
    data: dict = {}

    __length = 0

    def __init__(self, **kwargs):
        self.data = {}
        raw_data = kwargs.get("raw_data", None)

        if raw_data is not None:
            # Create message from bytes (used to parse incoming messages)
            self.__parse_raw_data(raw_data)
        else:
            # Create message from arguments (used to create outgoing messages)
            self.service = kwargs.get("service", None)
            self.type = kwargs.get("type", None)
            self.data = kwargs.get("data", None)

    def __str__(self):
        length = len(self.compile()) if self.__length == 0 else self.__length
        return f"{self.service} {hex(self.type)} ({length} bytes) {self.data}"

    def __parse_raw_data(self, raw_data: bytes):
        received_length = len(raw_data)

        if received_length < HEADER_LENGTH:
            raise Exception(
                f"Packet is too short to be valid (Expected at least 12 bytes, got {received_length})"
            )

        self.service = raw_data[
            SERVICE_OFFSET : SERVICE_OFFSET + SERVICE_LENGTH
        ].decode("utf-8")

        self.type = int.from_bytes(
            raw_data[KIND_OFFSET : KIND_OFFSET + KIND_LENGTH], byteorder="big"
        )

        self.__length = int.from_bytes(
            raw_data[LENGTH_OFFSET : LENGTH_OFFSET + LENGTH_LENGTH], byteorder="big"
        )

        if received_length != self.__length:
            raise Exception(
                f"Packet length does not match (Received: {received_length}, Expected: {self.__length})"
            )

        self.__read_data(raw_data, HEADER_LENGTH)

    def __read_data(self, raw_data, offset):
        transaction_data = raw_data[offset:].decode("utf-8").split("\n")

        # If transaction data is null terminated, remove null terminator before parsing
        if transaction_data[-1] == "\0":
            transaction_data = transaction_data[:-1]

        tokens = self.__make_key_value_pairs(transaction_data)
        tree = {}

        for key, value in tokens:
            tree = self.__add_branch(tree, key.split("."), self.__parse_value(value))

        self.parse_transaction_data(tree)

    def __make_key_value_pairs(self, transaction_data):
        final = []

        for data in transaction_data:
            pair = data.split("=", 1)

            if len(pair) != 2:
                # Ignore invalid pairs
                continue

            final.append(pair)

        return final

    def __add_branch(self, tree, vector, value):
        key = vector[0]
        tree[key] = (
            value
            if len(vector) == 1
            else self.__add_branch(tree[key] if key in tree else {}, vector[1:], value)
        )
        return tree

    def parse_transaction_data(self, data):
        for key, value in data.items():
            if isinstance(value, dict) and "[]" in value:
                length = value.pop("[]")
                temp_array = []

                for item in value:
                    temp_array.append(value[item])

                if length != len(temp_array):
                    logger.warning(
                        f"Array length does not match (Expected: {length}, Got: {len(temp_array)})"
                    )

                self.data[key] = temp_array
            else:
                self.data[key] = value

    def __parse_value(self, value: str):
        """Parse value from string"""
        if value.isdigit():
            return int(value)
        else:
            return unquote(value)

    def __encode_string(self, value):
        if isinstance(value, datetime):
            temp_value = quote(value.strftime("%b-%d-%Y %H:%M:%S UTC"))
        else:
            temp_value = quote(str(value))

        temp_value = temp_value.replace("%20", " ")

        if temp_value.find(" ") != -1:
            temp_value = '"' + temp_value + '"'

        return re.sub(r"%[0-9A-F]{2}", lambda pat: pat.group(0).lower(), temp_value)

    def compile(self):
        temp_packet = self.service.encode()
        temp_packet += int.to_bytes(self.type, 4, byteorder="big")

        temp_data = self.__convert_data()

        temp_packet += int.to_bytes(HEADER_LENGTH + len(temp_data), 4, byteorder="big")
        temp_packet += temp_data.encode()

        return temp_packet

    def __convert_data(self):
        final_data = ""
        temp_data = flatten(self.data)

        for key in temp_data:
            value = temp_data[key]

            if isinstance(value, Enum):
                final_data += key + "=" + str(value.value) + "\n"
            elif isinstance(value, list):
                final_data += key + ".[]=" + str(len(value)) + "\n"
                final_data += self.__process_dict(key, value)
            else:
                final_data += "%s=%s\n" % (key, self.__encode_string(value))

        # EA uses the final NULL delimiter so we set the last char from the data to NULL
        final_data = final_data[:-1]  # Remove last new line char
        final_data += "\0"  # Append NULL

        return final_data

    def __process_dict(self, key, values, skip_idx=False):
        processed_dict = ""

        for x in range(len(values)):
            if isinstance(values[x], dict):
                for y in values[x]:
                    if isinstance(values[x][y], list):
                        processed_dict += (
                            f"{key}.{x}.{y}" + ".[]=" + str(len(values[x][y])) + "\n"
                        )

                        processed_dict += self.__process_dict(
                            f"{key}.{x}.{y}", values[x][y]
                        )
                    elif isinstance(values[x][y], dict):
                        processed_dict += self.__process_dict(
                            f"{key}.{x}.{y}", [values[x][y]], True
                        )
                    else:
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
                if isinstance(values[x], list):
                    processed_dict += f"{key}.{x}" + ".[]=" + str(len(values[x])) + "\n"
                    processed_dict += self.__process_dict(f"{key}.{x}", values[x])
                elif isinstance(values[x], dict):
                    processed_dict += self.__process_dict(
                        f"{key}.{x}", [values[x]], True
                    )
                else:
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

        return processed_dict
