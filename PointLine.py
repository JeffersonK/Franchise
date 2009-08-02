import math
import random
#from pygooglechart import ScatterChart

DEBUG_POINTLINE_INTERSECT = 0

def sphericalCoordsToCartesian(playerLoc):
    #print playerLoc
    thetaPlayer, rPlayer = playerLoc
    YplyrField = rPlayer * math.sin(thetaPlayer)
    XplyrField = rPlayer * math.cos(thetaPlayer)
    #print "Player XY (%d,%d)" % (XplyrField, YplyrField)
    return (XplyrField, YplyrField)

def distance(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2

    return float(math.sqrt((x2 - x1)**2 + (y2-y1)**2))
    
    
def PointLineIntersect(hitCoord=(math.radians(10.0),250.0), 
                       playerCoord=(math.radians(15.0),250.0)):

    thetaHit = math.radians(hitCoord[0])
    rHit = hitCoord[1]

    thetaPlayer = math.radians(playerCoord[0])
    rPlayer = playerCoord[1]

    #thetaHit = math.radians(14.0)
    #rHit = 300.0

    #thetaPlayer = math.radians(15.0)
    #rPlayer = 240.0
    #playerRange = 75.0

    YhitField = (rHit * math.sin(thetaHit))
    XhitField = -(rHit * math.cos(thetaHit))

    YplyrField = (rPlayer * math.sin(thetaPlayer))
    XplyrField = -(rPlayer * math.cos(thetaPlayer))

        
    (x1,y1) = (0.0,0.0)

    (x2,y2) = (XhitField, YhitField)

    (x3,y3) = (XplyrField, YplyrField)


    u = ((x3-x1)*(x2-x1) + (y3-y1)*(y2-y1)) / ((x2-x1)**2 + (y2-y1)**2)

    x = x1 + u * (x2-x1)
    y = y1 + u * (y2-y1)

    d = math.sqrt( (x-XplyrField)**2 + (y-YplyrField)**2 )
    if u < 0.0 or u > 1.0:
        if DEBUG_POINTLINE_INTERSECT:   
            print "Closest point does not fall within line segment"
            print "Hit XY (%d,%d)" % (XhitField, YhitField)
            print "Player XY (%d,%d)" % (XplyrField, YplyrField)
            print "u:%f" % u
            print "XY-Coord(Closest Point): (%f, %f)" % (x, y)
            print "Min Distance: %f" % d

        return (False, d)

    if DEBUG_POINTLINE_INTERSECT:   
            print "Hit XY (%d,%d)" % (XhitField, YhitField)
            print "Player XY (%d,%d)" % (XplyrField, YplyrField)
            print "u:%f" % u
            print "XY-Coord(Closest Point): (%f, %f)" % (x, y)
            print "Min Distance: %f" % d
            
    return (True, d)

TEST="""def plotDefense(playerLocs=gsDEFAULT_PLAYER_LOCS):
    xlist = []
    ylist = []
    rlist = []
    for plyr in playerLocs:
        x, y = playerSphericalCoordsToCartesian(plyr)
        xlist.append(x)
        ylist.append(y)


        chart = ScatterChart(500, 250, 
                             x_range=(0, 100), y_range=(0, 100))
        chart.add_data(xlist)
        chart.add_data(ylist)
        chart.add_data([800]*3)
        chart.download('scatter-defense.png')"""

def main():
    PointLineIntersect()    
    #plotDefense()

if __name__ == '__main__':
    main()



