from django.conf.urls import url
from .blog import views

urlpatterns = [
    # Category
    url(r'^category/(?P<category>[-_a-zA-Z0-9]+)/$', views.view_category, name="view_category"),
    url(r'^category/(?P<category>[-_a-zA-Z0-9]+)/p/(?P<page>[0-9]+)/$', views.view_category, name="view_category"),
    # Single Post
    url(r'^(?P<year>[0-9]+)/(?P<mont>[0-9])+/(?P<slug>[-_a-zA-z0-9]+)/$', views.view_single_post, name="view_single_post")
]