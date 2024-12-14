import json
import os

class RhymParser:
    def __init__(self):
        self.version: int = 0
        self.artist: str = "Unknown Artist"
        self.romanized_artist: str = "Unknown Artist"
        self.title: str = "Unknown Title"
        self.romanized_title: str = "Unknown Title"
        self.difficulties: list = ["Unknown Difficulty"]

        self.difficulty_metadata: list = []
        self.difficulty_objectdata: list = []
    
    def RhymDecoder(self, folder_path: str): # decoder = reads
        metadata_file_path: str = os.path.join(folder_path, "metadata.json")

        with open(metadata_file_path, 'r') as global_meta:
            global_meta_data: dict = json.loads(global_meta.read())

        difficulty = global_meta_data['difficulties']

        for i in difficulty: # this will be a very big for loop! teehee!

            # diff metadata stuff goes here

            difficulty_metadata_path = os.path.join(folder_path, i, "metadata.json")
            with open(difficulty_metadata_path, 'r') as difficulty_meta:
                diff_meta_data: dict = json.loads(difficulty_meta.read())

            difficulty_metadata_object = {
                "artist": diff_meta_data["artist"],
                "title": diff_meta_data["title"],
                "mappers": diff_meta_data["mappers"],
                "note_count": diff_meta_data["noteCount"]
            }

            # this is for japanese titles, this checks if it has "romanizedTitle"s
            if "romanizedArtist" in diff_meta_data:
                difficulty_metadata_object["romanizedArtist"] = diff_meta_data["romanizedArtist"]
            if "romanizedTitle" in diff_meta_data:
                difficulty_metadata_object["romanizedTitle"] = diff_meta_data["romanizedTitle"]

            self.difficulty_metadata.append(difficulty_metadata_object)

            # diff object data goes here

            difficulty_object_path = os.path.join(folder_path, i, "object.json")

            with open(difficulty_object_path, 'r') as difficulty_object:
                diff_object_data: dict = json.loads(difficulty_object.read())
            note_count = diff_meta_data["noteCount"]
            note_fields = diff_object_data["noteFields"]

            note_list = diff_object_data["noteList"]

            notes: list = []

            current_ms = 0
            # # start at 0, up until note_count, increment by 3 note fields (properties)
            for i in range(0, note_count * note_fields, note_fields):
                time = note_list[i] + current_ms
                x = note_list[i + 1]
                y = note_list[i + 2]
                notes.append({"x": x, "y": y, "time": time})
                current_ms = time
            
            difficulty_objectdata_object = {
                "note_fields": diff_object_data["noteFields"],
                "note_list": notes
            }

            self.difficulty_objectdata.append(difficulty_objectdata_object)

        return self
            
    def RhymEncoder(self): # encoder = writes
        pass
