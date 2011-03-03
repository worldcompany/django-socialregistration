from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^objectconnect/', include('objectconnect.foo.urls')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^socialregistration/', include('socialregistration.urls')),

    (r'^$', 'objectconnect.views.index'),
    (r'^2/$', 'objectconnect.views.index2'),
)
