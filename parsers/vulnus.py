import os
import json

class VulnusParser:
    # {"_artist": "rocky", "_difficulties": ["converted.json", "opium.json", "ss.json" ], "_mappers": ["Water & fogsaturate"], "_music": "Multipole Expansion.mp3", "_title": "Multipole Expansion", "_version": 1}
    def __init__(self):
        self.version: int = 0
        self.artist: str = "Unknown Artist"
        self.title: str = "Unknown Title"
        self.mappers: list = ["Unknown Mapper"]
        self.difficulties: list = ["official.json"] # auto converted maps are called official
        self.audiofilename: str = "audio.mp3"

        self.difficulty_data: list = [] # there is only one .json for difficulties!

    def VulnusDecoder(self, folder_path: str):
        meta_file_path: str = os.path.join(folder_path, "meta.json")

        with open(meta_file_path, 'r') as vulnus_meta:
            vulnus_meta_data: dict = json.loads(vulnus_meta.read())

        self.version = vulnus_meta_data["_version"]
        self.artist = vulnus_meta_data["_artist"]
        self.title = vulnus_meta_data["_title"]
        self.mappers = vulnus_meta_data["_mappers"]
        self.difficulties = vulnus_meta_data["_difficulties"]
        self.audiofilename = vulnus_meta_data["_music"]

        for i in self.difficulties:

            difficulty_note_path = os.path.join(folder_path, i)

            with open (difficulty_note_path, 'r') as difficulty_note:
                diff_note_data: dict = json.loads(difficulty_note.read())

            note_list = diff_note_data["_notes"]

            notes: list = []

            for note in note_list:
                time = int(note["_time"] * 1000)
                x = note["_x"]
                y = note["_y"]

                notes.append({"x": x, "y": y, "time": time})

            difficulty_data_object = {
                "difficulty_name": diff_note_data["_name"],
                "approach_distance": diff_note_data["_approachDistance"],
                "approach_time": diff_note_data["_approachTime"],
                "note_list": notes
            }

            self.difficulty_data.append(difficulty_data_object)

        return self

    def VulnusEncoder(self):
        pass