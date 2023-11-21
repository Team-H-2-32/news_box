from django.urls import path
from .views import home_view, NewsView, DetailPageView, save_view, get_news_view, saved_news_view, history_view, \
    delete_view, category_list_view

app_name = 'news_app'

urlpatterns = [
    path('', home_view, name='home'),
    path('news/', NewsView.as_view(), name='news'),
    path('news/news/<str:category>/', get_news_view),
    path('news/detail/<uuid:id>/', DetailPageView.as_view(), name='news_detail'),
    path('news/saved-news/', saved_news_view, name='saved_news'),
    path('news/history/', history_view, name='history'),
    path('news/save/<uuid:id>/', save_view, name='save'),
    path('news/delete/<uuid:id>/<str:arg>/', delete_view, name='delete'),
    path('news/categories/', category_list_view, name='categories'),

]
