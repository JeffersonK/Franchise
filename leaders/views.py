# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
import leagueleaders

def league_leaders(request, leader_level):
	print leader_level
	ll = leagueleaders.leagueleaders("/home/frank/src/Franchise/players", "plr")
	print ll
	return render_to_response('leaders/index.html', {'leaders': ll})
