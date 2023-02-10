import os

from config import DOMAIN
from db.mongodb import comicbook_calibre
from db.redis import rds

from .celery import app
from .item import item_from_url
from .pipelines.comic_epub import ComicPipeline
from .spiders.ehentai import EhentaiSpider
from .spiders.nhentai import NhentaiSpider
from .spiders.wnacg import WnacgSpider
from .utils.storage import Storage


SPIDERS = {
    DOMAIN.nhentai_net: NhentaiSpider,
    DOMAIN.ehentai_org: EhentaiSpider,
    DOMAIN.wnacg_org: WnacgSpider,
}
COMIC_PROGRESS_KEY = "comic:progress:{}:{}"


def get_progress(domain, id):
    progress = rds.get(COMIC_PROGRESS_KEY.format(domain, id))
    if progress is None:
        return None
    return float(progress)


def set_progress(domain, id, progress):
    # TODO: make crawler timeout configuable
    rds.setex(name=COMIC_PROGRESS_KEY.format(domain, id), time=3600, value=str(progress))


def delete_progress(domain, id):
    rds.delete(COMIC_PROGRESS_KEY.format(domain, id))


@app.task
def crawl_comic(url):
    item = item_from_url(url)
    storage = Storage(item.domain, item.id)
    spider = SPIDERS[item.domain](url)

    set_progress(item.domain, item.id, 0.00)
    item = spider.crawl(item=item)
    if item is None:
        return

    progress = get_progress(item.domain, item.id)
    if progress is not None and progress > 0.00:
        return

    set_progress(item.domain, item.id, 0.01)
    pipeline = ComicPipeline(item)
    dir = storage.get_comic_file_downloading_path()

    def progress_callback(progress):
        set_progress(item.domain, item.id, progress)

    def done_callback(item):
        dl_dir = storage.get_comic_file_downloading_path()
        dir = storage.get_comic_file_path()
        os.rename(dl_dir, dir)
        comicbook_calibre.insert_one(
            {
                "storeInCalibre": False,
                "domain": item.domain.value,
                "id": item.id,
                "filepath": os.path.join(item.domain.value, storage.get_comic_file_name()),
            }
        )
        delete_progress(item.domain, item.id)

    pipeline.generate(dir=dir, progress_callback=progress_callback, done_callback=done_callback)
    return url
