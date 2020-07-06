# coding: UTF-8
import os
import sys
import requests
from comicepub import ComicEpub

from crawler.utils import ua
from crawler.utils.language_code import get_language_code

import config


class ComicPipeline():
    def __init__(self, item):
        self.item = item
        self.epub = None

    def generate(self, dir, thread, callback=None):
        self.epub = ComicEpub(dir)

        print('start to download image resources:')
        count = len(self.item.image_urls)
        thread.progress = 1 / (count + 1)

        session = requests.Session()
        session.headers.update({'User-Agent': ua.get_random_ua()})
        session.proxies.update(config.PROXY)

        for (index, url) in enumerate(self.item.image_urls):
            print('[%d/%d] %s ' % (index + 1, count, url), end='')
            sys.stdout.flush()

            r = session.get(url)
            if r.ok:
                thread.progress = (index + 1 + 1) / (count + 1)
                print('[OK]')
                image_name = url.split('/')[-1]
                is_cover = (index == 0)

                name, ext = os.path.splitext(image_name)
                self.epub.add_comic_page(r.content, ext, is_cover)
            else:
                print('[FAIL]')
                return False
        print('download completed.')
        self.epub.title = (self.item.titles[0], self.item.titles[0])
        self.epub.subjects = list(self.item.tags)
        self.epub.authors = [(self.item.author, self.item.author)]
        self.epub.publisher = ('Comicbook', 'Comicbook')

        if len(self.item.language) > 0:
            for language in self.item.language:
                if language == 'translated':
                    continue
                self.epub.language = get_language_code(language)
        else:
            if len(self.item.titles) > 0 and (
                    '漢化' in self.item.titles[0] or
                    '汉化' in self.item.titles[0] or
                    '翻譯' in self.item.titles[0]
            ):
                self.epub.language = 'zh'

        print('epubify...')
        self.epub.save()
        print('work done.')

        if callback:
            callback(self.item)
