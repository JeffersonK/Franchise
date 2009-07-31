from django.conf.urls.defaults import *

urlpatterns = patterns('Franchise.players.views',
	(r'^$', 'index'),
	(r'^(?P<player_id>\d+)/$', 'player_details'),
	(r'^(?P<player_id>\d+)/edit/$', 'edit_player'),
	(r'^(?P<player_id>\d+)/lineup/batter/adjust/(?P<lineup_id>\d+)/(?P<friend_id>\d+)/(?P<move_action>\w+)/$', 'adjust_lineup'),
	(r'^(?P<player_id>\d+)/lineup/pitcher/adjust/(?P<friend_id>\d+)/(?P<move_action>\w+)/$', 'adjust_pitcher'),
)
