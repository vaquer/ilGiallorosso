from django.shortcuts import render
from django.conf import settings
from django.core.paginator import Paginator
from django.core.cache import cache
from django.http import Http404

from fifastats.scrapper import FifaScrapper
from blog.models import Entry



def index(request, p=1):
    sc = FifaScrapper()
    return render(request, 'desktop/index.html', {'fifa': sc})


def home(request, p=1):
    sc = FifaScrapper()

    total_post = cache.get('home_posts')

    if not total_post:
        total_post = Entry.objects.all().order_by('-order')
        cache.set('home_posts', total_post, 60 * 10)

    paginator_object = Paginator(total_post, 10)

    try:
        p = int(p)
    except:
        raise Http404
    page = paginator_object.page(p)

    if p == 1:
        top_entries = page.object_list[:3]
        oldie_entries = page.object_list[3:]
        return render(request, 'desktop/home.html', {'fifa': sc, 'oldie_entries': oldie_entries, 'top_entries': top_entries})
    else:
        return render(request, 'desktop/home_paginator.html', {'fifa': sc, 'page': page, 'paginator': paginator_object})


def single_test(request):
    sc = FifaScrapper()
    return render(request, 'desktop/single_test.html', {'fifa': sc})
