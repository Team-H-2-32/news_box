from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from main.models import Category
from django.views import View

from news_app.forms import CommentForm
from news_app.models import News, Comment, History, SavedNews


# @login_required
def home_view(request):
    user = request.user
    categories = user.followed_categories.all()

    context = {
        'categories': categories
    }
    return render(request, 'news_app/home.html', context)


class NewsView( LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        categories = user.followed_categories.all()

        context = {
            'categories': categories
        }

        return render(request, 'news_app/news_page.html', context)


def get_news_view(request, category):
    ctgr = Category.objects.get(category_en=category)
    news = News.objects.filter(category=ctgr).order_by('-created_at')[:10]

    dict = {'news':[]}

    for n in news:
        dict['news'].append(
            {
                'url': reverse('news_app:news_detail', args=[n.id]),
                'title': n.title,
                'photo': n.photo,
                'description': n.description,
                'source': n.source,
                'category': n.category.category,
                'created_at': n.created_at
            }
        )

    context = {
        'page_name': category.title(),
        'news': dict['news']
    }

    return JsonResponse(context)


class DetailPageView(LoginRequiredMixin, View):
    def get(self, request, id):
        form = CommentForm()
        user = request.user
        news = News.objects.filter(id=id).first()
        comments = Comment.objects.filter(news=news)
        history_check = History.objects.filter(user=user, news=news).first()
        saved_check = SavedNews.objects.filter(user=user, news=news).first()
        saved = False

        if news:
            if saved_check:
                saved = True
            if not history_check:
                History.objects.create(
                    user=user,
                    news=news
                )

            context = {
                'form': form,
                'news': news,
                'comments': comments,
                'saved': saved
            }

            return render(request, 'news_app/news-detail.html', context)
        else:
            return redirect('main:error')

    def post(self, request, id):
        form = CommentForm(data=request.POST)
        news = News.objects.get(id=id)
        user = request.user

        if form.is_valid():
            comment = form.cleaned_data.get('comment')
            Comment.objects.create(
                user=user,
                news=news,
                comment=comment
            )
            return redirect('news_app:news_detail', id=news.id)
        else:
            return redirect('main:error')


def save_view(request, id):
    user = request.user
    news = News.objects.filter(id=id).first()
    obj = SavedNews.objects.filter(user=user, news=news).first()

    if news:
            if not obj:
                SavedNews.objects.create(
                    user=user,
                    news=news
                )
            else:
                obj.delete()
            return redirect('news_app:news_detail', id=news.id)
    else:
        return print('error')


def history_view(request):
    user = request.user
    history = History.objects.filter(user=user).order_by('-created_at')[0:20]

    news = [n.news for n in history]
    context = {
        'news': news
    }

    return render(request, 'news_app/saved-history-news-list.html', context)


def saved_news_view(request):
    user = request.user
    saved_news = SavedNews.objects.filter(user=user).order_by('-created_at')[0:20]

    news = [n.news for n in saved_news]
    context = {
        'news': news
    }

    return render(request, 'news_app/saved-history-news-list.html', context)


def delete_view(request, id, arg):
    news = News.objects.get(id=id)
    if arg == 'saved':
        obj = SavedNews.objects.get(news=news)
        obj.delete()
        return redirect('news_app:news_detail', id=news.id)
    else:
        obj = History.objects.delete(news=news)
        obj.delete()
        return redirect('news_app:history')


def category_list_view(request):
    categories = Category.objects.all()

    context = {
        'categories': categories
    }

    return render(request, 'news_app/categories.html', context)


