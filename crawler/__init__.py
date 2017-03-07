import logging
import re
import threading

from config import DOMAIN
from crawler.crawler_thread import CrawlerThread
from crawler.item import Item

logger = logging.getLogger("crawler")
logger.setLevel(logging.INFO)


class Crawler:

    @classmethod
    def crawl(cls, url, callback):
        item = parse_url(url)
        if not item:
            callback("error", None)
            return None

        thread_name = "CrawlerThread." + item.domain.value + "@" + item.id
        thread = get_thread(thread_name)

        if thread:
            return thread.progress
        else:
            thread = CrawlerThread(name=thread_name, item=item, url=url)
            callback("started", None)
            if thread:
                thread.callback = callback
                thread.start()


def parse_url(url):
    match = re.search(r'nhentai\.net/g/(\d+)', url)
    item = Item()
    if match:
        item.id = match.group(1)
        item.domain = DOMAIN.nhentai_net
    match = re.search(r'www\.wnacg\.com/photos-index-aid-(\d+)\.html', url)
    if match:
        item.id = match.group(1)
        item.domain = DOMAIN.wnacg_com
    match = re.search(r'e-hentai\.org/g/(\d+)/(\w+)', url)
    if match:
        item.id = match.group(1)
        item.domain = DOMAIN.ehentai_org

    if item.id:
        return item
    else:
        return None


def get_thread(thread_name):
    for t in threading.enumerate():
        if t.name == thread_name:
            return t
    return None