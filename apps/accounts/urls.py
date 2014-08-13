from django.conf.urls import patterns, url
from mezzanine.accounts import views

urlpatterns = patterns('',
    url(r"^accounts/login/$", 'mezzanine.accounts.views.login', name="accounts_login"),
    url(r"^accounts/logout/$", 'mezzanine.accounts.views.logout', name="accounts_logout"),
    url(r"^accounts/signup/$", views.signup, name="accounts_signup"),
    url(r"^accounts/reset/$", 'mezzanine.accounts.views.password_reset', name="accounts_reset"),
    #url(r"^accounts/password/$", views.password_change, {'template': 'accounts/account_password_change.html'}, name="password_change"),
)