import threading
import time
import os

from spiders.nhentai_spider import NhentaiSpider
from spiders.ehentai_spider import EhentaiSpider
from spiders.wnacg_spider import WnacgSpider

from pipelines.comic_pipeline import ComicPipeline
from config import DOMAIN
from comic_storage import ComicStorage


SPIDERS = {
    DOMAIN.nhentai_net: NhentaiSpider,
    DOMAIN.ehentai_org: EhentaiSpider,
    DOMAIN.wnacg_com: WnacgSpider
}


class CrawlerThread(threading.Thread):

    def __init__(self, name, item, url):
        threading.Thread.__init__(self)
        self.progress = 0.00
        self.name = name
        self.item = item
        self.url = url
        self.storage = ComicStorage(item.domain, item.id)

    def run(self):
        spider = SPIDERS[self.item.domain](self.url)
        self.item = spider.crawl(item=self.item, thread=self)
        self.progress = 0.05
        pipeline = ComicPipeline(self.item)
        dir = self.storage.get_comic_file_downloading_path()
        pipeline.generate(dir=dir, thread=self, callback=self.done)

    def done(self, item):
        dl_dir = self.storage.get_comic_file_downloading_path()
        dir = self.storage.get_comic_file_path()
        os.rename(dl_dir, dir)
        self.callback(item)