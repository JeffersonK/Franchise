

#################
#
#
#################
import time
class SimRunner:

    def __init__(self, SimObject, isRunning=False):

        #random.seed()
        self.__isRunning = isRunning
        self.__simObject = SimObject

        self.__startTime = None
        self.__finTime = None

    def startSimTimer(self):
        self.__startTime = time.time()
        return

    def stopSimTimer(self):
        if self.__startTime == None:
            return -1.0

        self.__finTime = time.time()
        return self.__finTime - self.__startTime

    #######
    #
    #Run the game simulation forward nsteps
    #######
    def step(self, nsteps=1):

        i = 0
        events = []
        if not self.__isRunning:
            events += self.__simObject.initSim()
            self.__isRunning = not self.__isRunning

        """if nsteps == -1: #run to done

            while 1:
                self.__simObject.stepSim()
                print self.__simObject
                if self.__simObject.isSimDone():
                    self.__simObject.finishSim()
                    return i
                i += 1
                
        else:"""

        while i < nsteps:
            events = self.__simObject.stepSim()
            #DEBUG
            #print self.__simObject
            if self.__simObject.isSimDone():
                events += self.__simObject.finishSim()
                return events
            i += 1
        
        return events


##########
#
#
#
##########
def main():
    
    #sim = SimRunner(
    return


if __name__ == "__main__":
    main()
