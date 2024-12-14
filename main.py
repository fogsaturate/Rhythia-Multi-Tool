import parsers.rhym
import parsers.vulnus
import os

RhymParser = parsers.rhym.RhymParser()
VulnusParser = parsers.vulnus.VulnusParser()

main_path = os.path.dirname(__file__)

rhym_path = os.path.join(main_path, "Test Maps", "rhym")
rhym_map_path = os.path.join(rhym_path, "Haxagon_iyowa_Kyu-kurarin_(7_7_bootleg)")

vulnus_path = os.path.join(main_path, "Test Maps", "vulnus")
vulnus_map_path = os.path.join(vulnus_path, "Multipole Expansion")
# lmfao


rhym_map = RhymParser.RhymDecoder(rhym_map_path)
vulnus_map = VulnusParser.VulnusDecoder(vulnus_map_path)
RhymParser.RhymEncoder(
    vulnus_map.version,
    vulnus_map.artist,
    vulnus_map.title,
    vulnus_map.difficulties,
    [
        {
          'difficulty_name': 'example',
          'artist': 'exampleartist',
          'romanized_artist': 'optionalartist',
          'title': 'exampletitle',
          'romanized_title': 'optionaltitle',
          'mappers': ['example mapper 1'],
          'note_count': 100
        }
    ],
    [
        {
            'note_fields': 3,
            'note_list': [{'x': 0, 'y': 1, 'time': 100},{'x': 1, 'y': -1, 'time': 200}]
        }
    ],
    romanized_artist="Bob"
)

# print(rhym_map.difficulty_objectdata)