from django.conf.urls import patterns, url
from config import views_settings as views_names

urlpatterns = patterns('',
    url(r'^showroom/category/$',
        showroom.category_view,
        name=views_names.VHMS_SHOWROOM_CATEGORY)
    )
