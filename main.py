import requests
from bs4 import BeautifulSoup
from fake_headers import Headers


class Scrapping_habr:

    def __init__(self, url):
        self.url = url

    @classmethod
    def get_headers(cls):
        header = Headers(
                browser="chrome",
                os="win",
                headers=True
        ).generate()
        return header

    def get_all_articles_from_preview(self):
        headers = self.get_headers()
        response = requests.get(url=(self.url + '/ru/all/'), headers=headers)
        text = response.text
        soup = BeautifulSoup(text, features='html.parser')
        articles = soup.find_all('article')
        return articles

    def get_text_of_the_article(self, link_of_article):
        headers = self.get_headers()
        response = requests.get(url=link_of_article, headers=headers)
        text = response.text
        soup = BeautifulSoup(text, features='html.parser')
        text_article = soup.find_all(class_="article-formatted-body article-formatted-body article-formatted-body_version-2")[0].text
        return text_article

    def find_articles_with_keywords(self, keywords):
        articles = self.get_all_articles_from_preview()
        for article in articles:
            link_of_article = self.url + article.find(class_="tm-article-"
                                                             "snippet").contents[2].next.attrs['href']
            print(link_of_article)
            if len(link_of_article) != 0:
                text_for_analys = self.get_text_of_the_article(link_of_article).replace('.', ' ').lower().split(' ')
                for keyword in keywords:
                    if keyword in text_for_analys:
                        date_of_article = article.find(class_="tm-article-snippet_"
                                                              "_datetime-published").next.attrs['datetime']
                        header_of_article = article.find(class_="tm-article-snippet").contents[2].text
                        link_of_article = self.url + article.find(class_="tm-article-"
                                                                         "snippet").contents[2].next.attrs['href']
                        print(f'{date_of_article} - {header_of_article} - {link_of_article}')
                    else:
                        self.get_text_of_the_article(link_of_article)



if __name__ == '__main__':
    KEYWORDS = ['дизайн', 'фото', 'web', 'python']
    url = 'https://habr.com'
    find_articles = Scrapping_habr(url)
    find_articles.find_articles_with_keywords(KEYWORDS)
