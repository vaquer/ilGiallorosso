from django.shortcuts import render
from django.conf import settings
from django.core.paginator import Paginator
from django.core.cache import cache
from django.http import Http404

from fifastats.scrapper import FifaScrapper
from blog.models import Entry


def home(request, p=1):
    sc = FifaScrapper()
    top_entries = None
    oldie_entries = None
    fichajes = None

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

    if p == 1:
        key_fichajes = 'post_category_fichajes'
        fichajes = cache.get(key_fichajes)
        if not fichajes:
            fichajes = Entry.objects.select_related('author', 'category').filter(category__slug='mercado-de-fichajes').order_by('-date')[:5]
            cache.set(key_fichajes, fichajes, 60 * 10)

        top_entries = page.object_list[:5]
        oldie_entries = page.object_list[5:]

    key_romatv = 'post_roma_tv'
    roma_tv = cache.get(key_romatv)
    if not roma_tv:
        roma_tv = Entry.objects.select_related('author', 'category').filter(category__slug='roma-tv').order_by('-date')[:5]
        cache.set(key_romatv, roma_tv, 60 * 10)


    return render(request, 'desktop/v2/home.html', {'settings': settings, 'fifa': sc, 'oldie_entries': oldie_entries, 'top_entries': top_entries, 'page': page, 'paginator': paginator_object, 'fichajes': fichajes, 'roma_tv': roma_tv})


def stats(request):
    sc = FifaScrapper()
    return render(request, 'desktop/estadisticas.html', {'fifa': sc, "settings": settings})
