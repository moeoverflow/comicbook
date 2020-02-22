import glob
import logging

from flask import Flask, send_file
from flask_socketio import SocketIO
from jinja2 import Environment, PackageLoader

import config
from crawler import Crawler
from crawler.utils.storage import Storage
from db.mongodb import comicbook_calibre

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn=config.SENTRY_DSN,
    integrations=[FlaskIntegration()]
)

env = Environment(loader=PackageLoader('comicbook', 'webapp/templates'))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins=config.URL)

logging.getLogger('socketio').setLevel(logging.WARNING)
logging.getLogger('engineio').setLevel(logging.WARNING)


def which_type(type):
    if type == 'nhentai':
        return config.DOMAIN.nhentai_net
    elif type == 'ehentai':
        return config.DOMAIN.ehentai_org
    elif type == 'wnacg':
        return config.DOMAIN.wnacg_org
    else:
        return None


def comic_file(domain, id):
    result = comicbook_calibre.find_one({ 'domain': domain.value, 'id': id })
    if result is not None:
        if result['storeInCalibre']:
            return send_file(Storage.get_calibre_epub_file(result['filepath']), mimetype='application/epub+zip')
        else:
            return send_file(Storage.get_comicbook_epub_file(result['filepath']), mimetype='application/epub+zip')
    else:
        return 404


@app.route('/')
def index():
    template = env.get_template('index.html')
    return template.render()


@socketio.on('check-status')
def handle_json(json):
    if json.get('start', False):
        return Crawler.crawl(json['url'])['data']
    else:
        return Crawler.check(json['url'])['data']


@app.route('/comic/download/<type>-<int:id>.epub')
def download_comic(type, id):
    return comic_file(which_type(type), str(id))


@app.errorhandler(404)
def page_not_found(error):
    template = env.get_template('404.html')
    return template.render(), 404


if __name__ == '__main__':
    app.debug = config.DEBUG
    socketio.run(app)

