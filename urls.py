from __future__ import unicode_literals
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

from mezzanine.core.views import direct_to_template


admin.autodiscover()

# Tech
urlpatterns = patterns("",
    (r"^static/(?P<path>.*)$", 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Admin
urlpatterns += i18n_patterns("",
    ("^admin/", include(admin.site.urls)),
)

# Include
urlpatterns += patterns("", 
    url(r"^", include("apps.profiles.urls", app_name="profiles")),
)

# Overall
urlpatterns += patterns('',
    url("^$", direct_to_template, {"template": "index.html"}, name=VHMS_CORE_HOME),
    url("^main/$", direct_to_template, {"template": "main.html"}, name=VHMS_CORE_TEST_HOME),
)

# Static
urlpatterns += staticfiles_urlpatterns()

#handler404 = "mezzanine.core.views.page_not_found"
#handler500 = "mezzanine.core.views.server_error"