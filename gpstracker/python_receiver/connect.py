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
        "latitud": latitude,
        "longitud": longitude,
        "fecha": local_date,
        "idUsuario": idUsuario
    })
    #print idUsuario+", "+imei+", "+str(latitude)+", "+str(longitude)+", "+local_date


#print consultarVehiculo("864895030184276")
# print default_app.name

# user = auth.get_user("UPOwPGiuxaUpdJFmTfgahTSLOSx2") # "hFF4aKwDORPd07nsCcdVHb35F0n1") # 'B91B7jpEGGfMBiuIg0hFJFU7c8C2')
# print('Successfully fetched user data: {0}'.format(user.email))

# user = auth.get_user_by_email("cvillada@gmail.com")
# print('Successfully fetched user data: {0}'.format(user.uid))


#page = auth.list_users()
#while page:
#    for user in page.users:
#        print('User: ' + user.uid)
#    # Get next batch of users.
#    page = page.get_next_page()

# Iterate through all users. This will still retrieve users in batches,
# buffering no more than 1000 users in memory at a time.
# for user in auth.list_users().iterate_all():
#    print('User: ' + user.email)