# coding: UTF-8
import requests
import re
from bs4 import BeautifulSoup
from source import Source
import ua

def get_comic(url):
    match = re.search(r'g.e-hentai.org\/g\/[0-9]+\/[0-9[a-z]+', url)
    if not match:
        print('not match')
        return None
    if 'http' not in url:
        url = 'http://' + url
    if url[-1] == '/':
        url = url[:-1]
    data = match.group().split('/')
    gid = data[-2]
    token = data[-1]

    source = Source()
    header = { 'User-Agent': ua.getRandomUA() }

    try:
        r = requests.get(url, headers=header)
        source.cookies = r.cookies
        soup = BeautifulSoup(r.text, "html.parser")

        source.title = soup.select('#gn')[0].string
        source.sub_title = soup.select('#gj')[0].string

        tags_container = soup.select('#taglist table tbody tr')
        for container in tags_container:
            if container.select('td')[0].string == 'artist:':
                source.artist = container.select('td')[1].select('div a').string
            elif container.select('td')[0].string == 'character:':
                pass

        thumb_images_container = soup.select('#gdt div[class="gdtm"]')

        for container in thumb_images_container:
            images_page_url = container.select('div a')[0].get('href')
            r_images_page = requests.get(images_page_url, headers=header, cookies=source.cookies)

            soup_images_page = BeautifulSoup(r_images_page.text, "html.parser")
            source.images.append(soup_images_page.select('#i3 a img')[0].get('src'))

        return source
    except ConnectionError as e:
        print(e)
        return None
