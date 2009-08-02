from django.conf.urls.defaults import *

urlpatterns = patterns('Franchise.admin.views',
	(r'^$', 'index'),
	(r'^player/(?P<player_id>\d+)/$', 'player_details'),
	(r'^player/(?P<player_id>\d+)/edit/$', 'edit_player'),
	(r'^player/(?P<player_id>\d+)/lineup/batter/adjust/(?P<lineup_id>\d+)/(?P<friend_id>\d+)/(?P<move_action>\w+)/$', 'adjust_lineup'),
	(r'^player/(?P<player_id>\d+)/lineup/pitcher/adjust/(?P<friend_id>\d+)/(?P<move_action>\w+)/$', 'adjust_pitcher'),
)
