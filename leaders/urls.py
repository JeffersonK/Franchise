from django.conf.urls.defaults import *

urlpatterns = patterns('Franchise.leaders.views',
	(r'^(?P<leader_level>\w+)/$', 'league_leaders'),
)
