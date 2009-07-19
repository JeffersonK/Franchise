

#################
#
#
#################
class SimRunner:

    def __init__(self, SimObject, isRunning=False):

        #random.seed()
        self.__isRunning = isRunning
        self.__simObject = SimObject

    #######
    #
    #Run the game simulation forward nsteps
    #######
    def run(self, nsteps=1):

        i = 0
        if not self.__isRunning:
            self.__simObject.initSim()
            self.__isRunning = not self.__isRunning

        if nsteps == -1: #run to done

            while 1:
                self.__simObject.stepSim()
                print self.__simObject
                if self.__simObject.isSimDone():
                    self.__simObject.finishSim()
                    return i
                i += 1
                
        else:

            while i < nsteps:
                self.__simObject.stepSim()
                if self.__simObject.isSimDone():
                    self.__simObject.finishSim()
                    return i
                i += 1
        
        return i


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
