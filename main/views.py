from django.shortcuts import render

# Create your views here.

def error_view(request):
    return render(request, 'main/error.html')
