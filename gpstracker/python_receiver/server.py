from datetime import datetime
from socket import *
import logging

import decoder

HOST = '0.0.0.0'
PORT = 8889

# Configurar el logger
current_date = datetime.now()
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logfile = "logs/file"+(str(current_date)[0:10].replace('-', ''))+".log"
logging.basicConfig(filename=logfile, level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger()

try :
    serversocket = socket(AF_INET,SOCK_STREAM)
    serversocket.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1)
    serversocket.bind((HOST,PORT))
    print 'bind success'
    serversocket.listen(5)
    print 'listening'

    while True:
        (clientsocket, address) = serversocket.accept()
        conexion = "Got client request from %s" % str(address)
        print conexion
        logger.info(conexion)
        #clientsocket.send('True')

        contador = 0
        data = clientsocket.recv(2048).split(';')
        for record in data:
            # Evitamos los registros vacios
            if record.strip()!="":
                decoder.decode(record)
                contador += 1
        
        clientsocket.send('True')
        clientsocket.close()

        logger.info("Entraron %d registros" % contador)
        print "Entraron %d registros" % contador
except KeyboardInterrupt:
    print "Bye bye!"
