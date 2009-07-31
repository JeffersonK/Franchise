from django.conf.urls.defaults import *

urlpatterns = patterns('mlbfranchise.leaders.views',
	(r'^(?P<leader_level>\w+)/$', 'league_leaders'),
)
