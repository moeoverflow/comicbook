import os
import threading

from config import DOMAIN
from crawler.pipelines.comic_epub import ComicPipeline
from crawler.spiders.ehentai import EhentaiSpider
from crawler.spiders.nhentai import NhentaiSpider
from crawler.spiders.wnacg import WnacgSpider
from crawler.utils.storage import Storage
from db.mongodb import comicbook_calibre

SPIDERS = {
    DOMAIN.nhentai_net: NhentaiSpider,
    DOMAIN.ehentai_org: EhentaiSpider,
    DOMAIN.wnacg_org: WnacgSpider
}


class CrawlerThread(threading.Thread):

    def __init__(self, name, item, url):
        threading.Thread.__init__(self)
        self.progress = 0.00
        self.name = name
        self.item = item
        self.url = url
        self.storage = Storage(item.domain, item.id)

    def run(self):
        spider = SPIDERS[self.item.domain](self.url)
        self.item = spider.crawl(item=self.item, thread=self)
        if self.item is None:
            return

        self.progress = 0.05
        pipeline = ComicPipeline(self.item)
        dir = self.storage.get_comic_file_downloading_path()
        pipeline.generate(dir=dir, thread=self, callback=self.done)

    def done(self, item):
        dl_dir = self.storage.get_comic_file_downloading_path()
        dir = self.storage.get_comic_file_path()
        os.rename(dl_dir, dir)
        comicbook_calibre.insert_one({
            'storeInCalibre': False,
            'domain': item.domain.value,
            'id': item.id,
            'filepath': os.path.join(item.domain.value, self.storage.get_comic_file_name()),
        })