import requests
from bs4 import BeautifulSoup
from fake_headers import Headers


class Scrapping_habr:

    def __init__(self, url, range_of_pages_for_find):
        self.url = url
        self.pages_for_search = range_of_pages_for_find

    @classmethod
    def get_headers(cls):
        headers = Headers(
                headers=False
        ).generate()
        return headers

    def get_all_articles_from_preview(self, page):
        headers = self.get_headers()
        if page == 0:
            response = requests.get(url=(self.url + '/ru/all/'), headers=headers)
            text = response.text
            soup = BeautifulSoup(text, features='html.parser')
            articles = soup.find_all('article')
        else:
            response = requests.get(url=(self.url + '/ru/all/' + f'page{page+1}/'), headers=headers)
            text = response.text
            soup = BeautifulSoup(text, features='html.parser')
            articles = soup.find_all('article')
        return articles

    def get_text_of_the_article(self, link_of_article):
        headers = self.get_headers()
        response = requests.get(url=link_of_article, headers=headers)
        text = response.text
        soup = BeautifulSoup(text, features='html.parser')
        text_article = soup.find_all(class_="article-formatted-body article-formatted-body "
                                            "article-formatted-body_version-2")[0].text
        return text_article

    def find_articles_with_keywords(self, keywords):
        for page in range(self.pages_for_search):
            articles = self.get_all_articles_from_preview(page)
            for article in articles:
                text_preview = article.find_all(class_="article-formatted-body "
                                                       "article-formatted-body article-formatted-body_version-2")
                link_of_article = self.url + article.find(class_="tm-article-"
                                                                 "snippet").contents[2].next.attrs['href']
                if len(text_preview) != 0:
                    text_for_analysis = self.get_text_of_the_article(link_of_article).replace('.', ' ').\
                        lower().split(' ')
                    for keyword in keywords:
                        if keyword in text_for_analysis:
                            date_of_article = article.find(class_="tm-article-snippet_"
                                                                  "_datetime-published").next.attrs['datetime']
                            header_of_article = article.find(class_="tm-article-snippet").contents[2].text
                            link_of_article = self.url + article.find(class_="tm-article-"
                                                                             "snippet").contents[2].next.attrs['href']
                            print(f'{date_of_article} - {header_of_article} - {link_of_article}')


if __name__ == '__main__':
    KEYWORDS = ['дизайн', 'фото', 'web', 'python']
    url = 'https://habr.com'
    range_of_pages_for_find = int(input('Введите количество страниц выдачи, на которых будем искать статьи: '))
    find_articles = Scrapping_habr(url, range_of_pages_for_find)
    find_articles.find_articles_with_keywords(KEYWORDS)
