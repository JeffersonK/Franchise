from django.conf.urls.defaults import *

urlpatterns = patterns('Franchise.players.views',
	(r'^$', 'index'),
	(r'^(?P<player_id>\d+)/$', 'player_details'),
	(r'^(?P<player_id>\d+)/stats/$', 'player_incstats'),
	(r'^(?P<player_id>\d+)/friends/$', 'player_getfriends'),
)
