class VulnusParser:
    # {"_artist": "rocky", "_difficulties": ["converted.json", "opium.json", "ss.json" ], "_mappers": ["Water & fogsaturate"], "_music": "Multipole Expansion.mp3", "_title": "Multipole Expansion", "_version": 1}
    def __init__(self):
        self._version: int = 0
        self._artist: str = "Unknown Artist"
        self._title: str = "Unknown Title"
        self._mappers: list = ["Unknown Mapper"]
        self._difficulties: list = ["official.json"] # auto converted maps are called official
        self._music: list = ["audio.mp3"]

    def VulnusDecoder(self):
        pass
