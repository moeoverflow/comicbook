import os
import config

from db.mongodb import comicbook_calibre


class Storage:
    def __init__(self, domain, id):
        self.domain = domain
        self.id = id

    def check_comic(self):
        result = comicbook_calibre.find_one({"domain": self.domain.value, "id": self.id})
        if result is not None:
            return True
        else:
            return False

    def get_comic_file_name(self):
        return "%s@%s.epub" % (self.domain.value, self.id)

    def get_comic_file_downloading_path(self):
        return "%s/%s" % (config.COMIC_DOWNLOADING_PATHS[self.domain], self.get_comic_file_name())

    def get_comic_file_path(self):
        return "%s/%s" % (config.COMIC_PATHS[self.domain], self.get_comic_file_name())

    def get_comic_public_download_url(self):
        return config.DOWNLOAD_URL[self.domain].format(params={"id": self.id})

    @staticmethod
    def get_calibre_epub_file(path):
        return os.path.join(config.CALIBRE_LIBRARY_PATH, path)

    @staticmethod
    def get_comicbook_epub_file(path):
        return os.path.join(config.COMIC_MAIN_PATH, path)
