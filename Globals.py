#gs = global static

gsBATTING_LINEUP_LENGTH = 9
gsPLAYERFREEAGENT = -1

#Position Codes (INTs)
gsPITCHER_POSCODE,gsCATCHER_POSCODE,gsFIRSTBASE_POSCODE, gsSECONDBASE_POSCODE, gsTHRIDBASE_POSCODE, gsSHORTSTOP_POSCODE, gsLEFTFIELDER_POSCODE, gsCENTERFIELDER_POSCODE, gsRIGHTFIELDER_POSCODE = range(1,10)

#Position Codes (STRs) POSCODE -> POSSTR
gsPOSITION_POSSTR = {1:'P',2:'C',3:'1B',
                     4:'2B',5:'3B',6:'SS',
                     7:'LF',8:'CF',9:'RF'}

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

#x,y from top left as origin going down
#gsBATTERZONES = [(0,0),(1,0),(2,0),
#                 (0,1),(1,1),(2,1),
#                 (0,2),(1,2),(2,2)]
gsSTRIKEZONE = range(9)
#gsBALLZONE = 9


#Hit Codes (Strings)
gsSINGLE = '1B'
gsDOUBLE = '2B'
gsTRIPLE = '3B'
gsHOMERUN = 'HR'
gsGROUNDOUT = 'GO'
gsAIROUT = 'AO'
gsSTRIKEOUT = 'SO'
gsWALK = 'BB'
gsHITBYPITCH = 'HBP'
gsINTENTIONALWALK = 'IBB'

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
