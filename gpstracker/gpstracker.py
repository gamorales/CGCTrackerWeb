from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify

import os

application= Flask(__name__)
api = Api(application)

class GpsRest(Resource):
    # Value puede ser: speed, time, distance o latitud01
    def get(self, imei, command, value=0, longitud01=0, latitud02=0, longitud02=0):
        path_script = os.path.dirname(os.path.realpath(__file__))+"/../websocket/comandos/"+imei
        f = open(path_script, "w")
        if longitud01!=0 and latitud02!=0 and longitud02!=0:
            f.write(command+","+value+","+longitud01+","+latitud02+","+longitud02)
        else:
            f.write(command+","+value)
        f.close()
        return jsonify({"imei": imei, "command": command, "path": path_script, "value": value,
                        "longitud01":longitud01, "latitud02":latitud02, "longitud02":longitud02})


api.add_resource(GpsRest, '/gps_rest/<imei>/<command>/<value>/<longitud01>/<latitud02>/<longitud02>') # Route_3


if __name__ == '__main__':
     application.run(host='0.0.0.0', port=8080, debug=True)

