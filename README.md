# hentaibook
convert  comic  to .epub e-book

## Install

``` Shell
$ pip install -r requirements.txt
```

## Usage

``` Shell
$ cd hentaibook
$ python3 main.py --nhentai https://nhentai.net/g/{id}/
$ python3 main.py --ehentai http://g.e-hentai.org/g/{gid}/{token}/
$ python3 main.py --wnacg http://wnacg.org/photos-view-id-{aid}.html
$ python3 main.py --help
```

## Webapp

```Shell
$ cd hentaibook 
$ pip install gunicorn
$ gunicorn -w 4 -b 127.0.0.1:5000 webapp:app --timeout 600
```

## LICENSE

hentaibook is published under GPL 3.0 License. See the LICENSE file for more.