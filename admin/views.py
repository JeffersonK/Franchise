# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import os
import ObjectDB
import sys
from Globals import *

gsPlayerDB = None

def header():
	global gsPlayerDB
	if gsPlayerDB == None:
		gsPlayerDB = ObjectDB.ObjectDB("./playersdb", "plr")

def index(request):
	return render_to_response('admin/index.html')

def player_details(request, player_id):
	global gsPlayerDB
	header()	
	#p = get_object_or_404(Poll, pk=poll_id)
	p = gsPlayerDB.getObjectHandle(player_id)
	f = gsPlayerDB.getAllObjectGUIDs("./playersdb", "plr")
	#l = gsPlayerDB.getLineup
	del(gsPlayerDB)
	gsPlayerDB = None
	pitcher = [-1]
	l = [-1,0,1,2,3,4,5,6,7]
	
	return render_to_response('admin/detail.html', {'player': p, 'friends': f, 'pitcher': pitcher, 'lineup': l})

def edit_player(request, player_id):
	global gsPlayerDB
	header()
	result = ''
	p = gsPlayerDB.getObjectHandle(player_id)
	#print p
	#print 
	if request.method == 'POST':
		#form = forms.Form(request.POST)
		#if form.is_valid():
		try:
			position = request.POST['Position']
			#experience = request.POST['Experience']
			energy = request.POST['Energy']
			wins = request.POST['Wins']
			losses = request.POST['Losses']
			maxEnergy = request.POST['MaxEnergy']
			energy = request.POST['Energy']

			#Batter/Pitcher Pitch Mastery
			fastball = request.POST['Fastball']
			curveball = request.POST['Curveball']
			slider = request.POST['Slider']
			changeup = request.POST['Changeup']
			knuckleball = request.POST['Knuckleball']
			sinker = request.POST['Sinker']
			spitball = request.POST['Spitball']
			forkball = request.POST['Forkball']
			pitchMastery = {gsFASTBALL:fastball,
					gsCURVEBALL:curveball, 
			                gsSLIDER:slider,
			                gsCHANGEUP:changeup, 
		        	        gsKNUCKLEBALL:knuckleball, 
			                gsSINKER:sinker, 
			                gsSPITBALL:spitball,
			                gsFORKBALL:forkball}
			x="""	
			#Batter/Pitcher Zone Mastery	
			zone0 = request.POST['zone0']
			zone1 = request.POST['zone1']
			zone2 = request.POST['zone2']
			zone3 = request.POST['zone3']
			zone4 = request.POST['zone4']
			zone5 = request.POST['zone5']
			zone6 = request.POST['zone6']
			zone7 = request.POST['zone7']
			zone8 = request.POST['zone8']
			zoneMastery = [zone0,zone1,zone2,zone3,zone4,zone5,zone6,zone7,zone8]

			pzone0 = request.POST['pzone0']
			pzone1 = request.POST['pzone1']
			pzone2 = request.POST['pzone2']
			pzone3 = request.POST['pzone3']
			pzone4 = request.POST['pzone4']
			pzone5 = request.POST['pzone5']
			pzone6 = request.POST['pzone6']
			pzone7 = request.POST['pzone7']
			pzone8 = request.POST['pzone8']
			powerZone = [pzone0,pzone1,pzone2,pzone3,pzone4,pzone5,pzone6,pzone7,pzone8]
			"""


		except:
			print "Unexpected error:", sys.exc_info()[0]

			return render_to_response('admin/detail.html', {
			'player': p,
			'error_message': "Error in Form.  Please Try again",
        		})
				#return HttpResponseRedirect(reverse('Franchise.players.views.player_details', args=(player_id)))
		
		else:
			if (p.getPosition() == "P"):
				print "Pitcher: "
				result += str(p.getPlayerAbilities().setPitchingPitchMasteryMatrix(pitchMastery))
				#result += str(p.getPlayerAbilities().setPitchingZoneMasteryMatrix(zoneMastery))
			else:
				print "Batter: "
				patience = request.POST['Patience']
				result += str(p.getPlayerAbilities().setPatience(patience))
				result += str(p.getPlayerAbilities().setBattingPitchMasteryMatrix(pitchMastery))
				#result += str(p.getPlayerAbilities().setBattingZoneMasteryMatrix(zoneMastery))
				result += str(p.getPlayerAbilities().setBattingPowerZones(powerZone))

			#p.setPosition(position)
			#p.setExperience(experience)
			#p.setEnergy(energy)
			
			energyChange = int(energy) - int(p.getEnergy())
			maxEnergyChange = int(maxEnergy) - int(p.getMaxEnergy())
			p.increaseEnergy(energyChange)
			#p.increaseMaxEnergy(maxEnergyChange)


			if (result.find('-') > -1):
				return render_to_response('admin/detail.html', {
				'player': p,
				'error_message': result,
        			})
			else:
				gsPlayerDB.write(player_id)
				del(gsPlayerDB)
				gsPlayerDB = None

				# Always return an HttpResponseRedirect after successfully dealing
				# with POST data. This prevents data from being posted twice if a
				# user hits the Back button.

				#return render_to_response('players/detail.html', {'player': p})
       
                                #return ('players/detail.html', { 'player': p }, 'error_message': '',})
				return HttpResponseRedirect(reverse('Franchise.admin.views.player_details', args =(player_id,)))
		#else:
		#	return render_to_response('players/detail.html', {
		#	'player': p,
		#	'error_message': "Error in Form.  NOT VALID!!!!Please Try again",
        	#	})
	else:
		return HttpResponseRedirect(reverse('Franchise.admin.views.player_details', args=(player_id,)))


def adjust_lineup(request,player_id,lineup_id,friend_id,move_action):
	global gsPlayerDB
	header()
	p = gsPlayerDB.getObjectHandle(player_id)
	l = [-1,0,1,2,3,4,5,6,7]
	pitcher = [0]
	f = gsPlayerDB.getAllObjectGUIDs("./playersdb", "plr")

	lineup_id = int(lineup_id)
	lineup_id_left = int(lineup_id)-1
	lineup_id_right = int(lineup_id)+1
	if(int(lineup_id_right) == 9):
		lineup_id_right = 0
	tmp = l[:]

	if(move_action == "left"):
		l[lineup_id] = tmp[lineup_id_left]
		l[lineup_id_left] = tmp[lineup_id]	
	elif(move_action == "right"):
		l[lineup_id] = tmp[lineup_id_right]
		l[lineup_id_right] = tmp[lineup_id]	
	elif(move_action == "remove"):
		l[lineup_id] = 0
	elif(move_action == "add"):
		if(-1 in l):
			l[l.index(-1)] = friend_id
		else:
			return render_to_response('admin/detail.html', {
			'player': p,
			'friends': f,
			'pitcher': pitcher,
			'lineup': l,
			'error_message': "Lineup Full.  Remove a Player before you can Add someone to your Lineup",
			})
	else:
		return render_to_response('admin/detail.html', {
		'player': p,
		'friends': f,
		'pitcher': pitcher,
		'lineup': l,
		'error_message': "Bad Move Action",
       		})

	print "Lineup: "+str(l)
	
	return render_to_response('admin/detail.html', {'player': p, 'friends': f, 'pitcher': pitcher, 'lineup': l})

#	return HttpResponseRedirect(reverse('Franchise.players.views.player_details', args=(player_id,)))


def adjust_pitcher(request,player_id,friend_id,move_action):
	global gsPlayerDB
	header()
	p = gsPlayerDB.getObjectHandle(player_id)
	l = [0,1,2,3,4,5,6,7,8]
	pitcher = [0]
	f = gsPlayerDB.getAllObjectGUIDs("./playersdb", "plr")

	if(move_action == "remove"):
		pitcher=[-1]
	elif(move_action == "add"):
		pitcher=[friend_id]
	else:
		return render_to_response('admin/detail.html', {
		'player': p,
		'friends': f,
		'pitcher': pitcher,
		'lineup': l,
		'error_message': "Bad Move Action",
       		})
	
	return render_to_response('admin/detail.html', {'player': p, 'friends': f, 'pitcher': pitcher, 'lineup': l})
