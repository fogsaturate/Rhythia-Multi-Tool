import parsers.rhym
import parsers.vulnus
import os

RhymParser = parsers.rhym.RhymParser()
VulnusParser = parsers.vulnus.VulnusParser()

main_path = os.path.dirname(__file__)



rhym_path = os.path.join(main_path, "Test Maps", "rhym")
rhym_map_path = os.path.join(rhym_path, "Haxagon_iyowa_Kyu-kurarin_(7_7_bootleg)")
rhym_output_path = os.path.join(main_path, "Output", "rhym")

vulnus_path = os.path.join(main_path, "Test Maps", "vulnus")
vulnus_map_path = os.path.join(vulnus_path, "Multipole Expansion")
# lmfao


rhym_map = RhymParser.RhymDecoder(rhym_map_path)
vulnus_map = VulnusParser.VulnusDecoder(vulnus_map_path)

vulnus_map_music_path = os.path.join(vulnus_map_path, vulnus_map.audio_filename)
vulnus_map_cover_path = os.path.join(vulnus_map_path, "cover.png")


# testing only

vulnus_map_difficulty_data = []
current_difficulty_name = []

for i in vulnus_map.difficulty_data:
    vulnus_difficulty_data = {
        "difficulty_name": i["difficulty_name"],
        "mappers": vulnus_map.mappers, # theres not really any other way to do this unfortunately
        "note_count": i["note_count"],
        "note_fields": 3,
        "note_list": i["note_list"] # in x, y, time (in ms) format. example: {'x': 0, 'y': 0, 'time': 100}
    }
    vulnus_map_difficulty_data.append(vulnus_difficulty_data)

print(vulnus_map_music_path)
print(vulnus_map_cover_path)

RhymParser.RhymEncoder(
    vulnus_map.version,
    vulnus_map.artist,
    vulnus_map.title,
    vulnus_map.difficulties,
    vulnus_map_difficulty_data,

    rhym_output_path,
    export_as_rhym=True,
    music_path=vulnus_map_music_path,
    cover_path=vulnus_map_cover_path
)

