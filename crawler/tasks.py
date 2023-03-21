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
    rds.setex(
        name=COMIC_PROGRESS_KEY.format(domain, id),
        time=3600,
        value=str(progress),
    )


def delete_progress(domain, id):
    rds.delete(COMIC_PROGRESS_KEY.format(domain, id))


@app.task
def crawl_comic(url):
    item = item_from_url(url)
    _domain = item.domain
    _id = item.id
    storage = Storage(_domain, _id)
    spider = SPIDERS[_domain](url)

    set_progress(_domain, _id, 0.00)
    item = spider.crawl(item=item)
    if item is None:
        delete_progress(_domain, _id)
        return f"ERR: crawl failed: {_domain.value} {_id}"
    if not item.titles:
        delete_progress(_domain, _id)
        return f"ERR: no title: {_domain.value} {_id}"

    progress = get_progress(_domain, _id)
    if progress is not None and progress > 0.00:
        return f"ERR: already in progress: {_domain.value} {_id}"

    set_progress(_domain, _id, 0.01)
    pipeline = ComicPipeline(item)
    dir = storage.get_comic_file_downloading_path()

    def progress_callback(progress):
        set_progress(_domain, _id, progress)

    def done_callback():
        dl_dir = storage.get_comic_file_downloading_path()
        dir = storage.get_comic_file_path()
        os.rename(dl_dir, dir)
        filepath = os.path.join(_domain.value, storage.get_comic_file_name())
        comicbook_calibre.insert_one(
            {
                "storeInCalibre": False,
                "domain": _domain.value,
                "id": _id,
                "filepath": filepath,
            }
        )
        delete_progress(_domain, _id)

    pipeline.generate(
        dir=dir,
        progress_callback=progress_callback,
        done_callback=done_callback,
    )
    return f"DONE: {_domain.value} {_id}"
