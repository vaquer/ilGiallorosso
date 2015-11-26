from django.shortcuts import render
from django.conf import settings
from fifastats.scrapper import FifaScrapper


def index(request):
    sc = FifaScrapper()
    return render(request, 'desktop/index.html', {'fifa': sc})


def single_test(request):
    sc = FifaScrapper()
    return render(request, 'desktop/single_test.html', {'fifa': sc})