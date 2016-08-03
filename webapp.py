from flask import Flask, send_file , url_for, abort, jsonify
import os.path
import main

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
    filepath = './static/comic/nhentai-%s.epub'%(id)
    if os.path.exists(filepath):
        return send_file(filepath, mimetype='application/epub+zip')
    else:
        abort(404)

@app.route('/comic/download/<int:id>')
def checkComic(id):
    filename = 'nhentai-%s.epub'%(id)
    filepath = './static/comic/%s'%(filename)
    print(os.path.expanduser(filepath))
    if not os.path.exists('./static/comic'):
        os.makedirs('./static/comic')
    if os.path.exists(os.path.expanduser(filepath)):
        return jsonify({ 'status': 'success' })
    else:
        if main.generalBook('https://nhentai.net/g/%s/'%(id), './static/comic/downloading/%s'%(filename)):
            os.rename('./static/comic/downloading/%s'%(filename), filepath)
        if os.path.exists(filepath):
            return jsonify({ 'status': 'success' })
        else:
            return jsonify({ 'status': 'failure' })

if __name__ == '__main__':
    app.debug = True
    app.run()
