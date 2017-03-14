import config
import os


class Storage:

    def __init__(self, domain, id):
        self.domain = domain
        self.id = id

    def check_comic(self):
        path = self.get_comic_file_path()
        return os.path.exists(path)

    def get_comic_file_name(self):
        return "%s@%s.epub" % (self.domain.value, self.id)

    def get_comic_file_downloading_path(self):
        return "%s/%s" % (config.COMIC_DOWNLOADING_PATHS[self.domain], self.get_comic_file_name())

    def get_comic_file_path(self):
        return "%s/%s" % (config.COMIC_PATHS[self.domain], self.get_comic_file_name())

    def get_comic_public_download_url(self):
        return config.DOWNLOAD_URL[self.domain].format(params={'id': self.id})