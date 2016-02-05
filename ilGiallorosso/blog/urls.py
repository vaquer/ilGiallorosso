from django.conf.urls import url
from . import views

urlpatterns = [
    # Category
    url(r'^category/(?P<slug>[-_a-zA-Z0-9]+)/$', views.view_category, name="view_category"),
    url(r'^feed/$', views.view_redgol_feed, name="view_redgol_feed"),
    url(r'^category/(?P<slug>[-_a-zA-Z0-9]+)/p/(?P<page>[0-9]+)/$', views.view_category, name="view_category_page"),
    # Single Post
    url(r'^(?P<year>[0-9]+)/(?P<month>[0-9])+/(?P<slug>[-_a-zA-z0-9]+)/$', views.view_single_post, name="view_single_post"),
    # Tags
    url(r'^tag/(?P<slug>[-_a-zA-Z0-9]+)/$', views.view_tag, name="view_tag"),
    url(r'^tag/(?P<slug>[-_a-zA-Z0-9]+)/p/(?P<page>[0-9]+)/$', views.view_tag, name="view_tag"),
]
