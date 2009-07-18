class PitchBatterHistoryDB:

class PitcherBatterHistory:

    def __init__(self, pitcherGUID, batterGUID):
        
        self.__pitcherGUID = pitcherGUID
        self.__batterGUID = batterGUID
        self.__HRs = 0
        self.__atBats = [] #(pitcher playerGUID, AtBatResultStr)
        self.__hits = 0
        self.__rbis = 0
        self.__runs = 0
        
        #pitching
        self.__battersFaced = [] #(batter playerGUID, AtBatResultStr)
        self.__ks = 0
        self.__walks = 0
        self.__hitsAllowed = 0
        self.__HRsAllowed = 0
        self.__earnedRuns = 0
        self.__totPitches = 0
        self.__totBalls = 0
        self.__totStrikesThrown = 0 #strikes + fouls
        self.__outsPitched = 0

