from .item import item_from_url
from .utils.storage import Storage
from .tasks import crawl_comic, crawl_comic_manually, get_progress, set_progress


class Crawler:
    @classmethod
    def check(cls, url):
        item = item_from_url(url)

        result = {}
        if item:
            result["item"] = item
        else:
            result["data"] = {
                "code": 400,
                "status": "error",
                "message": "url is not support.",
            }
            return result

        storage = Storage(item.domain, item.id)
        result["path"] = storage.get_comic_file_path()
        if storage.check_comic():
            result["data"] = {
                "code": 200,
                "status": "ready",
                "message": "files has generated.",
                "url": storage.get_comic_public_download_url(),
            }
            return result

        progress = get_progress(item.domain, item.id)
        if progress is not None:
            result["item"] = item
            result["data"] = {
                "code": 202,
                "status": "generating",
                "progress": float(progress),
            }
            return result
        else:
            result["data"] = {
                "code": 404,
                "status": "absent",
                "message": "not crawled yet",
            }
            return result

    @classmethod
    def add_download_task(cls, url):
        """
        Add download task to queue.
        """
        result = cls.check(url)
        if result["data"]["code"] != 404:
            return result
        item = result["item"]
        result.clear()
        result["item"] = item
        crawl_comic.delay(url)
        set_progress(item.domain, item.id, 0.00)
        result["data"] = {
            "code": 201,
            "status": "started",
            "message": "crawler task started.",
        }
        return result

    @classmethod
    def download(cls, url):
        """
        Download comic directly.
        """
        result = cls.check(url)
        if result["data"]["code"] != 404:
            return result
        crawl_comic(url)
        return cls.check(url)

    @classmethod
    def download_manually(cls, url, ftype, output):
        """
        Download comic as epub/cbz file to output path.
        """
        return crawl_comic_manually(url, ftype, output)
