# hentaibook
convert  comic on [nhentai.net](https://nhentai.net) to .epub e-book

## Install

``` Shell
$ pip install -r requirements.txt
```

## Usage

``` Shell
$ cd hentaibook
$ python3 main.py -l https://nhentai.net/g/123170/

$ python3 main.py --help
```

## Webapp

```Shell
$ cd hentaibook 
$ pip install gunicorn
$ gunicorn -w 4 -b 127.0.0.1:5000 webapp:app
```

## LICENSE

hentaibook is published under GPL 3.0 License. See the LICENSE file for more.