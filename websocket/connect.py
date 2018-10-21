import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import db

from datetime import datetime, timedelta

import logging
import os

path_script = os.path.dirname(os.path.realpath(__file__))

cred = credentials.Certificate(path_script+'/firebase/google-services.json')
# default_app = firebase_admin.initialize_app(cred)

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://gpstraker-5fe83.firebaseio.com'
})

def consultarVehiculo(imei, latitude, longitude, local_date, type_data, speed, course):
    # As an admin, the app has access to read and write all data, regradless of Security Rules
    dict_records = db.reference('Vehiculos').get()

    idUsuario = ""
    for record in dict_records:
        try:
            if dict_records[record]['imei']==imei:
                idUsuario = dict_records[record]['idUsuario']
        except KeyError:
            """"Sin la key imei"""
    
    # Se le restan cinco horas al servidor ya que si se modifica la fecha, se pierde la conexión con firebase
    fecha_now = datetime.now()
    fecha_delta = fecha_now - timedelta(hours=5, minutes=0)
    fecha_sistema = str(fecha_delta).replace(' ', '').replace('-', '').replace(':', '')[2:14]

    hora_sistema = fecha_sistema[6:12]

#    fecha_sistema = str(int(str(datetime.now()).replace(' ', '').replace('-', '').replace(':', '')[2:14]) - 50000)
#    fecha_sistema = str(datetime.now()).replace('-', '').replace(' ', '').replace(':', '')[2:14]    
    coordenadas = db.reference('Coordenadas/'+idUsuario+"/"+imei+"/"+fecha_sistema[0:6]+"/"+hora_sistema)
    coordenadas.set({
        "imei": imei,
        "latitud": round(latitude, 6),
        "longitud": round(longitude, 6),
        "fecha": fecha_sistema,
        "fecha_gps": local_date,
        "idUsuario": idUsuario,
        "tipo": type_data,
        "velocidad": (str(speed) if speed!=None else '0'),
        "curso": (str(course) if course!=None else '0')
    })
