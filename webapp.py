from flask import Flask, send_file , url_for, abort, jsonify
import os.path
import shutil
import time

import main

COMIC_URL = {
    'nhentai.net': 'https://nhentai.net/g/{params[id]}/',
    'e-hentai.org': 'http://g.e-hentai.org/g/{params[gid]}/{params[token]}/'
}
COMIC_FILE_NAME = {
    'nhentai.net': 'nhentai-{params[id]}.epub',
    'e-hentai.org': 'ehentai-{params[gid]}-{params[token]}.epub'
}
COMIC_MAIN_PATH = os.path.expanduser('./static/comic')
COMIC_PATHS = {
    'nhentai.net': '%s/nhentai'%(COMIC_MAIN_PATH),
    'e-hentai.org': '%s/ehentai'%(COMIC_MAIN_PATH)
}
COMIC_DOWNLOADING_PATHS = {
    'nhentai.net': '%s/downloading'%(COMIC_PATHS['nhentai.net']),
    'e-hentai.org': '%s/downloading'%(COMIC_PATHS['e-hentai.org'])
}

if not os.path.exists(COMIC_MAIN_PATH):
    os.makedirs(COMIC_MAIN_PATH)
for (key, path) in COMIC_PATHS.items():
    if not os.path.exists(path):
        os.makedirs(path)
for (key, path) in COMIC_DOWNLOADING_PATHS.items():
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def check_comic(source, params):
    file_name = COMIC_FILE_NAME[source].format(params=params)
    file_path = '%s/%s'%(COMIC_PATHS[source], file_name)
    file_downloading_path = '%s/%s'%(COMIC_DOWNLOADING_PATHS[source], file_name)

    if os.path.exists(file_downloading_path):
        for i in range (0, 6*5):
            time.sleep(10)
            if os.path.exists(file_path):
                return jsonify({ 'status': 'success' })
            elif not os.path.exists(file_downloading_path):
                break
        return jsonify({ 'status': 'failure' })
    elif os.path.exists(file_path):
        return jsonify({ 'status': 'success' })
    else:
        if main.CREATE_EPUB[source](COMIC_URL[source].format(params=params), file_downloading_path):
            os.rename(file_downloading_path, file_path)
        if os.path.exists(file_path):
            return jsonify({ 'status': 'success' })
        else:
            return jsonify({ 'status': 'failure' })

def download_comic(source, params):
    file_name = COMIC_FILE_NAME[source].format(params=params)
    file_path = '%s/%s'%(COMIC_PATHS[source], file_name)

    if os.path.exists(file_path):
        return send_file(file_path, mimetype='application/epub+zip')
    else:
        abort(404)


app = Flask(__name__)

@app.route('/')
def index():
    url_for('static', filename='css/hentaibook.css')
    url_for('static', filename='images/background.jpg')
    url_for('static', filename='favicon.ico')
    url_for('static', filename='semantic/dist/semantic.min.css')
    url_for('static', filename='semantic/dist/semantic.min.js')
    return send_file('static/index.html')

@app.route('/comic/nhentai/download/<int:id>')
def download_nhentai_comic(id):
    return download_comic('nhentai.net', { "id": id })
@app.route('/comic/nhentai/check/<int:id>')
def check_nhentai_comic(id):
    return check_comic('nhentai.net', { "id": str(id) })

@app.route('/comic/ehentai/download/<int:gid>/<token>')
def download_ehentai_comic(gid, token):
    return download_comic('e-hentai.org', { 'gid': str(gid), 'token': token })
@app.route('/comic/ehentai/check/<int:gid>/<token>')
def check_ehentai_comic(gid, token):
    return check_comic('e-hentai.org', { 'gid': str(gid), 'token': token })

@app.errorhandler(404)
def page_not_found(error):
    url_for('static', filename='static/404.html')
    url_for('static', filename='static/images/404.png')
    return send_file('static/404.html'), 404

if __name__ == '__main__':
    app.debug = True
    app.run()
