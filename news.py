import requests


"""News Module
Handles the API requests and information received for the News Page using
NewsAPI.org and short listing the information received to 10 articles.
"""


__version__ = '1.0'
__author__ = 'Joshua Mugglestone'


def get_news():
    """Requests the information from NewsAPI.org and converts it to jason"""
    url = ('https://newsapi.org/v2/top-headlines?'
           'sortBy=popularity&'
           'sources=bbc-news&'
           'apiKey=')
    response = requests.get(url)
    return response.json()


def short_list_news():
    """Reads The information from the request and adds 10 articles to a list"""
    long_list = get_news()
    short_list = []
    while len(short_list) < 10:
        short_list.append(long_list['articles'][len(short_list)])
    return short_list
