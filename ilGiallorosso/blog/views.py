from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage
from .models import Entry, Category
from fifastats.scrapper import FifaScrapper

# Create your views here.
def view_category(request, slug=None, page=1):
    category_model = get_object_or_404(Category, slug=slug)
    post_models = Entry.objects.filter(category=category_model).order_by('-order')

    post_paginator = Paginator(post_models, 10)

    try:
        page = int(page)
        post_page = post_paginator.page(page)
    except EmptyPage:
        raise Http404

    sc = FifaScrapper()

    return render(request, "desktop/blog/category.html", {"paginator": post_paginator, "page": post_page, "p": page, "page_top_post": post_page.object_list[:3], "category": category_model, "fifa": sc})


def view_tag(request, tag=None, page=1):
    post_models = get_object_or_404(Entry, tag__slug=tag, active=True)

    post_paginator = Paginator(post_models, 10)

    try:
        post_page = post_paginator.page(page)
    except EmptyPage:
        raise Http404

    return render(request, "desktop/blog/tag.html", {"paginator": post_paginator, "page": post_page})


def view_single_post(request, year=None, month=None, slug=None):
    post = get_object_or_404(Entry, date__year=year, date__month=month, slug=slug, active=True)
    sc = FifaScrapper()

    return render(request, "desktop/blog/single.html", {"post": post, "fifa": sc})
