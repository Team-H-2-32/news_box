from newsapi import NewsApiClient
import requests

key ='2aae7faa540f44f9bb78692e0d5e6608'


def top_headlines(api_key, category):
    api = NewsApiClient(api_key=api_key)
    dic = api.get_top_headlines(
        category=category,
        language='ja',
    )
    return dic


def top_headlines_get_url(api_key, category):
    response = requests.get(f'https://newsapi.org/v2/top-headlines?language=jp&category={category}&apiKey={api_key}')
    dic = response.json()

    return dic


