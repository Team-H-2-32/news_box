from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import get_language

from main.models import Category
from django.views import View
from news.microsoft_translator_api import translate
from news_app.forms import CommentForm
from news_app.models import News, Comment, History, SavedNews


# @login_required
def home_view(request):
    user = request.user
    categories = ''
    if user.username:
        categories = user.followed_categories.all()
    else:
        categories = Category.objects.all()

    context = {
        'categories': categories
    }
    return render(request, 'news_app/home.html', context)


class NewsView(View):
    def get(self, request):
        user = request.user
        categories = ''
        if user.username:
            categories = user.followed_categories.all()
        else:
            categories = Category.objects.all()

        context = {
            'categories': categories,
            'selected_category': request.GET.get('category', None)
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


class DetailPageView(View):
    def get(self, request, id):
        form = CommentForm()
        user = request.user
        news = News.objects.filter(id=id).first()
        comments = Comment.objects.filter(news=news)
        context = {}
        if user.is_authenticated:
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
                    'saved': saved,
                    'arg': 'saved-detail'
                }

                return render(request, 'news_app/news-detail.html', context)
            else:
                return redirect('main:error')
        else:
            context = {
                'form': form,
                'news': news,
                'comments': comments,
                'arg': 'saved-detail'
            }

            return render(request, 'news_app/news-detail.html', context)


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

    if user.username:
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
    else:
        return redirect('user:login')


def history_saved_view(request):
    user = request.user
    history_obj = History.objects.filter(user=user).order_by('-created_at')[0:20]
    saved_news_obj = SavedNews.objects.filter(user=user).order_by('-created_at')[0:20]

    history = [n.news for n in history_obj]
    saved_news = [n.news for n in saved_news_obj]
    context = {
        'history': history,
        'saved_news': saved_news,
    }

    return render(request, 'news_app/saved-history-news-list.html', context)


def delete_view(request, id, arg):
    news = News.objects.get(id=id)
    if arg == 'saved-detail':
        obj = SavedNews.objects.get(news=news)
        obj.delete()
        return redirect('news_app:news_detail', id=id)
    elif arg == 'saved':
        obj = SavedNews.objects.get(news=news)
        obj.delete()
        return redirect('news_app:history_saved')
    elif arg == 'history':
        obj = History.objects.filter(news=news).first()
        obj.delete()
        return redirect('news_app:history_saved')


def category_list_view(request):
    categories = Category.objects.all()

    context = {
        'categories': categories
    }

    return render(request, 'news_app/categories.html', context)


def follow_view(request, category):
    user = request.user
    ctgry = Category.objects.get(category_en=category)
    if user.is_authenticated:
        user.followed_categories.add(ctgry)
        messages.success(request, f"{ctgry.category} added to followed list")
        return redirect('news_app:categories')
    else:
        return redirect('user:login')


def unfollow_view(request, category):
    user = request.user
    ctgry = Category.objects.get(category_en=category)
    user.followed_categories.remove(ctgry)
    messages.info(request, f"{ctgry.category} removed from followed list")
    return redirect('news_app:categories')


def comment_translation_view(request, comment_id):
    current_language = get_language()
    comment = Comment.objects.get(id=comment_id)
    translated_comment = translate(current_language, comment.comment)

    context = {
        'translated_comment': translated_comment
    }

    return JsonResponse(context)


def comment_delete_view(request, comment_id):
    user = request.user
    comment = Comment.objects.get(id=comment_id)
    if user == comment.user:
        comment.delete()
        return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return redirect('main:error')


