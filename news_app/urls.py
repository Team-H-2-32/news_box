from django.urls import path
from .views import home_view, NewsView, DetailPageView, save_view, get_news_view, history_saved_view, \
    delete_view, category_list_view, follow_view, unfollow_view

app_name = 'news_app'

urlpatterns = [
    path('', home_view, name='home'),
    path('news/', NewsView.as_view(), name='news'),
    path('news/news/<str:category>/', get_news_view),
    path('news/detail/<uuid:id>/', DetailPageView.as_view(), name='news_detail'),
    path('news/history-saved/', history_saved_view, name='history_saved'),
    path('news/save/<uuid:id>/', save_view, name='save'),
    path('news/delete/<uuid:id>/<str:arg>/', delete_view, name='delete'),
    path('news/categories/', category_list_view, name='categories'),
    path('follow/<str:category>/', follow_view, name='follow'),
    path('unfollow/<str:category>/', unfollow_view, name='unfollow'),


]
