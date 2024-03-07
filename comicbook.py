# coding: UTF-8

import json
import argparse
import logging

from crawler import Crawler


logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="comicbook")
    parser.add_argument(
        "-c",
        "--comic",
        required=True,
        help="a comic link on nhentai.net, e-hentai.org, wnacg.com",
    )
    parser.add_argument(
        "-f",
        "--format",
        default="epub",
        choices=["epub", "cbz"],
        help="Specify a format.",
    )
    parser.add_argument("-o", "--output", help="Specify a output path.")
    args = parser.parse_args()

    if args.output:
        result = Crawler.download_manually(args.comic, args.format, args.output)
        print(result)
    else:
        result = Crawler.download(args.comic)
        result.pop("item")
        print(json.dumps(result, indent=2))
