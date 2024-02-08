from django.urls import path

from main.views import error_view, wiki_view

app_name = 'main'

urlpatterns = [
    path('error/', error_view, name='error'),
    path('wiki/', wiki_view, name='wiki'),
]