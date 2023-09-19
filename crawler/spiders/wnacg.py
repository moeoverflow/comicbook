# coding: UTF-8
import re
import logging

import requests
from requests.exceptions import ConnectionError
from lxml import etree


import config
from crawler.utils import ua

logger = logging.getLogger("spider_wnacg")
logger.setLevel(logging.INFO)


class WnacgSpider:
    def __init__(self, url):
        self.url = url

    def crawl(self, item):
        match = re.search(r"wnacg\.com", self.url)
        if not match:
            logger.warn("url not match")
            return None
        if "http" not in self.url:
            self.url = "https://" + self.url

        session = requests.Session()
        session.headers.update({"User-Agent": ua.get_random_ua()})
        session.proxies.update(config.PROXY)
        try:
            r = session.get(self.url)
            selector = etree.HTML(r.text)

            title = selector.xpath('//*[@id="bodywrap"]/h2/text()')[0]

            pages = []
            img_urls = []
            page = selector.xpath('//*[@id="bodywrap"]/div[2]/div/ul/li[1]/div[1]/a')[
                0
            ].get("href")
            pages.append(get_full_url(page))
            while len(pages) == 1 or (
                len(pages) > 1 and pages[0] != pages[len(pages) - 1]
            ):
                current_page = pages[len(pages) - 1]
                p = session.get(current_page)
                sel = etree.HTML(p.text)
                img_url = sel.xpath('//*[@id="picarea"]')[0].get("src")
                img_urls.append(img_url)

                next_page = sel.xpath("/html/body/div[8]/div/div/a[2]")[0].get("href")
                pages.append(get_full_url(next_page))

            item.titles = [title]
            item.author = "Unknown Author"
            item.tags = []
            item.image_urls = list(map(lambda url: "https:" + url, img_urls))
            return item
        except ConnectionError as e:
            logger.error(e)
            return None


def get_full_url(uri):
    return "https://www.wnacg.com" + uri
