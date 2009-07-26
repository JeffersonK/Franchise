#gs = global static

gsBATTING_LINEUP_LENGTH = 9
gsPLAYERFREEAGENT = -1

gsMAXGAMEINNINGS = 9
gsOUTSPERINNING = 3
gsBASEEMPTY = -1

#Position Codes (INTs)
gsPITCHER_POSCODE,gsCATCHER_POSCODE,gsFIRSTBASE_POSCODE, gsSECONDBASE_POSCODE, gsTHIRDBASE_POSCODE, gsSHORTSTOP_POSCODE, gsLEFTFIELDER_POSCODE, gsCENTERFIELDER_POSCODE, gsRIGHTFIELDER_POSCODE, gsDESIGNATEDHITTER_POSCODE = range(1,11)

#Position Codes (STRs) POSCODE -> POSSTR
gsPOSITION_POSSTR = {1:'P',2:'C',3:'1B',
                     4:'2B',5:'3B',6:'SS',
                     7:'LF',8:'CF',9:'RF',10:'DH'}


gsHOMEBASE = 0
gsFIRSTBASE = 0
gsSECONDBASE = 0
gsTHIRDBASE = 0

#x,y from top left as origin going down
#gsBATTERZONES = [(0,0),(1,0),(2,0),
#                 (0,1),(1,1),(2,1),
#                 (0,2),(1,2),(2,2)]
gsSTRIKEZONE = range(9)
#gsBALLZONE = 9

gsPITCHCALL_STRIKE = 'STRIKE'
gsPITCHCALL_BALL = 'BALL'
gsPITCHCALL_FOUL = 'FOUL'
gsPITCHCALL_CONTACT = 'CONT'

gsMAXSTRIKECOUNT = 3
gsMAXBALLCOUNT = 4


gsPITCHCALL_STRIKEOUT = 'SO'
gsPITCHCALL_WALK = 'BB'
gsPITCHCALL_HITBYPITCH = 'HBP'
#gsPITCHCALL_INTENWALK = 'IBB'

#AtBatResult Codes (Strings) 
#
# FMT for an AT BAT Result is:
#         RESULT_CODE (batterGUID, pitcherGUID, pitchType, pitchZone, pitchSpeed, pitchCount, hitLocation (coordinates off the bat), fielderGUID(or NONE), RunnerAdvance List or NONE)
#
# RUNNERADV format is runnerGUID(base0, baseF) : 
#            where 0 is home first is 1, etc...
#
gsNULL_ATBATRESULT_CODE = ""
gsATBATRESULT_SINGLE = '1B'
#gsSINGLE_RESULT_FMT = '1B(
gsATBATRESULT_DOUBLE = '2B'
gsATBATRESULT_TRIPLE = '3B'
gsATBATRESULT_HOMERUN = 'HR'
gsATBATRESULT_GROUNDOUT = 'GO'
gsATBATRESULT_AIROUT = 'AO'
gsATBATRESULT_SACOUT = 'SAC'
gsATBATRESULT_DOUBLEPLAY = 'DP'
gsATBATRESULT_TRIPLEPLAY = 'TP'

gsATBATRESULT_STRIKEOUT = gsPITCHCALL_STRIKEOUT
gsATBATRESULT_WALK = gsPITCHCALL_WALK
gsATBATRESULT_HITBYPITCH = gsPITCHCALL_HITBYPITCH
#gsATBATRESULT_INTENTIONALWALK = gsPITCHCALL_INTENWALK


gsCONTACTMADEEVENTS = [gsATBATRESULT_SINGLE,
                       gsATBATRESULT_DOUBLE,
                       gsATBATRESULT_TRIPLE,
                       gsATBATRESULT_HOMERUN,
                       gsATBATRESULT_GROUNDOUT,
                       gsATBATRESULT_AIROUT,
                       gsATBATRESULT_SACOUT,
                       gsATBATRESULT_DOUBLEPLAY,
                       gsATBATRESULT_TRIPLEPLAY,]


#gsBATTINGEVENTS = ['1B','2B','3B','HR','BB','SO','HBP',
#                   'GO','AO','SAC','DP','TP']#,'IBB']

gsHITS = ['1B','2B','3B','HR']
gsNOTATBAT = ['BB','HBP']
#gsDONTADDPITCH = ['SO','BB']
gsSINGLEOUTPLAYS = ['GO','SO','AO','SAC']
gsMULTIOUTPLAYS = ['DP','TP']
gsOUTEVENTS = gsSINGLEOUTPLAYS + gsMULTIOUTPLAYS
gsRUNNERSADVANCEEVENTS = gsHITS + ['BB','HBP','SAC']
gsMAXPITCHCOUNT = 10





#Pitch Types
gsCURVEBALL = 'CRV'
gsFASTBALL = 'FST'
gsSLIDER = 'SLD'
gsCHANGEUP = 'CHNG'
gsKNUCKLEBALL = 'KNCK'
gsSINKER = 'SINK'
gsSPITBALL = 'SPIT'
gsFORKBALL = 'FORK'

gsPITCHTYPES = [gsFASTBALL, 
                gsCURVEBALL, 
                gsSLIDER,
                gsCHANGEUP, 
                gsKNUCKLEBALL, 
                gsSINKER, 
                gsSPITBALL,
                gsFORKBALL]


class GlobalState:
 
    def __init__(self):
        self.__nextPlayerGUID = 0
        self.__nextFranchiseGUID = 0
        return

    def __str__(self):
        return self.__getstate__()

    def nextPlayerGUID(self):
        self.__nextPlayerGUID += 1
        return self.__nextPlayerGUID - 1
    
    def nextFranchiseGUID(self):
        self.__nextFranchiseGUID += 1
        return self.__nextFranchiseGUID - 1

    def __getstate__(self):
        
        state = "{'nextPlayerGUID':%d,'nextFranchiseGUID':%d}" % (self.__nextPlayerGUID, self.__nextFranchiseGUID)
        return state 

    def __setstate__(self, dictStr):
        print "TODO: check for eval errors when loading Global State"        
        d = eval(dictStr)
        self.__nextPlayerGUID = d['nextPlayerGUID']
        self.__nextFranchiseGUID = d['nextFranchiseGUID']

#globalState = GlobalState()
