from django.conf.urls import patterns, url
from mezzanine.accounts import views as mezzanine

from apps.accounts.views import password_change

urlpatterns = patterns('',
    url(r'^profile/view/(?P<username>.*)/$', mezzanine.profile,
        {'template': 'profiles/profiles_profile.html'}, name="profile_view"),
    url(r'^profile/update/$', mezzanine.profile_update,
        {'template': 'profiles/profiles_update.html'}, name="profile_update"),
    url(r'^profile/settings/$', password_change, name="account_settings"),
)