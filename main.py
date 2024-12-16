import parsers.rhym
import parsers.vulnus
import parsers.sspm
import os

RhymParser = parsers.rhym.RhymParser()
VulnusParser = parsers.vulnus.VulnusParser()
SSPMParser = parsers.sspm.SSPMParser()

main_path = os.path.dirname(__file__)

rhym_path = os.path.join(main_path, "Test Maps", "rhym")
rhym_map_path = os.path.join(rhym_path, "Haxagon_iyowa_Kyu-kurarin_(7_7_bootleg)")
rhym_output_path = os.path.join(main_path, "Output", "rhym")

vulnus_path = os.path.join(main_path, "Test Maps", "vulnus")
vulnus_map_path = os.path.join(vulnus_path, "Multipole Expansion")

sspm_path = os.path.join(main_path, "Test Maps", "sspm")
sspm_v2_path = os.path.join(sspm_path, "v2")
sspm_v2_map_path = os.path.join(sspm_v2_path, "xr_attractor_dimension.sspm")
# lmfao


rhym_map = RhymParser.RhymDecoder(rhym_map_path)
vulnus_map = VulnusParser.VulnusDecoder(vulnus_map_path)
sspm_v2_map = SSPMParser.SSPMDecoder(sspm_v2_map_path)

print(sspm_v2_map.header)
print(sspm_v2_map.version)
print(sspm_v2_map.custom_data)

vulnus_map_music_path = os.path.join(vulnus_map_path, vulnus_map.audio_filename)
vulnus_map_cover_path = os.path.join(vulnus_map_path, "cover.png")


# testing only

vulnus_map_difficulty_data = []
current_difficulty_name = []
real_vulnus_difficulty_names = []
for i in vulnus_map.difficulty_data:
    vulnus_difficulty_data = {
        "difficulty_name": i["difficulty_name"],
        "mappers": vulnus_map.mappers, # theres not really any other way to do this unfortunately
        "note_count": i["note_count"],
        "note_fields": 3,
        "note_list": i["note_list"] # in x, y, time (in ms) format. example: {'x': 0, 'y': 0, 'time': 100}
    }
    vulnus_map_difficulty_data.append(vulnus_difficulty_data)
    real_vulnus_difficulty_names.append(vulnus_difficulty_data["difficulty_name"])



# RhymParser.RhymEncoder(
#     vulnus_map.version,
#     vulnus_map.artist,
#     vulnus_map.title,
#     real_vulnus_difficulty_names,
#     vulnus_map_difficulty_data,
#
#     rhym_output_path,
#     # export_as_rhym=True,
#     music_path=vulnus_map_music_path,
#     # cover_path=vulnus_map_cover_path
# )

