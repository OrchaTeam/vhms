from django.conf.urls import patterns, url
from config import views_settings as views_names

from apps.profiles import views as profiles


urlpatterns = patterns('',
    url(r'^profile/profile_settings/$',
        profiles.profile_update,
        name=views_names.VHMS_PROFILE_UPDATE),
    url(r'^profile/account_settings/$',
        profiles.password_change,
        name=views_names.VHMS_PROFILE_ACCOUNT_SETTINGS),

    # переопределенные вьюхи, формы и урлы
    url(r"^accounts/signup/$",
        profiles.signup,
        name=views_names.VHMS_PROFILE_SIGNUP),
    url(r"^accounts/login/$",
        profiles.signin,
        name=views_names.VHMS_PROFILE_LOGIN),
    url(r"^accounts/signup/verify/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$",
        profiles.signup_verify,
        name=views_names.VHMS_PROFILE_SIGNUP_VERIFY),
    url(r"^accounts/password/verify/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$",
        profiles.password_reset_verify,
        name=views_names.VHMS_PROFILE_PASSWORD_RESET_VERIFY),
    url(r"^accounts/password/change/$",
        profiles.password_change,
        name=views_names.VHMS_PROFILE_PASSWORD_CHANGE),
    url(r"^accounts/reset/$",
        profiles.password_reset,
        name=views_names.VHMS_PROFILE_PASSWORD_RESET),
    url(r"^accounts/logout/$",
        profiles.signout,
        name=views_names.VHMS_PROFILE_SIGNOUT),
)