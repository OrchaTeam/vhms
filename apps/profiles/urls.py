from django.conf.urls import patterns, url

from apps.profiles import views as profiles

urlpatterns = patterns('',
    url(r'^profile/update/$',
        profiles.profile,
        {'template': "profiles/profiles_update.html"},
        name="profile_update"),
    url(r'^profile/settings/$',
        profiles.password_change,
        name="account_settings"),

    # переопределенные вьюхи, формы и урлы
    url(r"^accounts/signup/$",
        profiles.signup,
        name="accounts_signup"),
    url(r"^accounts/login/$",
        profiles.signin,
        name="accounts_login"),
    url(r"^accounts/signup/verify/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$",
        profiles.signup_verify,
        name="signup_verify"),
    url(r"^accounts/password/verify/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$",
        profiles.password_reset_verify,
        name="password_reset_verify"),
    url(r"^accounts/password/change/$",
        profiles.password_change,
        name="password_change"),
    url(r"^accounts/reset/$",
        profiles.password_reset,
        name="accounts_reset"),
    url(r"^accounts/logout/$",
        profiles.signup,
        name="accounts_logout"),
)