# coding: UTF-8
import requests
import re
from bs4 import BeautifulSoup
from source import Source
import ua

def getImagesLinks(url):
    match = re.search(r'nhentai.net/g/\d+', url)
    if not match:
        print('not match')
        return None
    if 'https' not in url:
        url = 'https://' + url

    source = Source()
    header = { 'User-Agent': ua.getRandomUA() }
    r = requests.get(url, headers=header)
    if r.ok:
        source.cookie = r.cookies
        soup = BeautifulSoup(r.text, "html.parser")

        title = soup.select('#info h1')[0].string
        subTitle = soup.select('#info h2')[0].string
        artist = soup.select('#tags div')[3].select('span a')[0].text.split(' ')[0]

        source.title = title
        source.subTitle = subTitle
        source.artist = artist

        container = soup.select('#thumbnail-container div')
        for (index, con) in enumerate(container):
            link = con.select('a img')[0].get('data-src')
            source.images.append(convertLinks(index, link))
        return source
    else:
        return None
def convertLinks(index, link):
    matchType = re.search(r'jpg|png$', link)
    imageType = matchType.group()
    matchUrl = re.search(r'\.nhentai\.net\/galleries\/\d+', link)
    imageUrl = "i" + matchUrl.group()
    return "https://%s/%d.%s"%(imageUrl, index+1, imageType)
