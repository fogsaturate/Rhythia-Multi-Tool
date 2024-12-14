class SSPMParser:
    def __init__(self):
        self.lastMs = None
        self.metadata = {}
        self.songName = None
        self.requiresMod = 0
        self.strict = False
        self.coverBytes = None
        self.Difficulty = 0
        self.audioBytes = None
        self.mapName = None
        self.mappers = None
        self.Notes = None
        self.mapID = None
        self.customDataOffset = 0
    def SSPMHeader(self):
            pass
    def SSPMv1(self):
            pass
    def SSPMv2(self):
            pass