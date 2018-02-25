from pymongo import MongoClient
from pprint import pprint
import datetime

server = MongoClient("159.89.231.140")

db = server.container

post = { "contains": "",
         "lat": "",
         "lon": "",
         "x": "",
         "y": "",
         "time": datetime.datetime.utcnow()
}

detected = db.detected
post_with_id = detected.insert_one(post).inserted_id
