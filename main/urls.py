from django.urls import path

from main.views import error_view, wiki_view

app_name = 'main'

urlpatterns = [
    path('error/', error_view, name='error'),
    path('wiki-search/<str:keyword>/', wiki_view, name='wiki_search'),

]