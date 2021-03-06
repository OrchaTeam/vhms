from __future__ import unicode_literals
from django.conf import settings

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

from mezzanine.core.views import direct_to_template


admin.autodiscover()

urlpatterns = patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)

urlpatterns += i18n_patterns("",
    ("^admin/", include(admin.site.urls)),
)

urlpatterns += patterns('',
    url("^$", direct_to_template, {"template": "index.html"}, name="home"),

    ("^", include("mezzanine.urls")),

)

#handler404 = "mezzanine.core.views.page_not_found"
#handler500 = "mezzanine.core.views.server_error"