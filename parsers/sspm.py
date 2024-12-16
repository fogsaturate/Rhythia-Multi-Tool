"""
I am planning on parsing every last detail
that basil intended for SSPMv2, including
every data type, and even custom difficulty
names. This also includes skipping unnecessary
errors such as if custom data is filled with
garbage.

I will also be explaining the meaning and
documentation since the official documentation
is lackluster, and so it will also be useful
for anyone planning on parsing the format
in the future.
"""

from typing import BinaryIO
from parsers.binary_reader import BinaryReader
from enum import Enum

class Difficulty(Enum):
    NA = 0
    EASY = 1
    MEDIUM = 2
    HARD = 3
    LOGIC = 4
    TASUKETE = 5

class SSPMParser:
    def __init__(self):
        self.version: int = 0
        self.note_count: int = 0

        self.last_ms: int = 0
        self.total_note_count: int = 0
        self.total_marker_count: int = 0

        self.difficulty: int = 0
        self.star_rating: int = 0

        self.audio_exists: int = 0
        self.cover_exists: int = 0
        self.mod_chart_exists: int = 0

    def data_types(self, file: BinaryIO, data_type: int):
        binary_reader = BinaryReader(file)
        match data_type:
            case 1: # 1 byte int
                return binary_reader.read_uint8()
            case 2: # 2 byte int
                return binary_reader.read_uint16()
            case 3: # 4 byte int
                return binary_reader.read_uint32()
            case 4: # 8 byte int
                return binary_reader.read_uint64()
            case 5: # 4 byte float
                return binary_reader.read_single()
            case 6: # 8 byte float
                return binary_reader.read_double()
            case 7: # note
                note_storage_type = binary_reader.read_uint8() # quantum bool

                if note_storage_type == 1:
                    x = binary_reader.read_uint8()
                    y = binary_reader.read_uint8()
                    return x, y
                else:
                    x = binary_reader.read_single()
                    y = binary_reader.read_single()
                    return x, y

            case 8: # short buffer
                buffer_length = binary_reader.read_uint16()
                return file.read(buffer_length)
            case 9: # short string
                string_length = binary_reader.read_uint16()
                return binary_reader.get_string_buffer(string_length)
            case 10: # long buffer
                long_buffer_length = binary_reader.read_uint32()
                return file.read(long_buffer_length)
            case 11: # long string
                long_string_length = binary_reader.read_uint32()
                return binary_reader.get_string_buffer(long_string_length)
            case 12: # array
                data_type_array = []

                array_data_type_length = binary_reader.read_uint32() # not even i know what this means
                array_object_count = binary_reader.read_uint16()

                array_data_type = binary_reader.read_uint8()
                for i in range(array_object_count):
                    data_type_array.append(self.data_types(file, array_data_type))
                return data_type_array



    def SSPMDecoder(self, sspm_map: str):
        with open(sspm_map, "rb") as file:
            binary_reader = BinaryReader(file)

            header = file.read(4)
            self.version = binary_reader.read_uint8()
            if self.version == 2:
                self.SSPMv2(file)

        return self

    def SSPMv1(self):

        pass

    def SSPMv2(self, file: BinaryIO):
        binary_reader = BinaryReader(file)

        file.read(4) # reserved space
        file.read(20) # hash

        self.last_ms = binary_reader.read_uint32()
        self.total_note_count = binary_reader.read_uint32()
        self.total_marker_count = binary_reader.read_uint32()

        self.difficulty = binary_reader.read_uint8()

        self.star_rating = binary_reader.read_uint16()

        self.audio_exists = binary_reader.read_uint8()
        self.cover_exists = binary_reader.read_uint8()
        self.mod_chart_exists = binary_reader.read_uint8()

        return self
