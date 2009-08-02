from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
#    (r'^updates/', include('Levitas.updates.urls')),
#    (r'^devices/', include('Levitas.devices.urls')),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/var/www/django/Franchise/pics'}),
    (r'^leaders/', include('Franchise.leaders.urls')),
    (r'^player/', include('Franchise.players.urls')),
    (r'^admin/', include('Franchise.admin.urls')),
)
