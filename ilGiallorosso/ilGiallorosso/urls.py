"""ilGiallorosso URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
import autocomplete_light.shortcuts as al

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import generic
from autocomplete_light.compat import url, urls

from blog.models import Tag
from blog.forms import EntryFormAutocomplete

admin.site.site_header = 'Noticias Roma - Administracion'
# admin.site.index_title = 'Casas Atlas | Administracion'
admin.site.site_title = 'Noticias Roma'

urlpatterns = [
    url(r'TagAutocomplete/', include('autocomplete_light.urls'), name='autocomplete'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^robots.txt', TemplateView.as_view(template_name='desktop/robots.txt', content_type='text/plain')),
    url(r'^', include('blog.urls')),
    # url(r'^', include('awesome_gallery.urls')),
    url(r'^$', 'ilGiallorosso.views.home'),
    url(r'^p/(?P<p>[0-9]+)/$', 'ilGiallorosso.views.home'),
    url(r'^single/$', 'ilGiallorosso.views.single_test')
]
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
