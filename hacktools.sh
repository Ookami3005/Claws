#!/bin/bash
# Script que automatiza la instalación de las herramientas
# que más utilizo en el Hacking Fight Club

# Indicamos que se espera una instrucción
if [[ $# -ne 1 ]] ; then
    echo "Error: No se recibio una instrucción"
    exit 1
fi

# Revisamos la instrucción dada es válida
if [[ $1 != "install" ]] && [[ $1 != "remove" ]] ; then
    echo "Error: Argumento incorrecto"
    exit 1
fi

# Definimos a Nala como herramienta predeterminada para instalar los paquetes
pac_man=nala

# De no tener instalado Nala redefinimos la herramienta como APT
if ! command -v nala > /dev/null ; then
    pac_man=apt
fi

# Herramientas principales en los repositorios oficiales
tools=(telnet john nmap ffuf hydra gobuster)

# Dependencias de John The Reaper
john_deps=(libssl-dev zlib1g-dev yasm pkg-config libgmp-dev libpcap-dev libbz2-dev)

# Función auxiliar que compila los scripts extra de John desde el repositorio oficial
build_john () {

    # Pedimos un argumento
    if [[ $# -ne 1 ]] ; then
        exit 1
    fi

    # Instalar las dependencias
    echo -e "\nInstalando dependencias de John...\n"
    sudo $pac_man install -y ${john_deps[@]}
    clear

    # Clonado del repo oficial
    echo -e "Clonando John del repositorio oficial...\n"
    temp_dir=$(mktemp -d)
    git clone https://github.com/openwall/john -b bleeding-jumbo "$1/john" || exit 1
    clear

    # Iniciando la compilación
    echo -e "Compilando John...\n"
    cd "$1/john/src" && ./configure > /dev/null && make -s clean /dev/null && make -sj4 /dev/null

    # Configuración de los ejecutables
    echo -e "Extrayendo scripts...\n"

    # Generamos un enlace simbólico por temas de compatibilidad con los scripts
    command -v python > /dev/null || sudo ln -s /usr/bin/python3 /sbin/python 2> /dev/null

    # Definimos la carpeta donde almacenaremos los ejecutables
    mkdir -p "$HOME/bin"
    mkdir -p "$HOME/bin/2john"

    # Transferir los ejecutables
    cd "$1/john/run"
    for item in *{2,to}john* ; do
        dest=$(cut -d "." -f 1 <<< $item)
        mv $item "${HOME}/bin/2john/$dest"
    done
    cd

    echo -e "Por favor añada al PATH la carpeta '~/bin/2john'...\n"
}

setup_sqlmap () {

    # Limpiamos (si existe) la instalación de sqlmap del repositorio
    sudo nala purge sqlmap 2> /dev/null

    # Creamos (si no existe la carpeta ~/bin)
    mkdir -p ${HOME}/bin

    # Clonamos el repositorio oficial de sqlmap a nuestra carpeta de binarios
    git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git ${HOME}/bin/sqlmap-dev
    clear

    # Creamos un enlace simbólico del ejecutable principal del reposiorio a una ubicación del PATH (/usr/bin)
    sudo ln -sv ${HOME}/bin/sqlmap-dev/sqlmap.py /usr/bin/sqlmap

    echo -e "SQLMAP configurado!\n"
}

# Instalamos las herramientas principales del repositorio
sudo $pac_man $1 -y ${tools[@]}
clear

if [[ $1 = "install" ]]; then

    # Configuramos sqlmap
    setup_sqlmap

    # Compilamos scripts adicionales de John
    build_john $(mktemp -d)

else

    # Destruimos los Scripts auxiliares de John
    sudo rm -rf "${HOME}/bin/2john"

    # Destruimos el directorio y el enlace simbólico de sqlmap
    sudo rm -rf ${HOME}/bin/sqlmap-dev
    sudo rm /usr/bin/sqlmap

    echo "Listo!"
fi
