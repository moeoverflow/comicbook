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



## Contributors

### Code Contributors

This project exists thanks to all the people who contribute. [[Contribute](CONTRIBUTING.md)].
<a href="https://github.com/moeoverflow/comicbook/graphs/contributors"><img src="https://opencollective.com/moeoverflow/contributors.svg?width=890&button=false" /></a>

### Financial Contributors

Become a financial contributor and help us sustain our community. [[Contribute](https://opencollective.com/moeoverflow/contribute)]

#### Individuals

<a href="https://opencollective.com/moeoverflow"><img src="https://opencollective.com/moeoverflow/individuals.svg?width=890"></a>

#### Organizations

Support this project with your organization. Your logo will show up here with a link to your website. [[Contribute](https://opencollective.com/moeoverflow/contribute)]

<a href="https://opencollective.com/moeoverflow/organization/0/website"><img src="https://opencollective.com/moeoverfloworganization/0/avatar.svg"></a>
<a href="https://opencollective.com/moeoverflow/organization/1/website"><img src="https://opencollective.com/moeoverflow/organization/1/avatar.svg"></a>
<a href="https://opencollective.com/moeoverflow/organization/2/website"><img src="https://opencollective.com/moeoverflow/organization/2/avatar.svg"></a>
<a href="https://opencollective.com/cmoeoverflow/organization/3/website"><img src="https://opencollective.com/moeoverflow/organization/3/avatar.svg"></a>
<a href="https://opencollective.com/moeoverflow/organization/4/website"><img src="https://opencollective.com/moeoverflow/organization/4/avatar.svg"></a>
<a href="https://opencollective.com/moeoverflow/organization/5/website"><img src="https://opencollective.com/moeoverfloworganization/5/avatar.svg"></a>
<a href="https://opencollective.com/moeoverflow/organization/6/website"><img src="https://opencollective.com/moeoverflow/organization/6/avatar.svg"></a>
<a href="https://opencollective.com/moeoverflow/organization/7/website"><img src="https://opencollective.com/moeoverflow/organization/7/avatar.svg"></a>
<a href="https://opencollective.com/moeoverflow/organization/8/website"><img src="https://opencollective.com/moeoverflow/organization/8/avatar.svg"></a>
<a href="https://opencollective.com/moeoverflow/organization/9/website"><img src="https://opencollective.com/cmoeoverflow/organization/9/avatar.svg"></a>

## LICENSE

Comicbook is published under GPL 3.0 License. See the LICENSE file for more.
