import main

import requests
from bs4 import BeautifulSoup
from datetime import datetime, date

HEADERS = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}

baseUrl = 'https://habr.com'
KEYWORDS = ['Microsoft SQL Server *', 'Удалённая работа', 'CSS *', 'web', 'python', 'DIY или Сделай сам',
            'психолог', 'любят', 'Программирование *']

@main.decorator_logger_path('log.txt')
def web_scraping():
    ret = requests.get(baseUrl + '/ru/all/', headers=HEADERS)
    ret.raise_for_status()
    soup = BeautifulSoup(ret.text, 'html.parser')

    articles = soup.find_all("article")
    for article in articles:
        hubs = article.find_all(class_='tm-article-snippet__hubs-item')
        hubs = set(hub.text.strip() for hub in hubs)
        article_preview = article.find(class_='tm-article-body tm-article-snippet__lead').text

        for keyw in KEYWORDS:
            if keyw in hubs or keyw in article_preview:
                datetimestr = article.find(class_='tm-article-snippet__datetime-published').find("time").attrs[
                    "datetime"]
                date = datetime.strptime(datetimestr, '%Y-%m-%dT%H:%M:%S.%fZ').date()
                header = article.find(class_='tm-article-snippet__title tm-article-snippet__title_h2').text
                href = article.find(class_='tm-article-snippet__title tm-article-snippet__title_h2').find("a").attrs[
                    'href']
                print(f"{date} — {header} — {baseUrl + href}")
                break

    return 'Ok'

if __name__ == '__main__':
    web_scraping()
