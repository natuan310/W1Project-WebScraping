from flask import Flask, render_template, request, redirect, url_for
import requests
import re
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_url(url):
    """ Get html from url
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def crawl_vnexpress(url):
    soup = get_url(url)
    articles = soup.find_all('article', class_='list_news')
    data = []
    for article in articles:
        d = {'title': '', 'img_url': '', 'links': '', 'description': ''}
        try:

            if article.img:
                d['title'] = article.a.string
                d['img_url'] = article.img['data-original']
                d['links'] = article.a['href']
                d['description'] = article.p.text
        except:
            pass
        if d['title'] != '':
            data.append(d)
        else:
            pass
    return data[:10]


def crawl_phimmoi(url):
    soup = get_url(url)
    # item selector div.List__Wrapper-sc-6lyqk4-0.layRnl
    movies = soup.find_all('a', class_='movie-item')
    data = []
    for movie in movies:
        mv = {'vn_title': '', 'eng_title': '',
              'img_url': '', 'duration': '', 'links': ''}

        img_url = re.findall(
            r'http.*jpg', movie.find_all("div", class_="public-film-item-thumb")[0]["style"])
        mv['img_url'] = img_url[0]
        mv['title'] = movie.find_all("div", class_="movie-title-1")[0].string
        mv['eng_title'] = movie.find_all(
            "span", class_="movie-title-2")[0].string
        mv['duration'] = movie.find_all(
            "span", class_="movie-title-chap")[0].string
        mv['links'] = "http://www.phimmoi.net/" + movie["href"]

        data.append(mv)
    return data[:10]


base_url = 'https://vnexpress.net'
url = 'http://www.phimmoi.net/'

@app.route('/')
def index():
    movies = crawl_phimmoi(url)
    print(movies)
    return render_template('crawl_phimmoi.html', movies=movies)


@app.route('/phimmoi', methods=['POST', 'GET'])
def phimmoi():
    url = 'http://www.phimmoi.net/'
    movies = crawl_phimmoi(url)
    print(movies[:2])
    return render_template('crawl_phimmoi.html', movies=movies)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
