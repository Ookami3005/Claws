# Claws

Recopilatorio de *Scripts* que espero sean utiles.

En esta rama principal yacen los *Scripts* que pueden ejecutarse en cualquier distro *Linux*, pues
no requieren de herramientas específicas de alguna distro (como de su gestor de paquetes).

Por supuesto, asumo que no tienes una instalación mínima o al menos que no tendrás problema en instalar
las herramientas que haya utilizado para la redacción de estos *Scripts*

Si no estas familiarizado con la ejecución de un *Script*, la idea básica (suponiendo que te encuentras en la carpeta donde están los *Scripts*)
es:

1. Dar permisos de ejecución al *Script*

   ```bash
    chmod u+x script.sh
   ```

3. Ejecutar el *Script* con './':

   ```bash
   ./script.sh
   ```

## Índice

- **Decodificación**
- **Portswigger Web Academy**
  - **Inyección SQL**
    - [Inyección condicional a ciegas](./portswigger-academy/blindsqli_lab.py)
- **x3CTF 2025**
  - **Web**
  - **Crypto**
    - *Sourceless-Crypto*: [Mi solución](./x3ctf-2025/crypto/sourceless.py) o [Solución oficial](./x3ctf-2025/crypto/official_sourceless.py)
  - **Reversing**
    - [Pickle-Season](./x3ctf-2025/rev/pickle-season.py)
    - [NotCrypto](./x3ctf-2025/rev/notcrypt.py)
  - **PWN**
    - [Devnull-as-a-service](./x3ctf-2025/pwn/dev_null.py)


> Besos a Danna

- Ookami
