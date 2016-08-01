# coding: UTF-8
import requests
import re
from bs4 import BeautifulSoup
from book import Book
import ua

def getImagesLinks(url):
    book = Book()

    header = { 'User-Agent': ua.getRandomUA() }
    r = requests.get(url, headers=header)
    if r.ok:
        book.cookie = r.cookies
        soup = BeautifulSoup(r.text, "html.parser")

        title = soup.select('#info h1')[0].string
        subTitle = soup.select('#info h2')[0].string
        img = soup.select('#cover a img')[0].get('src')

        matchType = re.search(r'jpg|png$', img)
        imagesType = matchType.group()
        book.imagesType = imagesType
        matchUrl = re.search(r'\.nhentai\.net\/galleries\/\d+', img)
        imagesBaseUrl = "i" + matchUrl.group()

        count = len(soup.select('#thumbnail-container div'))

        book.title = title
        book.subTitle = subTitle
        for i in range(0, count):
            book.images.append("https://" + imagesBaseUrl + "/" + str(i+1) + "." + imagesType)

        return book
    else:
        return None
