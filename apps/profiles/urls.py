from django.conf.urls import patterns, url
from mezzanine.accounts import views

urlpatterns = patterns('',
    url(r'^profile/page/(?P<username>.*)/$', views.profile, {'template': 'profiles/profiles_profile.html'}, name="profile"),
    url(r'^profile/update/$', views.profile_update, {'template': 'profiles/profiles_update.html'}, name="profiles_update"),
)