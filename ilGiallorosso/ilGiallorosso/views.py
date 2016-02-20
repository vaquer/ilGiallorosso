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

    total_post = cache.get('home_posts_v5')

    if not total_post:
        total_post = Entry.objects.select_related('author', 'category').filter(active=True).order_by('-order')
        cache.set('home_posts_v5', total_post, 60 * 10)

    paginator_object = Paginator(total_post, 20)

    try:
        p = int(p)
        page = paginator_object.page(p)
    except:
        raise Http404

    top_entries = page.object_list[:3]
    oldie_entries = page.object_list[3:]
    return render(request, 'desktop/home.html', {'settings': settings, 'fifa': sc, 'oldie_entries': oldie_entries, 'top_entries': top_entries, 'page': page, 'paginator': paginator_object})


def stats(request):
    sc = FifaScrapper()
    return render(request, 'desktop/estadisticas.html', {'fifa': sc, "settings": settings})
