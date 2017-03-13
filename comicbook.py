# coding: UTF-8

import sys
import getopt

from crawler import Crawler
import webapp


def crawl_done(status, item=None):
    print(status)
    if item:
        print(item.titles[0])
        for url in item.image_urls:
            print(url)


def crawl():
    crawler = Crawler()
    crawler.crawl(link, crawl_done)


version = '1.1.0'

if __name__ == "__main__":

    help = '''hentaibook options:
      -h, --help       Show help.
      -v, --version    Show version and exit.
      -c, --comic       a comic link on > nhentai.net
                                        > e-hentai.org
                                        > wnacg.org
      -o, --output     Specify a output path.(temporarily disabled)
    '''

    link = ""
    output = ""

    if len(sys.argv) == 1:
        print(help)
        sys.exit()
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "hvc:o:w", ["help", "version", "comic=", "output=", "webapp"])
    except getopt.GetoptError:
        print(help)
        sys.exit()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(help)
        if opt in ("-c", "--comic"):
            link = arg
            crawl()
        if opt in ("-o", "--output"):
            output = arg
        if opt in ("-v", "--version"):
            print(version)
        if opt in ("-w", "--webapp"):
            webapp.app.debug = True
            webapp.app.run()
