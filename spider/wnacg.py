# coding: UTF-8
import requests
import re
from bs4 import BeautifulSoup
from source import Source
import ua

def get_comic(url):
    match = re.search(r'http://www.wnacg.org/photos-index-aid-\d+\.html', url)
    if not match:
        print('not match')
        return None

    aid = url.split('-')[-1].split('.')[0]
    source = Source()
    header = { 'User-Agent': ua.getRandomUA() }
    try:
        r = requests.get(url, headers=header)
        source.cookies = r.cookies
        soup = BeautifulSoup(r.text, "html.parser")

        source.title = soup.select('#bodywrap h2')[0].string
        page = int(soup.select('.f_left.paginator a')[-2].string)

        get_image_url(source, soup)

        for i in range(2, page+1):
            index_url = "http://www.wnacg.org/photos-index-page-%d-aid-%s.html"%(i, aid)
            r = requests.get(index_url, headers=header, cookies=source.cookies)
            soup = BeautifulSoup(r.text, "html.parser")
            get_image_url(source, soup)
        return source
    except ConnectionError as e:
        print(e)
        return None

def get_image_url(source, soup):
    container = soup.select('.li.gallary_item')
    for (index, con) in enumerate(container):
        link = con.select('.pic_box a img')[0].get('data-original')
        thumb_name = link.split('/')[-1].split('.')[0]
        name = con.select('.info .title .name')[0].string
        source.images.append(convert_links(link, thumb_name, name))

def convert_links(link, thumb_name, name):
    return link.replace('/t/', '/').replace(thumb_name, name)
