import os
from enum import Enum

URL = 'https://comic.moeoverflow.com'

CORS_ALLOWED_ORIGINS = [
    URL,
    "https://nhentai.net",
    "https://e-hentai.org/",
    "https://wnacg.org/"
]

DEBUG = False

TELEGRAM_BOT_TOKEN = ''

SENTRY_DSN = ''

PROXY = {
    # 'http': 'socks5://127.0.0.1:1080',
    # 'https': 'socks5://127.0.0.1:1080'
}

CALIBRE_LIBRARY_PATH = ''

MONGODB_URL = 'mongodb://localhost:27017/'


class DOMAIN(Enum):
    nhentai_net = "nhentai.net"
    ehentai_org = "ehentai.org"
    wnacg_org = "wnacg.org"
    none = "none"


COMIC_ROOT_PATH = '/storage/comic'

# ------------------------------------------------------------

COMIC_MAIN_PATH = os.path.abspath(os.curdir) + COMIC_ROOT_PATH
COMIC_PATHS = {
    DOMAIN.nhentai_net: '%s/%s' % (COMIC_MAIN_PATH, DOMAIN.nhentai_net.value),
    DOMAIN.ehentai_org: '%s/%s' % (COMIC_MAIN_PATH, DOMAIN.ehentai_org.value),
    DOMAIN.wnacg_org: '%s/%s' % (COMIC_MAIN_PATH, DOMAIN.wnacg_org.value)
}
COMIC_DOWNLOADING_PATHS = {
    DOMAIN.nhentai_net: '%s/downloading' % (COMIC_PATHS[DOMAIN.nhentai_net]),
    DOMAIN.ehentai_org: '%s/downloading' % (COMIC_PATHS[DOMAIN.ehentai_org]),
    DOMAIN.wnacg_org: '%s/downloading' % (COMIC_PATHS[DOMAIN.wnacg_org]),
}
DOWNLOAD_URL = {
    DOMAIN.nhentai_net: '/comic/download/nhentai-{params[id]}.epub',
    DOMAIN.ehentai_org: '/comic/download/ehentai-{params[id]}.epub',
    DOMAIN.wnacg_org: '/comic/download/wnacg-{params[id]}.epub'
}