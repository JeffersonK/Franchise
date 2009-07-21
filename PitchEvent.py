import random
import os

GENERATE = 0

def genQuadrantEvents(n=1000):
    i = 0
    QuadrantEvents = []
    while i < n:
        QuadrantEvents += [random.randint(0,9)]
        i += 1
    
    return QuadrantEvents

swings = []
pitches = []
if GENERATE:
    pitches = genQuadrantEvents()
    swings = genQuadrantEvents()

    file = open("pitch.loc", "w+")
    file.write(str(PitchEventLocations)+"\n")
    file.close()

    file = open("swing.loc", "w+")
    file.write(str(SwingEventLocations)+"\n")
    file.close()


file = open("pitch.loc", "r")
pitches = file.readline()
file.close()
pitches = eval(pitches)

file = open("swing.loc", "r")
swings = file.readline()
file.close()
swings = eval(swings)

#cnt = 0
for i in range(len(pitches)):
    if pitches[i] == swings[i]:
        
#print "hit %d\n" % pitches[i]

#        cnt += 1
#print "%d matches\n" % cnt

