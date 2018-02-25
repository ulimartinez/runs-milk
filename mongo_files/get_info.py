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
#post_with_id = detected.insert_one(post).inserted_id

result_all = db.detected
x = result_all.find().sort({"datetime": -1})
for d in x:
    pprint(d)
