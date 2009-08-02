# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import HttpResponse
import ServerAPI as API
import leagueleaders
from Globals import *
import simplejson

def index(request):
	return render_to_response('player/index.html')

def player_details(request, player_id):
	pitcher = [-1]
	l = [-1,0,1,2,3,4,5,6,7]
	ajax = request.GET.has_key('ajax')

	player_json = API.ServerAPIGetPlayerState(player_id)[1:-1]
	friends_json = API.ServerAPIGetLineupCandidates(player_id)
	player = simplejson.dumps(player_json)
	friends = simplejson.dumps(friends_json)
	position = player_json[player_json.find("position")+11]
        if (ajax):
	        return HttpResponse(player_json, mimetype='application/javascript')
	return render_to_response('players/detail.html', {'guid': player_id, 'position': position, 'player': player, 'friends': friends, 'pitcher': pitcher, 'lineup': l})

def player_incstats(request, player_id):
	ajax = request.GET.has_key('ajax')
	stat = request.GET['stat_name']
	print stat
	result = API.ServerAPIUseStatPoint(player_id, stat)
	print result
	player_json = API.ServerAPIGetPlayerState(player_id)[1:-1]
	if (ajax):
		print "AJAX"
	        return HttpResponse(player_json, mimetype='application/javascript')
	
	print "NO AJAX"
	return render_to_response('players/index.html')
