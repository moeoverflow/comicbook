import pymongo
from config import MONGODB_URL

client = pymongo.MongoClient(MONGODB_URL)
db = client.comicbook
comicbook_calibre = db.comicbookcalibres
