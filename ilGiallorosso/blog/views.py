from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage
from .models import Entry, Category

# Create your views here.
def view_category(request, category=None, page=1):
    post_models = get_object_or_404(Entry, category__slug=category, active=True)
    category_model = get_object_or_404(Category, slug=category)

    post_paginator = Paginator(post_models, 10)

    try:
        post_page = post_paginator.page(page)
    except EmptyPage:
        raise Http404

    return render(request, "desktop/blog/category.html", {"paginator": post_paginator, "page": post_page, "p": page, "page_top_post": post_page.object_list[:3], "category": category_model})


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

    return render(request, "desktop/blog/single.html", {"post": post})
