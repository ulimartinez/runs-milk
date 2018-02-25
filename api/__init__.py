from flask import Flask
from flask_restful import Resource, Api
app = Flask(__name__)
api = Api(app)
class Magazine(Resource):
    def get(self):
        return {'WTF':'Im api'}
api.add_resource(Magazine, '/')
if __name__ == "__main__":
    app.run(port=80)
