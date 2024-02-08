from django.shortcuts import render
from django.views import View


def error_view(request):
    return render(request, 'main/error.html')


def wiki_view(request):
    return render(request, 'main/wiki.html')