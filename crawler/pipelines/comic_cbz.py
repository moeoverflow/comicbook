# coding: UTF-8
import os
import logging
from zipfile import ZipFile

import requests

from crawler.utils import ua
import config

logger = logging.getLogger("pipeline")
logger.setLevel(logging.INFO)


class ComicPipeline:
    def __init__(self, item):
        self.item = item
        self.cbz = None

    def generate(self, dir):
        self.cbz = ZipFile(dir, "w")
        slog = logger.getChild(f"{self.item.domain}-{self.item.id}")

        slog.info("start to download image resources")
        count = len(self.item.image_urls)

        session = requests.Session()
        session.headers.update({"User-Agent": ua.get_random_ua()})
        session.proxies.update(config.PROXY)

        for (index, url) in enumerate(self.item.image_urls):
            r = session.get(url)
            if r.ok:
                slog.info("[%d/%d] %s [OK]", index + 1, count, url)
                image_name = url.split("/")[-1]
                self.cbz.writestr(image_name, r.content)
            else:
                slog.info("[%d/%d] %s [FAIL]", index + 1, count, url)
                return False
        slog.info("download completed")

        slog.info("cbzify...")
        self.cbz.close()
        slog.info("work done")
