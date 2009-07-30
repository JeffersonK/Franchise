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

gsMIN_XP_PER_GAME = 10
gsMAX_XP_PER_GAME = 250
#BATTING EXPEREINCE

#Simple XP - XP per stat

#Conditional XP - XP first time something happens or a threshold is met

#Want to heavily weight individual stats 
gsXP_BATTER_ATBAT = 1
gsXP_BATTER_GAMEPLAYED = 1
gsXP_BATTER_WIN = 1

# +n for each base on a hit/walk
gsXP_BATTER_SINGLE = 10
gsXP_BATTER_DOUBLE = 20
gsXP_BATTER_TRIPLE = 30
gsXP_BATTER_HOMERUN = 40
gsXP_BATTER_WALK = 10
gsXP_BATTER_HBP = 10
#gsXP_IBB = 10
gsXP_BATTER_RBI = 10
gsXP_BATTER_RUN = 3

#BATTER EXP BONUSES
#gsXP_BATTER_GRANDSLAM = 50 #this is added on top of HR
gsXP_BATTER_CYCLE = 50
# +1 for increasing longest hitstreak past 10 games

#PITCHER EXP POINTS
gsXP_PITCHER_START = 50
gsXP_PITCHER_K = 1
#gsXP_PITCHER_SHUTOUT = 200
#gsXP_PITCHER_NOHITTER = 1000
#gsXP_PITCHER_WIN = 100
gsXP_PITCHER_OUT = 1

gsXP_PITCHER_EARNEDRUN = -4
gsXP_PITCHER_HITALLOWED = -2
gsXP_PITCHER_WALKSTHROWN = -1


#Conditional



#STAT POINT Award
# +1 Stat Point for Breaking a game record
# +1 Stat Point for moving up on a leader board Top 100
 



