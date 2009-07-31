from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
#    (r'^updates/', include('Levitas.updates.urls')),
#    (r'^devices/', include('Levitas.devices.urls')),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/var/www/django/mlbfranchise/pics'}),
    (r'^leaders/', include('mlbfranchise.leaders.urls')),
    (r'^players/', include('mlbfranchise.players.urls')),
    (r'^admin/(.*)', admin.site.root),
)
