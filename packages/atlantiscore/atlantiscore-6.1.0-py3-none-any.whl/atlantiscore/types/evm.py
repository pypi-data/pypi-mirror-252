from __future__ import annotations

from typing import Any, Self, Type

from eth_utils.address import to_checksum_address
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import core_schema

from atlantiscore.lib.exceptions import InvalidEVMAddress

EXAMPLE_ADDRESS_STRING = "0xa8E219Aa773fb12A812B7A3a4671b5B1933a49A8"
LiteralEVMAddress = str | int | bytes
PREFIXED_ADDRESS_LENGTH = 42
ADDRESS_BYTE_LENGTH = 20
PREFIX_SIZE = 2
BYTE_ORDER = "big"
NUMBER_OF_BITS_IN_BYTE = 8


class EVMAddress:
    _value: bytes

    def __init__(self, value: EVMAddress | LiteralEVMAddress) -> None:
        self._value = _address_to_bytes(value)

    def _to_checksum(self) -> str:
        return to_checksum_address(self._value)

    def __bytes__(self) -> bytes:
        return self._value

    def __int__(self) -> int:
        return int.from_bytes(self._value, BYTE_ORDER)

    def __str__(self) -> str:
        return self._to_checksum()

    def __eq__(self, other: any) -> bool:
        try:
            return hash(self) == hash(EVMAddress(other))
        except InvalidEVMAddress:
            return False

    def __ne__(self, other: any) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return int(self)

    def __bool__(self) -> bool:
        return bool(int(self))

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Type[Any],
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls._validate,
            schema=core_schema.union_schema(
                (
                    core_schema.str_schema(
                        min_length=PREFIXED_ADDRESS_LENGTH - PREFIX_SIZE,
                        max_length=PREFIXED_ADDRESS_LENGTH,
                    ),
                    core_schema.int_schema(ge=0),
                    core_schema.bytes_schema(
                        min_length=ADDRESS_BYTE_LENGTH,
                        max_length=ADDRESS_BYTE_LENGTH,
                    ),
                    core_schema.is_instance_schema(cls=cls),
                )
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda v: str(v),
                info_arg=False,
                return_schema=core_schema.str_schema(),
            ),
        )

    @classmethod
    def _validate(cls, v: EVMAddress | LiteralEVMAddress) -> Self:
        try:
            return cls(v)
        except InvalidEVMAddress as e:
            raise ValueError(str(e))

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        core_schema: core_schema.CoreSchema,
        handler: GetJsonSchemaHandler,
    ) -> dict:
        json_schema = handler.resolve_ref_schema(handler(core_schema))
        json_schema.update(example=EXAMPLE_ADDRESS_STRING)
        return json_schema


def _address_to_bytes(value: EVMAddress | LiteralEVMAddress) -> bytes:
    try:
        if isinstance(value, EVMAddress):
            return bytes(value)

        if isinstance(value, str):
            address_bytes = _hex_to_bytes(value)
        elif isinstance(value, int):
            address_bytes = _int_to_bytes(value)
        elif isinstance(value, bytes):
            address_bytes = value
        else:
            raise TypeError

        if not _is_valid_address(address_bytes):
            raise ValueError

        return address_bytes
    except (ValueError, TypeError) as e:
        raise InvalidEVMAddress(value) from e


def _hex_to_bytes(address: str) -> bytes:
    if len(address) == PREFIXED_ADDRESS_LENGTH:
        address = address[PREFIX_SIZE:]
    return bytes.fromhex(address)


def _int_to_bytes(integer: int) -> bytes:
    return integer.to_bytes(_calculate_required_byte_count(integer), BYTE_ORDER).rjust(
        ADDRESS_BYTE_LENGTH, b"\x00"
    )


def _calculate_required_byte_count(integer: int) -> int:
    """Returns the minimum number of bytes required to represent the given int.

    Example:
    0 + 7 would require 0 bytes
    1 + 7 would require 1 byte
    """
    return (integer.bit_length() + 7) // NUMBER_OF_BITS_IN_BYTE


def _is_valid_address(address: bytes) -> bool:
    try:
        to_checksum_address(address)
        return True
    except ValueError:
        return False
