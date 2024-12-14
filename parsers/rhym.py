import json
import os
import shutil
import zipfile

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

        self.version = global_meta_data['version']
        self.artist = global_meta_data['artist']
        if "romanizedArtist" in global_meta_data:
            self.romanized_artist = global_meta_data['romanizedArtist']
        self.title = global_meta_data['title']
        if "romanizedTitle" in global_meta_data:
            self.title = global_meta_data['romanizedTitle']

        self.difficulties = global_meta_data['difficulties']

        for i in self.difficulties: # this will be a very big for loop! teehee!

            # diff metadata stuff goes here

            difficulty_metadata_path = os.path.join(folder_path, i, "metadata.json")
            with open(difficulty_metadata_path, 'r') as difficulty_meta:
                diff_meta_data: dict = json.loads(difficulty_meta.read())

            difficulty_metadata_object = {
                "difficulty_name": diff_meta_data["difficultyName"],
                "mappers": diff_meta_data["mappers"],
                "note_count": diff_meta_data["noteCount"]
            }

            # difficulty song metadata is optional if it has different songs
            if "artist" in diff_meta_data:
                difficulty_metadata_object["artist"] = diff_meta_data["artist"]
            if "romanizedArtist" in diff_meta_data:
                difficulty_metadata_object["romanized_artist"] = diff_meta_data["romanizedArtist"]
            if "title" in diff_meta_data:
                difficulty_metadata_object["title"] = diff_meta_data["title"]
            if "romanizedTitle" in diff_meta_data:
                difficulty_metadata_object["romanized_title"] = diff_meta_data["romanizedTitle"]

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

    # encoder = writes
    # this is for all the required attributes
    def RhymEncoder(
        self,
        version: int,
        artist: str,
        title: str,
        difficulties: list,
        difficulty_data: list,
        # formatted in a dictionary
        # [{
        #
        #   'difficulty_name': 'example',
        #   'artist': 'optionalartist',
        #   'romanized_artist': 'optionalromanizedartist',
        #   'title': 'optionaltitle',
        #   'romanized_title': 'optionalromanizedtitle',
        #   'mappers': ['example mapper 1'],
        #   'note_count': 2,
        #   'note_fields': 3, (how many note properties there are, for example x, y, and time is only 3 properties)
        #   'note_list': [{'x': 0, 'y': 1, 'time': 100},{'x': 1, 'y': -1, 'time': 200}],
        # }]
        output_path: str,
        export_as_rhym = False, # optional, export as a .rhym zip (for sharing purposes)
        romanized_artist = None, # optional
        romanized_title = None, # optional
        music_path = None, # optional but highly recommended
        cover_path = None # also optional
    ):

        mappersarray = []

        for metadataindex in difficulty_data:
            mappersarray += metadataindex["mappers"]

        no_duplicates_mappers = list(dict.fromkeys(mappersarray)) # get rid of duplicates

        total_mappers_string = ' '.join(no_duplicates_mappers) # for loop slop but it works LOL

        map_output_id = (total_mappers_string + f" - {artist} - {title}").replace(" ", "_") # this is for the preferred .rhym output id format

        map_output_path = os.path.join(output_path, map_output_id)

        if not os.path.exists(map_output_path):
            os.makedirs(map_output_path)

        output_metadata = os.path.join(map_output_path, "metadata.json")
        output_music = os.path.join(map_output_path, "audio.mp3")
        output_cover = os.path.join(map_output_path, "cover.png")

        global_metadata_dict = {
            "version": version,
            "artist": artist,
            "title": title,
            "difficulties": difficulties
        }

        if romanized_artist:
            global_metadata_dict["romanizedArtist"] = romanized_artist
        if romanized_title:
            global_metadata_dict["romanizedTitle"] = romanized_title

        with open(output_metadata, 'w') as global_metadata_file:
            json.dump(global_metadata_dict, global_metadata_file, indent=4)

        if music_path:
            shutil.copyfile(music_path, output_music)
        if cover_path:
            shutil.copyfile(cover_path, output_cover)

        for i in difficulty_data:

            # difficulty's metadata.json

            current_difficulty_name = i["difficulty_name"]
            difficulty_name_dir = os.path.join(map_output_path, current_difficulty_name)

            if not os.path.exists(difficulty_name_dir):
                os.makedirs(difficulty_name_dir)

            difficulty_metadata_dict = {
                "difficultyName": current_difficulty_name,
                "mappers": i["mappers"],
                "noteCount": i["note_count"]
            }

            difficulty_metadata_path = os.path.join(difficulty_name_dir, "metadata.json")

            with open(difficulty_metadata_path, 'w') as difficulty_metadata_json:
                json.dump(difficulty_metadata_dict, difficulty_metadata_json, indent=4)

            # time for notes!
            # difficulty's object.json

            note_list = i["note_list"]

            notes: list = []

            previous_ms: int = 0

            for note in note_list:
                x = note["x"]
                y = note["y"]
                time = note["time"]

                """
                delta is used to save file space! its basically
                the value you get when you subtract the current
                note's time with the last note's time (in ms)
                """

                delta = time - previous_ms # time - previous ms (first is always 0)
                previous_ms = time # define previous ms as the time in the actual note index

                notes.extend([delta, x, y])

            difficulty_object_dict = {
                "noteFields": i["note_fields"],
                "noteList": notes
            }

            difficulty_object_path = os.path.join(difficulty_name_dir, "object.json")

            with open(difficulty_object_path, 'w') as difficulty_object_json:
                json.dump(difficulty_object_dict, difficulty_object_json, separators=(',', ':'))
                """
                The separators here in the json.dump gets
                rid of all the spaces, so you can save
                more space! for example, without the
                separators, the noteList would look like
                [1, 0, 100, 0, -1, 100]

                The separators make it now look like
                [1,0,100,0,-1,100]

                Very cool
                """

        if export_as_rhym == True:
            rhym_file_name = f"{map_output_id}.rhym"
            rhym_output_path = os.path.join(output_path, rhym_file_name)
            with zipfile.ZipFile(rhym_output_path, 'w') as zip_stream:
                for root, dirs, files in os.walk(map_output_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, map_output_path)
                        zip_stream.write(file_path, arcname=arcname)

            if os.path.exists(map_output_path):
                shutil.rmtree(map_output_path)