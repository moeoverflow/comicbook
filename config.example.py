import os
from enum import Enum

URL = "https://comic.moeoverflow.com"

CORS_ALLOWED_ORIGINS = [
    URL,
    "https://nhentai.net",
    "https://e-hentai.org/",
    "https://wnacg.com/",
]

DEBUG = False

TELEGRAM_BOT_TOKEN = ""

SENTRY_DSN = ""

REQUESTS_MAX_RETRY = 5

PROXY = {
    # 'http': 'socks5://127.0.0.1:1080',
    # 'https': 'socks5://127.0.0.1:1080'
}

CALIBRE_LIBRARY_PATH = ""

MONGODB_URL = "mongodb://localhost:27017/"
REDIS_URL = "redis://localhost:6379/0"


class DOMAIN(Enum):
    nhentai_net = "nhentai.net"
    ehentai_org = "ehentai.org"
    wnacg_com = "wnacg.com"
    none = "none"

    def __str__(self):
        return self.value


COMIC_ROOT_PATH = "/storage/comic"

# ------------------------------------------------------------

COMIC_MAIN_PATH = os.path.abspath(os.curdir) + COMIC_ROOT_PATH
COMIC_PATHS = {
    DOMAIN.nhentai_net: "%s/%s" % (COMIC_MAIN_PATH, DOMAIN.nhentai_net.value),
    DOMAIN.ehentai_org: "%s/%s" % (COMIC_MAIN_PATH, DOMAIN.ehentai_org.value),
    DOMAIN.wnacg_com: "%s/%s" % (COMIC_MAIN_PATH, DOMAIN.wnacg_com.value),
}
COMIC_DOWNLOADING_PATHS = {
    DOMAIN.nhentai_net: "%s/downloading" % (COMIC_PATHS[DOMAIN.nhentai_net]),
    DOMAIN.ehentai_org: "%s/downloading" % (COMIC_PATHS[DOMAIN.ehentai_org]),
    DOMAIN.wnacg_com: "%s/downloading" % (COMIC_PATHS[DOMAIN.wnacg_com]),
}
DOWNLOAD_URL = {
    DOMAIN.nhentai_net: "/comic/download/nhentai-{params[id]}.epub",
    DOMAIN.ehentai_org: "/comic/download/ehentai-{params[id]}.epub",
    DOMAIN.wnacg_com: "/comic/download/wnacg-{params[id]}.epub",
}
COOKIES = {
    DOMAIN.nhentai_net: {
        "csrftoken": "xxx",
        "sessionid": "xxx",
        "cf_clearance": "xxx",
    },
}
USER_AGENT = {
    DOMAIN.nhentai_net: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",  # NOQA
}
