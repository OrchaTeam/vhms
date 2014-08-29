from __future__ import unicode_literals
from django.conf import settings

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

from mezzanine.core.views import direct_to_template

admin.autodiscover()

# Tech
urlpatterns = patterns("",
    (r"^static/(?P<path>.*)$", 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)

# Admin
urlpatterns += i18n_patterns("",
    ("^admin/", include(admin.site.urls)),
)

# Include
urlpatterns += patterns("", 
    url(r"^", include("apps.accounts.urls", app_name="accounts")),
    url(r"^", include("apps.profiles.urls", app_name="profiles")),
)

# Overall
urlpatterns += patterns('',
    url("^$", direct_to_template, {"template": "index.html"}, name="home"),
    url("^main/$", direct_to_template, {"template": "main.html"}, name="home"),
    ("^", include("mezzanine.urls")),

)

#handler404 = "mezzanine.core.views.page_not_found"
#handler500 = "mezzanine.core.views.server_error"