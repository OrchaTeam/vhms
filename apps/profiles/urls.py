from django.conf.urls import patterns, url
#from .views import profile_view

urlpatterns = patterns('',
    url(r'^profile/(?P<username>\w+)/$', 'mezzanine.accounts.views.profile', name="profiles_profile"),
)