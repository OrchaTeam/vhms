from django.conf.urls import patterns, url
from apps.config import settings

from apps.profiles import views as profiles


urlpatterns = patterns('',
    url(r'^profile/update/$',
        profiles.profile_update,
        name=settings.VHMS_PROFILE_UPDATE),
    url(r'^profile/settings/$',
        profiles.password_change,
        name=settings.VHMS_PROFILE_ACCOUNT_SETTINGS),

    # переопределенные вьюхи, формы и урлы
    url(r"^accounts/signup/$",
        profiles.signup,
        name=settings.VHMS_PROFILE_SIGNUP),
    url(r"^accounts/login/$",
        profiles.signin,
        name=settings.VHMS_PROFILE_LOGIN),
    url(r"^accounts/signup/verify/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$",
        profiles.signup_verify,
        name=settings.VHMS_PROFILE_SIGNUP_VERIFY),
    url(r"^accounts/password/verify/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$",
        profiles.password_reset_verify,
        name=settings.VHMS_PROFILE_PASSWORD_RESET_VERIFY),
    url(r"^accounts/password/change/$",
        profiles.password_change,
        name=settings.VHMS_PROFILE_PASSWORD_CHANGE),
    url(r"^accounts/reset/$",
        profiles.password_reset,
        name=settings.VHMS_PROFILE_PASSWORD_RESET),
    url(r"^accounts/logout/$",
        profiles.signout,
        name=settings.VHMS_PROFILE_SIGNOUT),
)