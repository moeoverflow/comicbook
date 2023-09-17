import config
from crawler.utils.storage import Storage
from db.mongodb import comicbook_calibre


def which_type(type):
    if type == "nhentai":
        return config.DOMAIN.nhentai_net
    elif type == "ehentai":
        return config.DOMAIN.ehentai_org
    elif type == "wnacg":
        return config.DOMAIN.wnacg_com
    else:
        return None


def comic_file(domain, id):
    result = comicbook_calibre.find_one({"domain": domain.value, "id": id})
    if result is None:
        return None
    else:
        if result["storeInCalibre"]:
            return Storage.get_calibre_epub_file(result["filepath"])
        else:
            return Storage.get_comicbook_epub_file(result["filepath"])
