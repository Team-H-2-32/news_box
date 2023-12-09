from django.core.mail import send_mail
from main.models import Category
from news_app.models import News
# from .celery import app
from .news_api import top_headlines, key
from .microsoft_translator_api import translate


def send_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        '019alisobirov@gmail.com',
        recipient_list
    )


categories = ['business', 'sports', 'technology', 'health', 'entertainment', 'science', 'general']


def get_all_news():
    for category_name in categories:
        category = Category.objects.get(category_en=category_name.title())
        existing_urls = News.objects.filter(category=category).values_list('url', flat=True)

        category_data = top_headlines(key, category_name)

        for article in category_data['articles']:
            article_url = article['url']
            if article_url not in existing_urls:
                title = article['title']
                description = article['description']
                News.objects.create(
                    title=article['title'],
                    title_en=translate(to='en', text=title),
                    title_ru=translate(to='ru', text=title),
                    description=article['description'],
                    description_en=translate(to='en', text=description),
                    description_ru=translate(to='ru', text=description),
                    photo=article['urlToImage'],
                    source=article['source']['name'],
                    url=article_url,
                    category=category
                )

                existing_urls = list(existing_urls) + [article_url]


