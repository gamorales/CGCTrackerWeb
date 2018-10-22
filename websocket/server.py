#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import logging
import sys
import threading
import decoder
import sys
import os

from _thread import *
from datetime import datetime
from commands import commands

HOST = "0.0.0.0"
PORT = 8889

# Configurar el logger
path_script = os.path.dirname(os.path.realpath(__file__))
current_date = datetime.now()
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logfile = path_script+"/logs/file"+(str(current_date)[0:10].replace('-', ''))+".log"
logging.basicConfig(filename=logfile, level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger()
  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print ("Socket creado")

def clientes(conn):
    welcome = "Bienvenido al server"
    conn.send(welcome.encode())

    while True:
        data = conn.recv(1024) #
        datos =  data.decode().split(';')
        reply = "OK. " + datos[0]
        contador = 0
        if not data:
            break;

        if datos[0][0:2]=="##": # ##,imei:864895030184277,A":
            conn.sendall('LOAD'.encode())
            logger.info('LOAD')
        elif datos[0][0].isdigit(): # 864895030184277
            imei = '**,imei:%s,B;' % str(datos[0])
            conn.sendall(imei.encode())
            logger.info('**,imei:%s,B;' % str(datos[0]))
        elif datos[0][0:4]=="imei": # imei:865328021048409,tracker,141210110820,,F,030823.000,A,3745.9502,S,14458.2049,E,1.83,119.35,,0,0,0.0%,,;
            conn.sendall('ON'.encode())
            logger.info('ON')

            # Se buscará si hay comandos para enviarle al GPS
            archivo = path_script+"/comandos/"+datos[0][5:20]
            try:
                import os
                if os.path.exists(archivo):
                    f = open(archivo,"r")
                    content = f.readlines()
                    for linea in content:
                        comando = linea.rstrip().split(',') # 0->command, 1->speed/time/distance/latitud01, 2->longitud01, 3->latitud02, 4-> longitud02
                        comando_enviar = commands[comando[0]].replace("#imei#", comando[1])
                        # El primer caso es para geofence
                        if len(comando)==5:
                            comando_enviar = commands[comando[0]].replace("#latitud01#", comando[1])
                            comando_enviar = commands[comando[0]].replace("#longitud01#", comando[2])
                            comando_enviar = commands[comando[0]].replace("#latitud02#", comando[3])
                            comando_enviar = commands[comando[0]].replace("#longitud02#", comando[4])
                        # Segundo caso es para velocidad, tiempo o distancia
                        elif len(comando)==2:
                            comando_enviar = commands[comando[0]].replace("#time#", comando[1])
                            comando_enviar = commands[comando[0]].replace("#speed#", comando[1])
                            comando_enviar = commands[comando[0]].replace("#distance#", comando[1])
                        else:
                            comando_enviar = commands[comando[0]]

                        conn.sendall(comando_enviar.encode())
                        logger.info(comando_enviar)
                    f.close()
                    os.remove(archivo)
            except:
                pass

            for record in datos:
                # Evitamos los registros vacios
                if record.strip()!="":
                    if record.find("tracker")>=0:
                        print (record + "\n\n")
                        decoder.decode(record)
                        logger.info(record)
                        contador += 1

            logger.info("Entraron %d registros" % contador)

        recibido = 'received "%s"' % datos
        logger.info(recibido)
        logger.info("Entraron %d registros" % contador)
 
#        print (reply)
#        conn.sendall(data)

    conn.close()

def main():
    try:
        s.bind((HOST, PORT))
    except socket.error:
        print ("Binding failed")
        sys.exit()

    s.listen(10)

    while True:
        conn, addr = s.accept()
        conexion = "Cliente: " + addr[0] + ":" + str(addr[1])
        logger.info(conexion)
        print (conexion + "\n")
        start_new_thread(clientes, (conn,))

    s.close()

if __name__ == '__main__': 
    try:
        main() 
    except KeyboardInterrupt:
        logger.info("Cerrado abruptamente")
        print ("Bye bye!")

