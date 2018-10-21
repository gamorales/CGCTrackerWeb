from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify

application= Flask(__name__)
api = Api(application)

class GpsRest(Resource):
    def get(self, imei, command):
        return jsonify({"imei": imei, "command": command})


api.add_resource(GpsRest, '/gps_rest/<imei>/<command>') # Route_3


if __name__ == '__main__':
     application.run(host='0.0.0.0', port=8080)

