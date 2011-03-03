from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^objectconnect/', include('objectconnect.foo.urls')),

    (r'^accounts/logout/', 'django.contrib.auth.views.logout'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^socialregistration/', include('socialregistration.urls')),

    (r'^$', 'userconnect_generate_username.views.index'),
)
