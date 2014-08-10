from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r"^accounts/login/$", 'mezzanine.accounts.views.login', name="accounts_login"),
    url(r"^accounts/logout/$", 'mezzanine.accounts.views.logout', name="accounts_logout"),
    url(r"^accounts/signup/$", 'mezzanine.accounts.views.signup', name="accounts_signup"),
    url(r"^accounts/reset/$", 'mezzanine.accounts.views.password_reset', name="accounts_reset"),
)