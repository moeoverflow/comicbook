# coding: UTF-8
import sys
import getopt
import requests

import spider.nhentai
import spider.ehentai
from source import Source
from epub import EPUB
import ua
version = '1.1.0'

def create_comic(source, link, spider, output):
    print('visit to %s...'%(source))
    source = spider.get_comic(link)
    if not source:
        print('get comic resource failed.')
        return False
    print(source.title)
    print('create .epub file to %s'%(output))
    if output == '':
        output = './books'
    if '.epub' in output:
        epub = EPUB(output)
    else:
        if output[-1:] != '/':
            output += '/'
        epub = EPUB('%s%s'%(output, source.title))

    print('start to download image resources:')
    count = len(source.images)
    for (index, image) in enumerate(source.images):
        print('[%d/%d] %s '%(index+1, count, image), end = '')
        sys.stdout.flush()
        header = { 'User-Agent': ua.getRandomUA() }
        r = requests.get(image, cookies=source.cookies, headers=header)
        if r.ok:
            print('[OK]')
            image_name = image.split('/')[-1]
            flag = (index == 0)
            epub.addImage(image_name, r.content, cover=flag)
            epub.addHTML('', '<div><img src="../Images/%s"/></div>'%(image_name))
        else:
            print('[FAIL]')
            return False
    print('download completed.')
    epub.title = source.title
    epub.author = source.artist
    epub.subject = '漫画'
    epub.source = link

    print('epubify...')
    epub.close()
    print('work done.')
    return True


def nhentai_spider(link, output):
    return create_comic('nhentai.net', link, spider.nhentai, output)
def ehentai_spider(link, output):
    return create_comic('e-hentai.org', link, spider.ehentai, output)


CREATE_EPUB = {
    'nhentai.net': nhentai_spider,
    'e-hentai.org': ehentai_spider
}

if __name__ == "__main__":

    help = '''hentaibook options:
      -h, --help       Show help.
      -v, --version    Show version and exit.
      -n, --nhentai    a comic link on nhentai.net
      -e, --ehentai    a comic link on e-hentai.org
      -o, --output     Specify a output path.
    '''

    link = ""
    output = ""
    source = ""

    if len(sys.argv) == 1:
        print(help)
        sys.exit()
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv,"hve:n:o:",["help", "version", "ehentai=", "nhentai=", "output="])
    except getopt.GetoptError:
        print(help)
        sys.exit()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            rint(help)
            sys.exit()
        if opt in ("-e", "--ehentai"):
            link = arg
            source = 'e-hentai.org'
        if opt in ("-n", "--nhentai"):
            link = arg
            source = 'nhentai.net'
        if opt in ("-o", "--output"):
            output = arg
        if opt in ("-v", "--version"):
    	    print(version)
    	    sys.exit()

    CREATE_EPUB[source](link, output)
