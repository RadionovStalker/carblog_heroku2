from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from django.contrib.auth.decorators import user_passes_test

BASE_URL = "http://uprom.info/category/news/cars/"


def get_html(url=BASE_URL):
    from urllib.request import Request, urlopen
    req = Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req)
    return webpage.read()


def get_page_count(html):
    soup = BeautifulSoup(html)
    paggination = soup.find('div', class_='page-nav td-pb-padding-side')
    return int(paggination.find_all('a')[-2].text)


def get_article_urls(html):
    soup = BeautifulSoup(html)
    articles_on_page = soup.find_all('div', class_='td-block-span6')
    article_urls = list()
    for article_on_page in articles_on_page:
        article_urls.append(article_on_page.find('div', class_="td-module-thumb").text)
    print(article_urls)
    return article_urls


def parse_page(html):
    soup = BeautifulSoup(html)
    content = soup.find('article', class_="post")
    article = dict()
    article['title'] = content.find('h1', class_="entry-title").text
    content = content.find('div', class_="td-post-content")
    pass


def main():
    total_pages = get_page_count(get_html(BASE_URL))
    print('Всего найдено %d страниц...' % total_pages)
    for numb in range(1, total_pages+1):
        page = get_html(BASE_URL+"/page/{0}/".format(numb))
        article_urls = get_article_urls(page)
        print(article_urls)
        for article_url in article_urls:
            pass



        # projects = []
    #
    # for page in range(1, total_pages + 1):
    #     print('Парсинг %d%% (%d/%d)' % (page / total_pages * 100, page, total_pages))
    #     projects.extend(parse(get_html(BASE_URL + "page=%d" % page)))
    #
    # print('Сохранение...')
    # save(projects, 'projects.csv')


if __name__ == '__main__':
    main()