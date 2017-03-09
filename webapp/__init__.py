from flask import Flask, send_file, url_for, abort, jsonify
from jinja2 import Environment, PackageLoader, Template

env = Environment(loader=PackageLoader('comicbook', 'webapp/templates'))

from config import DOMAIN
from crawler import Crawler
from crawler.utils.storage import Storage

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

app = Flask(__name__, static_url_path='/webapp/static')


def crawl_done(status, item):
    print("-----crawl done-----")
    print(status)


def check_comic_status(domain, params):
    storage = Storage(domain, params['id'])
    if storage.check_comic():
        return jsonify({
            "code": 200,
            "status": "ready",
            "file": DOWNLOAD_URL[domain].format(params=params)
        })
    else:
        url = COMIC_URLS[domain].format(params=params)
        progress = Crawler.crawl(url, crawl_done)
        if progress:
            return jsonify({
                "code": 202,
                "status": "generating",
                "progress": progress
            })
        return jsonify({
            "code": 201,
            "status": "started"
        })

        abort(404)


def download_comic(domain, id):
    storage = Storage(domain, id)
    return send_file(storage.get_comic_file_path(), mimetype='application/epub+zip')


@app.route('/')
def index():
    template = env.get_template('index.html')
    return template.render()

@app.route('/comic/nhentai/<int:id>')
def check_comic_nhentai_status(id):
    return check_comic_status(DOMAIN.nhentai_net, {'id': str(id)})


@app.route('/comic/ehentai/<int:gid>/<token>')
def check_ehentai_comic(gid, token):
    return check_comic_status(DOMAIN.ehentai_org, {'id': str(gid), 'token': token})


@app.route('/comic/wnacg/<int:aid>')
def check_wnacg_comic(aid):
    return check_comic_status(DOMAIN.wnacg_com, {"id": str(aid)})


@app.route('/comic/download/nhentai-<int:id>.epub')
def download_comic_nhentai(id):
    return download_comic(DOMAIN.nhentai_net, id)


@app.route('/comic/download/ehentai-<int:gid>.epub')
def download_comic_ehentai(gid):
    return download_comic(DOMAIN.ehentai_org, gid)


@app.route('/comic/download/wnacg-<int:aid>.epub')
def download_comic_wnacg(aid):
    return download_comic(DOMAIN.wnacg_com, str(aid))


@app.errorhandler(404)
def page_not_found(error):
    url_for('static', filename='static/404.html')
    url_for('static', filename='static/images/404.png')

    template = env.get_template('404.html')
    return template.render(), 404


if __name__ == '__main__':
    app.debug = True

    app.run()
