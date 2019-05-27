LANGUAGES = ('chinese', 'english', 'japanese')


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
        self._author = ''

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
    def language(self, l):
        if isinstance(l, list):
            for la in l:
                if la.strip() in LANGUAGES:
                    self._language.add(la.strip())
        elif isinstance(l, str):
            if l.strip() in LANGUAGES:
                self._language.add(l.strip())

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
