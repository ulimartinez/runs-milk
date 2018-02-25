from flask import Flask
from flask_restful import Resource, Api
from pymongo import MongoClient
app = Flask(__name__)
api = Api(app)
server = MongoClient("159.89.231.140")

db = server.container
class Magazine(Resource):
    def get(self):
        result_all = db.detected
        x = result_all.find().sort({"datetime": -1})
        return x
api.add_resource(Magazine, '/updatedmag')
if __name__ == "__main__":
    app.run(port=80)
