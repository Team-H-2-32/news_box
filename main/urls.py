from django.urls import path

from main.views import error_view

app_name = 'main'

urlpatterns = [
    path('error/', error_view, name='error')
]