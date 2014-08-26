from django.conf.urls import patterns, url
from mezzanine.accounts import views

from apps.accounts.views import password_change

urlpatterns = patterns('',
    url(r'^profile/view/(?P<username>.*)/$', views.profile, 
        {'template': 'profiles/profiles_profile.html'}, name="profile"),
    url(r'^profile/update/$', views.profile_update, 
        {'template': 'profiles/profiles_update.html'}, name="profiles_update"),
    url(r'^profile/settings/$', password_change, 
        {'template': 'profiles/profiles_account_settings.html'}, name="account_settings"),
)