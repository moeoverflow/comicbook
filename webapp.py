from flask import Flask, send_file , url_for, abort, jsonify
import os.path
import shutil
import time

import main


COMIC_PATH = os.path.expanduser('./static/comic/')
COMIC_DOWNLOADING_PATH = os.path.expanduser('%sdownloading/'%(COMIC_PATH))

if not os.path.exists(COMIC_PATH):
    os.makedirs(COMIC_PATH)
if os.path.exists(COMIC_DOWNLOADING_PATH):
    shutil.rmtree(COMIC_DOWNLOADING_PATH)
os.makedirs(COMIC_DOWNLOADING_PATH)


app = Flask(__name__)

@app.route('/')
def index():
    url_for('static', filename='css/hentaibook.css')
    url_for('static', filename='images/background.jpg')
    url_for('static', filename='favicon.ico')
    url_for('static', filename='semantic/dist/semantic.min.css')
    url_for('static', filename='semantic/dist/semantic.min.js')
    return send_file('static/index.html')

@app.route('/comic/<int:id>')
def comic(id):
    print('comic')
    print(id)
    file_path = '%snhentai-%s.epub'%(COMIC_PATH, id)

    if os.path.exists(file_path):
        return send_file(file_path, mimetype='application/epub+zip')
    else:
        abort(404)

@app.route('/comic/download/<int:id>')
def checkComic(id):
    print('checkComic')
    print(id)
    file_name = 'nhentai-%s.epub'%(id)
    file_path = COMIC_PATH + file_name
    file_downloading_path = COMIC_DOWNLOADING_PATH + file_name

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
        if main.general_book('https://nhentai.net/g/%s/'%(id), file_downloading_path):
            os.rename(file_downloading_path, file_path)
        if os.path.exists(file_path):
            return jsonify({ 'status': 'success' })
        else:
            return jsonify({ 'status': 'failure' })

@app.errorhandler(404)
def page_not_found(error):
    url_for('static', filename='404.html')
    return send_file('static/404.html'), 404

if __name__ == '__main__':
    app.debug = True
    app.run()
