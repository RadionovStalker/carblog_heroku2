import sys
import os
sys.path.append('..')
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from django.contrib.auth.decorators import user_passes_test
import json
from .models import Article, Gallery, TreeCategory
from django.contrib.auth.models import User

BASE_URL = "http://uprom.info/category/news/cars/"


def get_html(url=BASE_URL):
    from urllib.request import Request, urlopen
    req = Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req)
    return webpage.read()


def get_page_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    paggination = soup.find('div', class_='page-nav td-pb-padding-side')
    return int(paggination.find_all('a')[-2].text)


def get_article_urls(html):
    soup = BeautifulSoup(html, 'html.parser')
    articles_on_page = soup.find_all('div', class_='td-block-span6')
    # print(articles_on_page)
    article_urls = list()
    for article_on_page in articles_on_page:
        article_urls.append(article_on_page.find('div', class_="td-module-thumb").find('a').attrs['href'])
    print(article_urls)
    return article_urls


def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find('article', class_="post")
    article = dict()
    article['title'] = content.find('h1', class_="entry-title").text
    # print("title")
    # print(article['title'])
    content = content.find('div', class_="td-post-content")
    article['main_img'] = content.find('div', class_="td-post-featured-image").find('a').attrs['href']
    # print("main image")
    # print(article['main_img'])
    p_texts = content.find_all('p')
    # print("p-s")
    # print(p_texts)
    article_text = list()
    for text in p_texts:
        article_text.append(text.text)
    article['text'] = article_text
    gallery = content.find('div', class_="td-gallery")
    # print("GALLERY")
    # print(gallery)
    if gallery:
        images = list()
        gallery = gallery.find_all('div', class_="td-slide-item")
        for image in gallery:
            images.append(image.find('a', class_="slide-gallery-image-link").attrs['href'])
        article['gallery'] = images
    else:
        gallery = content.find_all('figure')
        if gallery:
            images = list()
            for gal in gallery:
                images.append(gal.find('img').attrs['src'])
            article['gallery'] = images
        else:
            article['gallery'] = ''

    return article


def save_to_json_file(articles):
    with open('parse_articles.json', 'w', encoding='utf-8') as file:
        json.dump(articles, file, indent=2, ensure_ascii=False)


def load_to_db_of_carblog():
    with open('parse_articles.json', 'r', encoding='utf-8') as file:
        data_for_articles = json.load(file)
        for data in data_for_articles:
            new_article = Article()
            new_article.set_current_language('uk')
            new_article.title = data['title']
            text = ''
            for row in data['text']:
                text += row
            new_article.description = text[:457]+"..."
            new_article.body = text
            author = User.objects.get(username='admin')
            category = TreeCategory.objects.get(name="Машиностроение")
            new_article.author = author
            new_article.image = data['main_img']
            new_article.save()
            new_article.tree_category.add(category)
            new_article.save()
            for img in data['gallery']:
                new_gallery = Gallery()
                new_gallery.image = img
                new_gallery.article = new_article
                new_gallery.save()


def main():
    # total_pages = get_page_count(get_html(BASE_URL))
    # total_pages = 2
    # print('Всего найдено %d страниц...' % total_pages)
    # parsed_articles = list()
    # for numb in range(1, total_pages+1):
    #     page = get_html(BASE_URL+"/page/{0}/".format(numb))
    #     article_urls = get_article_urls(page)
    #     print("parse "+str(numb)+" page of "+str(total_pages)+" pages")
    #     # print(article_urls)
    #     for article_url in article_urls:
    #         print("parse: "+article_url)
    #         article_page = get_html(article_url)
    #         parsed_art = parse_page(article_page)
    #         print(parsed_art)
    #         parsed_articles.append(parsed_art)
    # print("Finish of parsing!")
    # save_to_json_file(parsed_articles)
    # print("Saved to file")
    load_to_db_of_carblog()

# if __name__ == '__main__':
#     main()