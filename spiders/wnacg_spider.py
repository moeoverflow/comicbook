# coding: UTF-8
import requests
import re
from bs4 import BeautifulSoup
from item import Item
import ua
from requests.exceptions import ConnectionError
import config

from lxml import etree

class WnacgSpider:

    def __init__(self, url):
        self.url = url

    def crawl(self, item, thread):
        match = re.search(r'www.wnacg.com/photos-index-aid-\d+.html', self.url)
        if not match:
            print('not match')
            return None

        session = requests.Session()
        session.headers.update({'User-Agent': ua.getRandomUA()})
        session.proxies.update(config.PROXY)
        try:
            r = session.get(self.url)
            soup = BeautifulSoup(r.text, "html.parser")

            item.titles = [soup.select('.userwrap h2')[0].string]

            item.image_urls = []
            item.image_urls += get_image_url(item, soup)

            page = int(soup.select('.f_left.paginator a')[-2].string)

            total_images_count = int(page) * len(soup.select('.li.gallary_item'))
            for i in range(2, page + 1):
                index_url = "http://www.wnacg.org/photos-index-page-%d-aid-%s.html" % (i, item.id)
                r = session.get(index_url)
                soup = BeautifulSoup(r.text, "html.parser")
                item.image_urls += get_image_url(item, soup)
                thread.progress = 0.10 * (len(item.image_urls) / total_images_count)
            return item
        except ConnectionError as e:
            print(e)
            return None

def get_image_url(item, soup):
    urls = []
    container = soup.select('.li.gallary_item')
    for (index, con) in enumerate(container):
        url = con.select('.pic_box a img')[0]['src']
        thumb_name = url.split('/')[-1].split('.')[0]
        name = con.select('.info .title .name')[0].string
        url = url.replace('/t/', '/').replace(thumb_name, name)
        urls.append("http://www.wnacg.com"+url)
    return urls