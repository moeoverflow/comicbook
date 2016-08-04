# coding: UTF-8
import requests
import re
from bs4 import BeautifulSoup
from source import Source
import ua

def get_images_links(url):
    match = re.search(r'nhentai.net\/g\/\d+', url)
    if not match:
        print('not match')
        return None
    if 'https' not in url:
        url = 'https://' + url

    source = Source()
    header = { 'User-Agent': ua.getRandomUA() }
    try:
        r = requests.get(url, headers=header)
        source.cookie = r.cookies
        soup = BeautifulSoup(r.text, "html.parser")

        title = soup.select('#info h1')[0].string
        sub_title = soup.select('#info h2')[0].string
        artist = soup.select('#tags div')[3].select('span a')[0].text.split(' ')[0]

        source.title = title
        source.sub_title = sub_title
        source.artist = artist

        container = soup.select('#thumbnail-container div')
        for (index, con) in enumerate(container):
            link = con.select('a img')[0].get('data-src')
            source.images.append(convert_links(index, link))
        return source
    except ConnectionError as e:
        print(e)
        return None
def convert_links(index, link):
    match_type = re.search(r'jpg|png$', link)
    image_type = match_type.group()
    match_url = re.search(r'\.nhentai\.net\/galleries\/\d+', link)
    image_url = "i" + match_url.group()
    return "https://%s/%d.%s"%(image_url, index+1, image_type)
