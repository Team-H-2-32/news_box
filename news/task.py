from django.core.mail import send_mail
from main.models import Category
from news_app.models import News
from .celery import app
from .news_api import top_headlines, key


@app.task()
def send_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        '019alisobirov@gmail.com',
        recipient_list
    )


categories = ['business', 'sports', 'technology', 'health', 'entertainment', 'science', 'general']


@app.task()
def get_all_news():
    for category_name in categories:
        category = Category.objects.get(category=category_name)
        existing_urls = News.objects.filter(category=category).values_list('url', flat=True)

        category_data = top_headlines(key, category_name)

        for article in category_data['articles']:
            article_url = article['url']
            if article_url not in existing_urls:
                News.objects.create(
                    title=article['title'],
                    description=article['description'],
                    photo=article['urlToImage'],
                    source=article['source']['name'],
                    url=article_url,
                    category=category
                )
                existing_urls = list(existing_urls) + [article_url]


