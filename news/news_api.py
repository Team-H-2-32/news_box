from newsapi import NewsApiClient

key ='2aae7faa540f44f9bb78692e0d5e6608'


def top_headlines(api_key, category):
    api = NewsApiClient(api_key=api_key)
    dic = api.get_top_headlines(
        category=category,
        language='ja',
    )
    return dic

