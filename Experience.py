############################
#
#
#
# This file defines/describes the
# Model for how experience is accrued 
# by Players in the game. This is essentially boils down
# to how many XP players get for certain types of events
# 
# so an experience 'rule' or 'check' is a triple of the form:
# 
# (COND_OP, {CONDITION 1, CONDITION 2, ... CONDITION N}, INTEGER)
# 
# where:
#        COND_OP is in {AND, OR, NOR, XOR, NAND}
#
#        CONDITION is stat/attribute comparison that evalutes to a boolean
#      
#        INTEGER is a number of experients points to add
#
# FOR SIMPLICITY INITIALLY: 'XP Rules' will be ('python exp', INTEGER)
#
############################

#BATTING EXPEREINCE

#Simple XP - XP per stat

#Conditional XP - XP first time something happens or a threshold is met

# +1 for each at bat
gsXP_BATTER_ATBAT = 1

# +5 for each game played
gsXP_BATTER_GAMEPLAYED = 3

# +10 for each win
gsXP_BATTER_WIN = 10

# +1 for each base on a hit/walk
gsXP_BATTER_SINGLE = 1
gsXP_BATTER_WALK = 1
gsXP_BATTER_HBP = 1

gsXP_BATTER_DOUBLE = 2
gsXP_BATTER_TRIPLE = 3
gsXP_BATTER_HOMERUN = 4
#gsXP_IBB = 1

# +1 for each RBI
gsXP_BATTER_RBI = 1

# +1 
gsXP_BATTER_RUN = 1

gsXP_BATTER_GRANDSLAM = 5
# +5 for a grandslam

gsXP_BATTER_CYCLE = 5
# +5 for a cycle

#Conditional
# +1 for increasing longest hitstreak past 10 games


#STAT POINT Award
# +1 Stat Point for Breaking a game record
# +1 Stat Point for moving up on a leader board Top 100
 

#for each base get a point
#rule1 = totHits

