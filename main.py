import parsers.rhym
import os

Parser = parsers.rhym.RhymParser()
main_path = os.path.dirname(__file__)
rhym_path = os.path.join(main_path, "Test Maps", "rhym")
rhym_map_path = os.path.join(rhym_path, "Haxagon_iyowa_Kyu-kurarin_(7_7_bootleg)")
# lmfao


rhym_test_map = Parser.RhymDecoder(rhym_map_path)
print(rhym_test_map.difficulty_objectdata)