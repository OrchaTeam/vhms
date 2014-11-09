from django.conf.urls import patterns, url
from mezzanine.accounts import views as mezzanine

from apps.profiles.views import signup, signup_verify, password_change, password_reset_verify

urlpatterns = patterns('',
    url(r'^profile/view/(?P<username>.*)/$', mezzanine.profile,
        {'template': 'profiles/profiles_profile.html'}, name="profile_view"),
    url(r'^profile/update/$', mezzanine.profile_update,
        {'template': 'profiles/profiles_update.html'}, name="profile_update"),
    url(r'^profile/settings/$', password_change, name="account_settings"),

    # переопределенные вьюхи, формы и урлы
    url(r"^accounts/signup/$", signup, name="accounts_signup"),
    url(r"^accounts/signup/verify/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$",
        signup_verify, name="signup_verify"),
    url(r"^accounts/password/verify/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$", password_reset_verify, name="password_reset_verify"),
    url(r"^accounts/password/change/$", password_change, name="password_change"),
)