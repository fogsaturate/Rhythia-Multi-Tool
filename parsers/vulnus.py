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
        self.audio_filename: str = "audio.mp3"

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
        self.audio_filename = vulnus_meta_data["_music"]

        for i in self.difficulties:

            difficulty_note_path = os.path.join(folder_path, i)

            with open (difficulty_note_path, 'r') as difficulty_note:
                diff_note_data: dict = json.loads(difficulty_note.read())

            note_list = diff_note_data["_notes"]
            note_count = 0
            notes: list = []

            for note in note_list:
                time = round(int(note["_time"] * 1000)) # im rounding because sometimes you get numbers like 56418.9499999283
                x = round(note["_x"], 3)
                y = round(note["_y"], 3)
                notes.append({"x": x, "y": y, "time": time})
                note_count += 1

            difficulty_data_object = {
                "difficulty_name": diff_note_data["_name"],
                "approach_distance": diff_note_data["_approachDistance"],
                "approach_time": diff_note_data["_approachTime"],
                "note_count": note_count,
                "note_list": notes
            }

            self.difficulty_data.append(difficulty_data_object)

        return self

    def VulnusEncoder(
        self,
        artist: str,
        title: str,
        difficulties: list,
        mappers: list,
        difficulty_data: list,
        # formatted in a dictionary
        # [{
        #   'difficulty_name': 'example',
        #   'approach_distance': 50,
        #   'approach_time': 1,
        #   'note_list': [{'x': 0, 'y': 1, 'time': 100},{'x': 1, 'y': -1, 'time': 200}],
        # }]
        output_path: str,
        export_as_vul=False, # EXTREMELY DEPRECATED. NEVER USE EVER.
        music_path: str = None,
        cover_path: str = None
    ):
        pass