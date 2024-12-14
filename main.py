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


rhym_test_map = RhymParser.RhymDecoder(rhym_map_path)
vulnus_test_map = VulnusParser.VulnusDecoder(vulnus_map_path)

print(vulnus_test_map.difficulty_data)