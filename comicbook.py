# coding: UTF-8

import sys
import json
import getopt

from crawler import Crawler

import config
from bot import ComicbookTelegramBot


version = "1.1.0"

if __name__ == "__main__":

    help = """comicbook options:
      -h, --help            Show help.
      -v, --version         Show version and exit.
      -c, --comic           a comic link on > nhentai.net
                                            > e-hentai.org
                                            > wnacg.org
      -o, --output          Specify a output path.(temporarily disabled)
      -t, --telegram-bot    Run telegram bot.
    """

    link = ""
    output = ""

    if len(sys.argv) == 1:
        print(help)
        sys.exit()
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(
            argv, "hvc:o:ts", ["help", "version", "comic=", "output=", "telegram-bot", "server"]
        )
    except getopt.GetoptError:
        print(help)
        sys.exit()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(help)
        if opt in ("-c", "--comic"):
            link = arg
            result = Crawler.download(link)
            result.pop("item")
            print(json.dumps(result, indent=2))
        if opt in ("-o", "--output"):
            output = arg
        if opt in ("-v", "--version"):
            print(version)

    if ("-t", "") in opts or ("--telegram-bot", "") in opts:
        bot = ComicbookTelegramBot(config.TELEGRAM_BOT_TOKEN)
        bot.start()
