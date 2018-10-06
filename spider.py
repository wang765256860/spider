import os
import requests
from pyquery import PyQuery as pq


class Movie(object):
    def __init__(self):
        self.name = ''
        self.score = 0
        self.quote = ''
        self.cover_url = ''
        self.ranking = 0
        self.director = ''


def cached_url(url):
    folder = 'cached'
    filename = url.split('=', 1)[-1] + '.html'
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            s = f.read()
            return s
    else:
        if not os.path.exists(folder):
            os.makedirs(folder)
        headers = {
            'user-agent': '''Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8''',
        }
        r = requests.get(url, headers)
        with open(path, 'wb') as f:
            f.write(r.content)
        return r.content


def movie_from_div(div):
    e = pq(div)
    m = Movie()
    m.name = e('.title').text()
    m.score = e('.rating_num').text()
    m.quote = e('.inq').text()
    m.cover_url = e('img').attr('src')
    m.ranking = e('.pic').find('em').text()
    m.director = e('.bd').find('p').eq(0).text()
    return m


def movies_from_url(url):
    page = cached_url(url)
    e = pq(page)
    items = e('.item')
    for i in items:
        m = movie_from_div(i)
        with open('douban.txt', 'a') as f:
            f.write("TOP{}\n影片名称：{}\n评分：{}\n摘要：{}\n{}".format(m.ranking, m.name, m.score, m.quote, m.director))
            f.write('\n{}'.format(url))
            f.write("\n============================================\n")


def main():
    for i in range(0, 250, 25):
        url = 'https://movie.douban.com/top250?start={}'.format(i)
        movies_from_url(url)


if __name__ == '__main__':
    main()
