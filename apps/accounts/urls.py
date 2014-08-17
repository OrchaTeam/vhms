from django.conf.urls import patterns, url

from .views import password_change, password_reset_verify

urlpatterns = patterns('',
    url(r"^accounts/login/$", 'mezzanine.accounts.views.login', name="accounts_login"),
    url(r"^accounts/logout/$", 'mezzanine.accounts.views.logout', name="accounts_logout"),
    url(r"^accounts/signup/$", 'mezzanine.accounts.views.signup', name="accounts_signup"),
    url(r"^accounts/reset/$", 'mezzanine.accounts.views.password_reset', name="accounts_reset"),
    url(r"^accounts/password/change/$", password_change, {'template': 'accounts/account_password_change.html'}, name="password_change"),
    url(r"^accounts/password/verify/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$", password_reset_verify, name="password_reset_verify"),
)