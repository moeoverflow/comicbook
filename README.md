# Comicbook
convert  comic  to .epub e-book.

## Install

``` Shell
$ pip3 install -r requirements.txt
```

## Usage

``` Shell
$ cd comicbook
$ python3 comicbook.py --comic https://nhentai.net/g/{id}/
$ python3 comicbook.py --comic http://g.e-hentai.org/g/{gid}/{token}/
$ python3 comicbook.py --comic http://wnacg.org/photos-view-id-{aid}.html
$ python3 comicbook.py --help
```

## Webapp

```Shell
# gunicorn and eventlet
$ pip3 install gunicorn
$ pip3 install eventlet
$ gunicorn --worker-class eventlet -w 1 --threads 12 -b 127.0.0.1:5000 webapp:app
# or
$ python3 comicbook.py --server

# run server and bot.
$ python3 comicbook.py --server --telegram-bot
```

## Docker Deploy Note

Docker Compose deploy structure

``` shell
➜  comicbook_project tree -L 1
.
├── comicbook # Project Git Repo
├── comicbook-calibre-web # Project Git Repo
├── comicbook-calibre-web_data # Persistent Data
├── comicbook-calibre-worker # Project Git Repo
├── comicbook-calibre-worker_data # Persistent Data
├── comicbook_data # Persistent Data
└── docker-compose.yml # Docker Compose configuration

6 directories, 1 file
```

example docker-compose.yml

``` YAML
version: '3'

services:
  comicbook:
    container_name: comicbook
    build:
      context: ./comicbook
      dockerfile: ./Dockerfile
    expose:
      - 8080
    ports:
      - 5000:8080
    volumes:
      - <CALIBRE_LIBRARY>:/usr/src/app/library
      - ./comicbook_data/storage:/usr/src/app/storage
      - ./comicbook_data/config.py:/usr/src/app/config.py
    networks:
      - mongodb_default
  comicbook-calibre-worker:
    container_name: comicbook-calibre-worker
    build:
      context: ./comicbook-calibre-worker
      dockerfile: ./Dockerfile
    networks:
      - mongodb_default
    volumes:
      - <CALIBRE_LIBRARY>:/usr/src/app/library
      - ./comicbook-calibre-worker_data/config.js:/usr/src/app/config.js
      - ./comicbook_data/storage/comic/nhentai.net:/usr/src/app/storage/nhentai
      - ./comicbook_data/storage/comic/ehentai.org:/usr/src/app/storage/ehentai
      - ./comicbook_data/storage/comic/wnacg.org:/usr/src/app/storage/wnacg
  comicbook-calibre-web:
    container_name: comicbook-calibre-web
    build:
      context: ./comicbook-calibre-web
      dockerfile: ./Dockerfile
    volumes:
      - <CALIBRE_LIBRARY>:/data/DATA/comicbook_library
      - ./comicbook-calibre-web_data/app.db:/usr/src/app/app.db
      - ./comicbook-calibre-web_data/gdrive.db:/usr/src/app/gdrive.db
    ports:
      - 5001:8083
networks:
  mongodb_default:
    external: true
```

example comicbook config.py

``` python
# ...

CALIBRE_LIBRARY_PATH = '/usr/src/app/library'

MONGODB_URL = 'mongodb://mongo:27017/'

# ...
```

example comicbook-calibre-worker config.js

``` javascript
module.exports = {
	  libraryPath: '/usr/src/app/library',
	  nhentaiDir: '/usr/src/app/storage/nhentai',
	  ehentaiDir: '/usr/src/app/storage/ehentai',
	  wnacgDir: '/usr/src/app/storage/wnacg',
	  mongodbUrl: 'mongodb://mongo:27017/comicbook',
}
```

PS: You should create your own mongodb docker container.

## LICENSE

Comicbook is published under GPL 3.0 License. See the LICENSE file for more.
