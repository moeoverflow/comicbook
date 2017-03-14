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



## LICENSE

Comicbook is published under GPL 3.0 License. See the LICENSE file for more.
