# coding: UTF-8
import re

import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError

import config
from crawler.utils import ua


class EhentaiSpider:

    def __init__(self, url):
        self.url = url

    def crawl(self, item, thread):
        match = re.search(r'e-hentai.org\/g\/\d+\/\w+', self.url)
        if not match:
            print('not match')
            return None
        if 'https' not in self.url:
            self.url = 'https://' + self.url
        if self.url[-1] == '/':
            url = self.url[:-1]
        data = match.group().split('/')
        gid = data[-2]
        token = data[-1]

        session = requests.Session()
        session.headers.update({'User-Agent': ua.get_random_ua(),
                                'Referer': 'https://e-hentai.org/',
                                'Host': 'e-hentai.org',
                                'authority': 'e-hentai.org'})
        session.proxies.update(config.PROXY)

        try:
            r = session.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            en_title = soup.select('#gn')[0].string
            jp_title = soup.select('#gj')[0].string
            item.titles = []
            if jp_title != "":
                item.titles.append(jp_title)
            item.titles.append(en_title)

            tags_container = soup.select('#taglist table tbody tr')
            for container in tags_container:
                if container.select('td')[0].string == 'artist:':
                    item.author = container.select('td')[1].select('div a').string
                elif container.select('td')[0].string == 'character:':
                    pass

            nav_container = soup.select('div.gtb table.ptt tr td')
            page_num = len(nav_container) - 2

            item.image_urls = []

            for page_index in range(page_num):
                page_r = session.get(url, params={'p': page_index})
                page_soup = BeautifulSoup(page_r.text, 'html.parser')

                thumb_images_container = page_soup.select('#gdt div[class="gdtm"]')
                total_images_count = len(thumb_images_container)

                for container in thumb_images_container:
                    images_page_url = container.select('div a')[0].get('href')
                    r_images_page = session.get(images_page_url)

                    soup_images_page = BeautifulSoup(r_images_page.text, "html.parser")
                    imgs = soup_images_page.select('.sni a img')

                    for img in imgs:
                        if re.search(r'/h/', img['src']):
                            item.image_urls.append(img['src'])
                            thread.progress = 0.15 * (len(item.image_urls) / total_images_count)
                            print(img['src'])

            return item
        except ConnectionError as e:
            print(e)
            return None