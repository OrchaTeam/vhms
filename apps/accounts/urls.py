from django.conf.urls import patterns, url
from mezzanine.accounts import views as mezzanine

from .views import password_reset_verify, password_change

urlpatterns = patterns('',
    url(r"^accounts/login/$", mezzanine.login, name="accounts_login"),
    url(r"^accounts/logout/$", mezzanine.logout, name="accounts_logout"),
    url(r"^accounts/signup/$", mezzanine.signup, name="accounts_signup"),
    url(r"^accounts/reset/$", mezzanine.password_reset, name="accounts_reset"),
    url(r"^accounts/password/change/$", password_change, name="password_change"),
    url(r"^accounts/password/verify/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$", password_reset_verify, name="password_reset_verify"),
)