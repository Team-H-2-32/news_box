from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .wikipedia import search_wikipedia
from django.utils.translation import get_language



def error_view(request):
    return render(request, 'main/error.html')


def wiki_view(request, keyword):
    language = get_language()

    try:
        result = search_wikipedia(language, keyword)
    except Exception as e:
        result = False

    context = {
        'result': result
    }

    return JsonResponse(context)
