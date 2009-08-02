# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, HttpResponse
import leagueleaders
import simplejson

def league_leaders(request, leader_level):
	ajax = request.GET.has_key('ajax')
	ll = leagueleaders.leagueleaders("./playersdb", "plr")
	if (ajax):
		print "AJAX"
		return HttpResponse(simplejson.dumps(ll), mimetype='application/javascript')
	print "NO AJAX"
	return render_to_response('leaders/index.html', {'leaders': ll})
