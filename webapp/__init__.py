from flask import Flask, send_file
from flask_socketio import SocketIO
from jinja2 import Environment, PackageLoader

from config import DOMAIN
from crawler import Crawler
from crawler.utils.storage import Storage

env = Environment(loader=PackageLoader('comicbook', 'webapp/templates'))
app = Flask(__name__)
socketio = SocketIO(app)


COMIC_URLS = {
    DOMAIN.nhentai_net: 'https://nhentai.net/g/{params[id]}/',
    DOMAIN.ehentai_org: 'https://e-hentai.org/g/{params[id]}/{params[token]}/',
    DOMAIN.wnacg_com: 'http://www.wnacg.com/photos-index-aid-{params[id]}.html'
}
DOWNLOAD_URL = {
    DOMAIN.nhentai_net: '/comic/download/nhentai-{params[id]}.epub',
    DOMAIN.ehentai_org: '/comic/download/ehentai-{params[id]}.epub',
    DOMAIN.wnacg_com: '/comic/download/wnacg-{params[id]}.epub'
}


def crawl_done(status, item):
    print("-----crawl done-----")
    print(status)


def check_status(domain, params):
    if domain == None:
        return {
            "code": 404,
            "status": "not found"
        }

    storage = Storage(domain, params['id'])
    if storage.check_comic():
        return {
            "code": 200,
            "status": "ready",
            "url": DOWNLOAD_URL[domain].format(params=params)
        }
    else:
        url = COMIC_URLS[domain].format(params=params)
        progress = Crawler.crawl(url, crawl_done)
        if progress:
            return {
                "code": 202,
                "status": "generating",
                "progress": progress
            }
        return {
            "code": 201,
            "status": "started"
        }


def which_type(type):
    if type == 'nhentai':
        return DOMAIN.nhentai_net
    elif type == 'ehentai':
        return DOMAIN.ehentai_org
    elif type == 'wnacg':
        return DOMAIN.wnacg_com
    else:
        return None


def comic_file(domain, id):
    storage = Storage(domain, id)
    return send_file(storage.get_comic_file_path(), mimetype='application/epub+zip')


@app.route('/')
def index():
    template = env.get_template('index.html')
    return template.render()


@socketio.on('check-status')
def handle_json(json):
    return check_status(which_type(json['type']), json)


@app.route('/comic/download/<type>-<int:id>.epub')
def download_comic(type, id):
    return comic_file(which_type(type), str(id))


@app.errorhandler(404)
def page_not_found(error):
    template = env.get_template('404.html')
    return template.render(), 404


if __name__ == '__main__':
    app.debug = True
    socketio.run(app)

