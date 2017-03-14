# coding: UTF-8
import logging
import re

import requests
from lxml import etree
from requests.exceptions import ConnectionError

import config
from crawler.utils import ua

logger = logging.getLogger("spider")
logger.setLevel(logging.INFO)


class NhentaiSpider:
    def __init__(self, url):
        self.url = url

    def crawl(self, item, thread):
        match = re.search(r'nhentai.net/g/\d+', self.url)
        if not match:
            logger.info(" url not match")
            return None
        if 'https' not in self.url:
            self.url = 'https://' + self.url

        session = requests.Session()
        session.headers.update({'User-Agent': ua.get_random_ua()})
        session.proxies.update(config.PROXY)

        try:
            logger.info("fetching " + self.url)
            r = session.get(self.url)
            item.cookies = r.cookies

            selector = etree.HTML(r.text)

            en_title = selector.xpath('//*[@id="info"]/h1/text()')
            sub_title = selector.xpath('//*[@id="info"]/h2/text()')
            item.titles = sub_title + en_title
            item.author = selector.xpath('//*[@id="tags"]/div[4]/span[1]/a/text()')

            item.tags = selector.xpath('//*[@id="tags"]/div[3]/span/a/text()')
            item.language = selector.xpath('//*[@id="tags"]/div[6]/span/a/text()')
            item.image_urls = selector.xpath('//*[@id="thumbnail-container"]/div/a/img/@data-src')
            item.image_urls = list(map(convert_url, item.image_urls))
            item.source = self.url
            thread.progress = 0.05
            return item
        except ConnectionError as e:
            print(e)
            return None


def convert_url(url):
    match_type = re.search(r'jpg|png$', url)
    type = match_type.group()
    match_url = re.search(r'\.nhentai\.net/galleries/(\d+)/(\d+)', url)
    id = match_url.group(1)
    index = match_url.group(2)
    return "https://i.nhentai.net/galleries/%s/%s.%s" % (id, index, type)
