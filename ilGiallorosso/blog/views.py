import json
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator, EmptyPage
from django.core.cache import cache
from django.contrib.sitemaps import Sitemap
from django.utils import timezone
from django.conf import settings
from .models import Entry, Category, Tag
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

    return render(request, "desktop/blog/category.html", {"settings": settings, "paginator": post_paginator, "page": post_page, "p": page, "page_top_post": post_page.object_list[:3], "category": category_model, "fifa": sc})


def view_tag(request, slug=None, page=1):
    tag = get_object_or_404(Tag, slug=slug)

    post_models = cache.get('entries_tag_v3_{0}'.format(slug))
    if not post_models:
        post_models = Entry.objects.select_related('author', 'category').filter(tags__slug__in=[slug], active=True).order_by('-order')
        cache.set('entries_tag_v3_{0}'.format(slug), post_models, 60 * 15)

    post_paginator = Paginator(post_models, 20)

    try:
        post_page = post_paginator.page(page)
    except EmptyPage:
        raise Http404

    sc = FifaScrapper()

    return render(request, "desktop/blog/tag.html", {"settings": settings, "paginator": post_paginator, "page": post_page, "page_top_post": post_page.object_list[:3], 'tag': tag, "fifa": sc})


def view_single_post(request, year=None, month=None, slug=None):
    post = cache.get('entry_{0}_v4'.format(slug))
    if not post:
        try:
            post = Entry.objects.select_related('author', 'category').get(date__year=year, date__month=month, slug=slug)
        except:
            raise Http404
        cache.set('entry_{0}_v4'.format(slug), post, 60 * 5)

    sc = FifaScrapper()

    return render(request, "desktop/blog/single.html", {"settings": settings, "post": post, "fifa": sc})


def view_redgol_feed(request):
    # if request.method != "POST":
    #     raise Http404

    total_post = cache.get('home_posts_v5')

    if not total_post:
        total_post = Entry.objects.select_related('author', 'category').filter(active=True).order_by('-order')
        cache.set('home_posts_v5', total_post, 60 * 10)

    post_response = total_post[:5]
    post_response_json = [post.dehydrate() for post in post_response]
    post_response_json = json.dumps(post_response_json)

    if "callback" in request.GET:
        data = "{0}({1});".format(request.GET.get('callback', 'reponseCallback'), post_response_json)
        return HttpResponse(data, content_type="text/javascript")
    else:
        return HttpResponse(post_response_json, content_type="application/json")


class EntrySitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0
    lastmod = timezone.now()

    def items(self):
        site_map_entries = cache.get('site_map_entries')

        if not site_map_entries:
            site_map_entries = Entry.objects.filter(active=True).order_by('-date')
            cache.set('site_map_entries', site_map_entries, 60 * 15)

        return site_map_entries


class TagSiteMap(Sitemap):
    changefreq = "daily"
    priority = 1.0
    lastmod = timezone.now()

    def items(self):
        site_tags = cache.get('site_tags')

        if not site_tags:
            site_tags = Tag.objects.all().order_by('tag')
            cache.set('site_tags', site_tags, 60 * 60)

        return site_tags


class CategorySiteMap(Sitemap):
    changefreq = "daily"
    priority = 1.0
    lastmod = timezone.now()

    def items(self):
        site_categories = cache.get('site_categories')

        if not site_categories:
            site_categories = Category.objects.all().order_by('name')
            cache.set('site_categories', site_categories, 60 * 60)

        return site_categories

