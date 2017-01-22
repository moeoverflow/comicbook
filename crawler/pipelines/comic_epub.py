import sys
import requests

from crawler.utils.epub import EPUB
from crawler.utils import ua
import config


class ComicPipeline():
    def __init__(self, item):
        self.item = item

    def generate(self, dir, thread, callback=None):
        self.epub = EPUB(dir)

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
                thread.progress = (index+1+1) / (count+1)
                print('[OK]')
                image_name = url.split('/')[-1]
                flag = (index == 0)
                self.epub.addImage(image_name, r.content, cover=flag)
                self.epub.addHTML('', '<div><img src="../Images/%s"/></div>' % (image_name))
            else:
                print('[FAIL]')
                return False
        print('download completed.')
        self.epub.title = self.item.titles[0]
        self.epub.author = self.item.author
        self.epub.subject = '漫画'
        self.epub.source = self.item.source

        print('epubify...')
        self.epub.close()
        print('work done.')

        if callback:
            callback(self.item)
