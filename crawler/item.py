import re

import config

LANGUAGES = ("chinese", "english", "japanese", "korean")


class Item:
    def __init__(self):
        self.titles = None
        self.image_urls = None
        self.source = None
        self.domain = None
        self.id = None
        self.dir = None

        self._tags = set()
        self._language = set()
        self._author = ""

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, t):
        if isinstance(t, list):
            for ta in t:
                self._tags.add(ta.strip())
        elif isinstance(t, str):
            self._tags.add(t.strip())

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, lang):
        if isinstance(lang, list) or isinstance(lang, set):
            for la in lang:
                if la.strip() in LANGUAGES:
                    self._language.add(la.strip())
        elif isinstance(lang, str):
            if lang.strip() in LANGUAGES:
                self._language.add(lang.strip())

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, a):
        if not a:
            self._author = ""
        elif isinstance(a, list):
            # only use first author as creator
            self._author = a[0].strip()
        elif isinstance(a, str):
            self._author = a.strip()


def item_from_url(url):
    match = re.search(r"nhentai\.net/g/(\d+)", url)
    item = Item()
    if match:
        item.id = match.group(1)
        item.domain = config.DOMAIN.nhentai_net
    match = re.search(r"wnacg\.org\/photos-index-aid-([0-9]+)\.html$", url)
    if match:
        item.id = match.group(1)
        item.domain = config.DOMAIN.wnacg_org
    match = re.search(r"e-hentai\.org/g/(\d+)/(\w+)", url)
    if match:
        item.id = match.group(1)
        item.token = match.group(2)
        item.domain = config.DOMAIN.ehentai_org

    if item.id:
        return item
    else:
        return None
