# coding: UTF-8
import os
import logging

import requests
from requests.adapters import HTTPAdapter
from comicepub import ComicEpub

from crawler.utils import ua
from crawler.utils.language_code import get_language_code
import config

logger = logging.getLogger("pipeline")
logger.setLevel(logging.INFO)


class ComicPipeline:
    def __init__(self, item):
        self.item = item
        self.epub = None

    def generate(self, fname, progress_callback, done_callback=None):
        self.epub = ComicEpub(fname)
        slog = logger.getChild(f"{self.item.domain}-{self.item.id}")

        slog.info("start to download image resources")

        count = len(self.item.image_urls)
        progress_callback(1 / (count + 1))

        session = requests.Session()
        session.headers.update({"User-Agent": ua.get_random_ua()})
        session.mount("https://", HTTPAdapter(max_retries=config.REQUESTS_MAX_RETRY))
        session.proxies.update(config.PROXY)

        for index, url in enumerate(self.item.image_urls):
            r = session.get(url)
            if r.ok:
                slog.info("[%d/%d] %s [OK]", index + 1, count, url)
                progress_callback((index + 1 + 1) / (count + 1))
                image_name = url.split("/")[-1]
                is_cover = index == 0

                name, ext = os.path.splitext(image_name)
                self.epub.add_comic_page(r.content, ext, is_cover)
            else:
                slog.info("[%d/%d] %s [FAIL]", index + 1, count, url)
                return False
        slog.info("download completed")
        self.epub.title = (self.item.titles[0], self.item.titles[0])
        self.epub.subjects = list(self.item.tags)
        self.epub.authors = [(self.item.author, self.item.author)]
        self.epub.publisher = ("Comicbook", "Comicbook")

        if len(self.item.language) > 0:
            for language in self.item.language:
                if language == "translated":
                    continue
                self.epub.language = get_language_code(language)
        else:
            if len(self.item.titles) > 0 and (
                "漢化" in self.item.titles[0]
                or "汉化" in self.item.titles[0]
                or "翻譯" in self.item.titles[0]
            ):
                self.epub.language = "zh"

        slog.info("epubify...")
        self.epub.save()
        slog.info("work done")

        if done_callback is not None:
            done_callback()

        return True
