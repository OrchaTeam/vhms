from django.conf.urls import patterns, url
from mezzanine.accounts import views
#from .views import profile_view

urlpatterns = patterns('',
    url(r'^profile/(?P<username>.*)/$', views.profile, {'template': 'profiles/profiles_profile.html'}, name="profile"),
)