from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage
from django.core.cache import cache
from .models import Entry, Category
from fifastats.scrapper import FifaScrapper

# Create your views here.
def view_category(request, slug=None, page=1):
    category_model = get_object_or_404(Category, slug=slug)

    post_models = cache.get('entries_category_v2_{0}'.format(category_model.id))
    if not post_models:
        post_models = Entry.objects.select_related('author', 'category').filter(category=category_model, active=True).order_by('-order')
        cache.set('entries_category_{0}'.format(category_model.id), post_models, 60*15)

    post_paginator = Paginator(post_models, 20)

    try:
        page = int(page)
        post_page = post_paginator.page(page)
    except EmptyPage:
        raise Http404

    sc = FifaScrapper()

    return render(request, "desktop/blog/category.html", {"paginator": post_paginator, "page": post_page, "p": page, "page_top_post": post_page.object_list[:3], "category": category_model, "fifa": sc})


def view_tag(request, tag=None, page=1):
    post_models = cache.get('entries_tag_v2_{0}'.format(tag))
    if not post_models:
        post_models = Entry.objects.select_related('author', 'category').filter(tags__slug__in=[tag], active=True)
        cache.set('entries_tag_{0}'.format(category_model.id), post_models, 60*15)

    post_paginator = Paginator(post_models, 20)

    try:
        post_page = post_paginator.page(page)
    except EmptyPage:
        raise Http404

    return render(request, "desktop/blog/tag.html", {"paginator": post_paginator, "page": post_page})


def view_single_post(request, year=None, month=None, slug=None):
    post = cache.get('entry_{0}_v4'.format(slug))
    if not post:
        try:
            post = Entry.objects.select_related('author', 'category').get(date__year=year, date__month=month, slug=slug)
        except:
            raise Http404
        cache.set('entry_{0}_v4'.format(slug), post, 60 * 5)

    sc = FifaScrapper()

    return render(request, "desktop/blog/single.html", {"post": post, "fifa": sc})
