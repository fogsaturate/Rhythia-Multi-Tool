"""
I am making this library because frankly,
I am very C# pilled and all binary reader
libraries suck lmao, so this is just so
my job is easier for binary format
parsing.
"""

import struct
from typing import BinaryIO


class BinaryReader:
    def __init__(self, file: BinaryIO):
        self.file = file

    def read_uint8(self) -> int:
        byte_data = self.file.read(1)
        return int.from_bytes(byte_data, byteorder="little", signed=False)

    def read_uint16(self) -> int:
        bytes_data = self.file.read(2)
        return int.from_bytes(bytes_data, byteorder="little", signed=False)

    def read_uint32(self) -> int:
        bytes_data = self.file.read(4)
        return int.from_bytes(bytes_data, byteorder="little", signed=False)

    def read_uint64(self) -> int:
        bytes_data = self.file.read(8)
        return int.from_bytes(bytes_data, byteorder="little", signed=False)

    def read_single(self) -> float:
        bytes_data = self.file.read(4)
        return struct.unpack('<f', bytes_data)[0]

    def read_double(self) -> float:
        bytes_data = self.file.read(8)
        return struct.unpack('<d', bytes_data)[0]

    def get_string_buffer(self, length) -> str:
        string_length_bytes = self.file.read(length)
        string_length = int.from_bytes(string_length_bytes, byteorder='little', signed=False)
        string_bytes = self.file.read(string_length)
        return string_bytes.decode('utf-8')
