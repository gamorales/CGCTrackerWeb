import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import db

import logging

cred = credentials.Certificate('firebase/google-services.json')
# default_app = firebase_admin.initialize_app(cred)

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://gpstraker-5fe83.firebaseio.com'
})

def consultarVehiculo(imei, latitude, longitude, local_date):
    # As an admin, the app has access to read and write all data, regradless of Security Rules
    dict_records = db.reference('Vehiculos').get()

    idUsuario = ""
    for record in dict_records:
        try:
            if dict_records[record]['imei']==imei:
                idUsuario = dict_records[record]['idUsuario']
        except KeyError:
            """"Sin la key imei"""
    
    coordenadas = db.reference('Coordenadas/'+idUsuario+"/"+imei+"/"+local_date)
    coordenadas.set({
        "imei": imei,
        "latitud": round(latitude, 6),
        "longitud": round(longitude, 6),
        "fecha": local_date,
        "idUsuario": idUsuario
    })
