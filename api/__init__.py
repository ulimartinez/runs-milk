from flask import Flask
from flask_restful import Resource, Api
from pymongo import MongoClient
app = Flask(__name__)
api = Api(app)
server = MongoClient("159.89.231.140")

db = server.container


class Magazine(Resource):
    def get(self):
        results = {}
        result_all = db.detected
        x = result_all.find().limit(50).sort("datetime", -1)
        results["x"] = x[0]["x"]
        results["y"] = x[0]["y"]
        return results


api.add_resource(Magazine, '/', '/updatedmag')
if __name__ == "__main__":
    app.run()
