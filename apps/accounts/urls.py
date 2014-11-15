from django.conf.urls import patterns, url
from mezzanine.accounts import views as mezzanine

urlpatterns = patterns('',



    url(r"^accounts/reset/$", mezzanine.password_reset, name="accounts_reset"),
    #url(r"^accounts/password/change/$", password_change, name="password_change"),




)