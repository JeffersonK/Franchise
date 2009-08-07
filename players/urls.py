from django.conf.urls.defaults import *

urlpatterns = patterns('Franchise.players.views',
	(r'^$', 'index'),
	(r'^(?P<player_id>\d+)/$', 'player_index'),
	(r'^(?P<player_id>\d+)/main/$', 'player_main'),
	(r'^(?P<player_id>\d+)/training/$', 'player_training'),
	(r'^(?P<player_id>\d+)/profile/$', 'player_profile'),
	(r'^(?P<player_id>\d+)/challenge/$', 'player_challenge'),
	(r'^(?P<player_id>\d+)/stats/$', 'player_stats'),
	(r'^(?P<player_id>\d+)/headerstats/$', 'player_headerstats'),
	(r'^(?P<player_id>\d+)/stats/(?P<stat_id>\d+)/$', 'player_incstats'),
	(r'^(?P<player_id>\d+)/training/(?P<training_id>\d+)/$', 'player_inctraining'),
#add create player
)
