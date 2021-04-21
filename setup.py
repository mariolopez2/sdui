#!/usr/bin/env python
# Copyright (c) 2021 Foxconn GDL PCE Paragon Solutions México
# Author: Mario Lopez
# Proyecto: https://github.com/mariolopez2/sdui

import re
import configparser
import socket
import requests
import os
import subprocess
import sys
from time import sleep

# Archivo de configuración Inicial
config = configparser.ConfigParser()
config.read('config.ini')

primer_uso = bool(config['DEFAULT']['FIRST_USE'])
segundo_uso = bool(config['DEFAULT']['SECOND_USE'])

ipv4 = config['DEFAULT']['IPV4']
gateway = config['DEFAULT']['GATEWAY']
dns = config['DEFAULT']['DNS']
mascara = config['DEFAULT']['MASK']

def mascara_red(mask):
    if(mask == 8 ):
        return "255.0.0.0"
    elif(mask == 9):
        return "255.128.0.0"
    elif(mask == 10):
        return "255.192.0.0"
    elif(mask == 11):
        return "255.224.0.0"
    elif(mask == 12):
        return "255.240.0.0"
    elif(mask == 13):
        return "255.248.0.0"
    elif(mask == 14):
        return "255.252.0.0"
    elif(mask == 15):
        return "255.254.0.0"
    elif(mask == 16):
        return "255.255.0.0"
    elif(mask == 17):
        return "255.255.128.0"
    elif(mask == 18):
        return "255.255.192.0"
    elif(mask == 19):
        return "255.255.224.0"
    elif(mask == 20):
        return "255.255.240.0"
    elif(mask == 21):
        return "255.255.248.0"
    elif(mask == 22):
        return "255.255.252.0"
    elif(mask == 23):
        return "255.255.254.0"
    elif(mask == 24):
        return "255.255.255.0"
    elif(mask == 25):
        return "255.255.255.128"
    elif(mask == 26):
        return "255.255.255.192"
    elif(mask == 27):
        return "255.255.255.224"
    elif(mask == 28):
        return "255.255.255.240"
    elif(mask == 29):
        return "255.255.255.248"
    elif(mask == 30):
        return "255.255.255.252"
    elif(mask == 31):
        return "255.255.255.254"
    elif(mask == 32):
        return "255.255.255.255"
    else:
        return "Mascara Invalida"

def validar_ipv4(ipv4):
    try:
        socket.inet_pton(socket.AF_INET,ipv4)
        return True
    except socket.error:
        return False

def iniciar_configuracion():
    if(primer_uso):
        os.system("clear")
        os.system("cat readme.txt")
        mostrar_configuracion()
        configurar_dispositivo()
    else:
        if(segundo_uso):
            configurar_archivos()
            config.set("DEFAULT","SECOND_USE",str(False))
        else:
            sys.exit()

def configurar_archivos():
    os.system("sudo mkdir /home/pi/Sharepoint")
    os.system("sudo mv -rf /home/pi/New_IoT/html /var/www/html/")
    print("Hemos terminado, el ultimo paso es necesario sea ejecutado de manera Manual. Por favor ejecute 'rclone config' y siga las instrucciones en el documento.")


def configurar_dispositivo():
    comando = "cat /proc/cpuinfo | grep -w Serial | awk '{print $3}'"
    sn_completo = os.popen(comando).read()
    sn_corto = sn_completo[10:16]
    nuevo_hostname = "GDLIOT" + sn_corto

    print(" POR FAVOR ESTABLEZCA LOS NUEVOS VALORES.")
    while True:
        nueva_ip = input("Ingrese la nueva IP: ")
        if(validar_ipv4(nueva_ip)):
            print(f"La IP: {nueva_ip} ha sido guardada.")
            break
        else:
            print(f"La IP: {nueva_ip} no es valida, por favor intenta de nuevo.")
    while True:
        nuevo_gateway = input("Ingrese el nuevo gateway: ")
        if(validar_ipv4(nuevo_gateway)):
            print(f"El gateway: {nuevo_gateway} ha sido guardado.")
            break
        else:
            print(f"El gateway: {nuevo_gateway} no es valido, por favor intenta de nuevo.")
    while True:
        nuevo_dns = input("Ingrese el nuevo DNS: ")
        if(validar_ipv4(nuevo_dns)):
            print(f"El DNS: {nuevo_dns} ha sido guardado.")
            break
        else:
            print(f"El DNS: {nuevo_dns} no es valido, por favor intenta de nuevo.")
    while True:
        nueva_mascara = int(input("Ingrese la mascara de red en notación simplificada (Ejemplo 24): "))
        if(nueva_mascara >= 8 and nueva_mascara <= 32):
            print(f"La mascara de red: {mascara_red(nueva_mascara)} ha sido guardada.")
            break
        else:
            print(f"La mascara de red: {mascara_red(nueva_mascara)} no es valida, intenta de nuevo por favor.")
        
    print("Revisa la información introducida: ")    
    print(f"- IP: {nueva_ip}")
    print(f"- Gateway: {nuevo_gateway}")
    print(f"- Mascara de red: {mascara_red(nueva_mascara)}")
    print(f"- DNS: {nuevo_dns}")
    print(f"- Hostname: {nuevo_hostname}")
    while True:
        respuesta = input("¿Deseas aplicar estos cambios? s/n")
        if( respuesta == 's'):
            aplicar_cambios(nueva_ip,nuevo_gateway,nuevo_dns,nueva_mascara,nuevo_hostname)
            config.set("DEFAULT","FIRST_USE",str(False))
            config.set("DEFAULT","IPV4",str(nueva_ip))
            config.set("DEFAULT","GATEWAY",str(nuevo_gateway))
            config.set("DEFAULT","DNS",str(nuevo_dns))
            config.set("DEFAULT","MASK",str(nueva_mascara))
            config.set("DEFAULT","HOSTNAME",str(nuevo_hostname))
            print("Cambios aplicados, el equipo se reiniciará en 10 segundos")
            sleep(10000)
            os.system("sudo shutdown -r now")
            break
        else:
            print("No se han hecho cambios. Programa finalizado.")
            break

def aplicar_cambios(ip,gateway,dns,mascara,hostname):
    # Cambiar datos de red
    file_name = '/etc/dhcpcd.conf'
    with open(file_name, 'r') as f:
        file_text = f.read()

    if len(re.findall('inform', file_text)) == 0:
        newlines = [
            'interface eth0' + '\n',
            'inform ' + ip + '\n',
            'static routers=' + gateway + '\n',
            'static domain_nbame_servers=' + dns + '\n'
        ]
        with open(file_name, 'a+') as f:
            f.writelines(newlines)
    else:
        newlines = []
        with open(file_name) as f:
            lines = f.readlines()
            for l in lines:
                if re.findall('#', l):
                    continue
                elif re.findall('inform [0-9.]*', l):
                    newlines.append('inform ' + ip + '/' + mask + '\n')
                elif re.findall('static routers=', l):
                    newlines.append('static routers=' + gateway + '\n')
                elif re.findall('static domain_name_servers=', l):
                    newlines.append('static domain_name_servers=' + dns + '\n')
                else:
                    newlines.append(l)
        with open(file_name, 'w') as n:
            n.writelines(newlines)

    # Cambiar Hostname
    with open('/etc/hosts', 'r') as file:
        data = file.readlines()
        data[5] = '127.0.1.1    ' + nuevo_hostname
        with open('temp.txt', 'w') as file:
            file.writelines(data)

        os.system('sudo mv temp.txt /etc/hosts')

        with open('/etc/hostname', 'r') as file:
            data = file.readlines()

        data[0] = newHostname

        with open('temp.txt', 'w') as file:
            file.writelines(data)
        os.system('sudo mv temp.txt /etc/hostname')   

def mostrar_configuracion():
    comando = "cat /proc/cpuinfo | grep -w Serial | awk '{print $3}'"
    sn_completo = os.popen(comando).read()
    sn_corto = sn_completo[10:16]
    os.system("clear")
    print("-------------------------------------------------------")
    print("         INFORMACION ACTUAL DEL DISPOSITIVO")
    print(f"Numero de Serie: {sn_corto}")
    print(f"IPV4: {ipv4}")
    print(f"Gateway: {gateway}")
    print(f"Mascara de red: {mascara_red()}")
    print(f"DNS: {dns}")
    print("--------------------------------------------------------")

def instrucciones():
    print("-------------------------------------------------------------------")
    print("setup.py es un script para configurar el dispositivo para subir fotografias a SharePoint")
    print("para ejecutar el script es necesario teclear 'python3 setup.py'")
    print("existen comandos que puedes utilizar - setup.py <comando>")
    print(" - comandos disponibles -")
    print("    -i ó --iniciar       <--- Iniciar el proceso de configuración.")
    print("    -c ó --configuracion <--- Muestra la configuración actual.")
    print("    -h ó --help          <--- Ayuda de como utilizar el script.")
    print("-------------------------------------------------------------------")
    
if __name__ == '__main__':
    if(len(sys.argv) > 1):
        if(sys.argv[1] == "-i" or sys.argv[1] == "--iniciar"):
            iniciar_configuracion()
        elif(sys.argv[1] == "-c" or sys.argv[1] == "--configuracion"):
            mostrar_configuracion()
        elif(sys.argv[1] == "-h" or sys.argv[1] == "--help"):
            instrucciones()
        else:
            print("Comando no valido")
            instrucciones()
    else:
        iniciar_configuracion()
