from flask import Flask, send_file
from flask_socketio import SocketIO
from jinja2 import Environment, PackageLoader

import config
from crawler import Crawler
from crawler.utils.storage import Storage

env = Environment(loader=PackageLoader('comicbook', 'webapp/templates'))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


def which_type(type):
    if type == 'nhentai':
        return config.DOMAIN.nhentai_net
    elif type == 'ehentai':
        return config.DOMAIN.ehentai_org
    elif type == 'wnacg':
        return config.DOMAIN.wnacg_com
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
    return Crawler.crawl(json['url'])['data']


@app.route('/comic/download/<type>-<int:id>.epub')
def download_comic(type, id):
    return comic_file(which_type(type), id)


@app.errorhandler(404)
def page_not_found(error):
    template = env.get_template('404.html')
    return template.render(), 404


if __name__ == '__main__':
    app.debug = config.DEBUG
    socketio.run(app)

