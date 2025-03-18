#!/usr/bin/env python3

import requests
import re

# URL del login al que quieres enviar los datos
url = "http://verbal-sleep.picoctf.net:50313/impossibleLogin.php"

# Lectura de los pdf SHAttered con el mismo hash
reader1 = open('./shattered-1.pdf','rb')
reader2 = open('./shattered-2.pdf','rb')

# Contenido de los archivos SHAttered, en este caso, se simulan como strings
shattered1_content = reader1.read()
shattered2_content = reader2.read()

# Crear los parámetros para la solicitud (username y pwd)
params = {
    "username": shattered1_content,  # Puedes enviar el contenido del ataque SHAttered 1 como username
    "pwd": shattered2_content         # Puedes enviar el contenido del ataque SHAttered 2 como pwd
}

# Enviar la solicitud POST con los parámetros
response = requests.post(url, data=params)

# Mostrar la respuesta
flag = re.search(r'picoCTF{.*}',response.text)
if flag:
    print(flag.group())
