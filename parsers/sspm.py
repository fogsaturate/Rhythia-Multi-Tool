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
        self.header: str = ""
        self.version: int = 0

        self.last_ms: int = 0
        self.total_note_count: int = 0
        self.total_marker_count: int = 0

        self.difficulty: int = 0
        self.star_rating: int = 0

        self.audio_exists: int = 0
        self.cover_exists: int = 0
        self.mod_chart_exists: int = 0

        self.custom_data_offset: int = 0
        self.custom_data_length: int = 0
        self.audio_data_offset: int = 0
        self.audio_data_length: int = 0
        self.cover_data_offset: int = 0
        self.cover_data_length: int = 0
        self.marker_definition_offset: int = 0
        self.marker_definition_length: int = 0
        self.marker_section_offset: int = 0
        self.marker_section_length: int = 0

        self.map_id: str = ""
        self.map_name: str = ""
        self.song_name: str = ""
        self.mappers: list = []

        self.custom_data: list = [] # this is where difficulty names would go

        self.audio_data = None
        self.cover_data = None

        self.marker_definitions: list = []

        self.markers: list = []

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
                return binary_reader.read_string_buffer(2)
            case 10: # long buffer
                long_buffer_length = binary_reader.read_uint32()
                return file.read(long_buffer_length)
            case 11: # long string
                return binary_reader.read_string_buffer(4)
            case 12: # array
                data_type_array = []

                array_data_type_length = binary_reader.read_uint32() # not even i know what this means
                array_object_count = binary_reader.read_uint16()

                array_data_type = binary_reader.read_uint8()
                for i in range(array_object_count):
                    data_type_array.append(self.data_types(file, array_data_type))
                return data_type_array



    def SSPMDecoder(self, sspm_map: str):
        try:
            with open(sspm_map, "rb") as file:
                binary_reader = BinaryReader(file)

                self.header = file.read(4).decode('utf-8')
                if self.header != "SS+m":
                    raise ValueError(f"Invalid Header: {self.header}")

                self.version = binary_reader.read_uint16()
                if self.version == 2:
                    self.SSPMv2(file)
                else:
                    raise ValueError(f"Unsupported Version! This SSPM file is v{self.version}")
        except:
            raise ValueError("Invalid file! Make sure it is a proper SSPM file.")

        return self

    def SSPMv1(self):

        pass

    def SSPMv2(self, file: BinaryIO):
        binary_reader = BinaryReader(file)

        file.read(4)
        file.read(20) # reserved space
        # --- Parsing Metadata ---
        self.last_ms = binary_reader.read_uint32()
        self.total_note_count = binary_reader.read_uint32()
        self.total_marker_count = binary_reader.read_uint32()

        self.difficulty = binary_reader.read_uint8()

        self.star_rating = binary_reader.read_uint16() # Never Used

        self.audio_exists = binary_reader.read_uint8()
        self.cover_exists = binary_reader.read_uint8()
        self.mod_chart_exists = binary_reader.read_uint8()

        # --- Pointers ---
        self.custom_data_offset = binary_reader.read_uint64()
        self.custom_data_length = binary_reader.read_uint64()
        self.audio_data_offset = binary_reader.read_uint64()
        self.audio_data_length = binary_reader.read_uint64()
        self.cover_data_offset = binary_reader.read_uint64()
        self.cover_data_length = binary_reader.read_uint64()
        self.marker_definition_offset = binary_reader.read_uint64()
        self.marker_definition_length = binary_reader.read_uint64()
        self.marker_section_offset = binary_reader.read_uint64()
        self.marker_section_length = binary_reader.read_uint64()

        # --- Song Metadata ---
        self.map_id = binary_reader.read_string_buffer(2)
        self.map_name = binary_reader.read_string_buffer(2)
        self.song_name = binary_reader.read_string_buffer(2)

        mapper_count = binary_reader.read_uint16()
        for i in range(mapper_count): # for every mapper in mapper_count,
            self.mappers.append(binary_reader.read_string_buffer(2))

        # --- Custom Data --- (this is going to be long)
        custom_data_object_count = binary_reader.read_uint16()

        custom_data_dict = {
            "custom_data_object_count": custom_data_object_count,
            "custom_data": []
        }
        for i in range(custom_data_object_count):
            custom_data_field_indicator = binary_reader.read_string_buffer(2) # usually going to be difficulty_name
            custom_data_object_data_type = binary_reader.read_uint8()
            custom_data_object_value = self.data_types(file, custom_data_object_data_type)

            custom_data_object = {
                "field_indicator": custom_data_field_indicator,
                "data_type": custom_data_object_data_type,
                "value": custom_data_object_value
            }
            custom_data_dict["custom_data"].append(custom_data_object)

        self.custom_data = custom_data_dict


        return self
