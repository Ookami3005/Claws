#!/bin/zsh
# Script que automatiza la instalación de las herramientas
# que más utilizo en el Hacking Fight Club

# Indicamos que se espera una instrucción
if [[ $# -ne 1 ]] ; then
    echo "Error: No se recibio una instrucción"
    exit 1
fi

# Revisamos la instrucción dada
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
tools=(john nmap ffuf hydra gobuster sqlmap)

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
    sudo $pac_man install -y $john_deps
    clear

    # Clonado del repo oficial
    echo -e "\nClonando John del repositorio oficial...\n"
    temp_dir=$(mktemp -d)
    git clone https://github.com/openwall/john -b bleeding-jumbo "$1/john"
    clear

    # Iniciando la compilación
    echo -e "\nCompilando John...\n"
    cd "$1/john/src" && ./configure > /dev/null && make -s clean /dev/null && make -sj4 /dev/null

    # Configuración de los ejecutables
    echo -e "\nExtrayendo scripts...\n"

    # Generamos un enlace simbólico por temas de compatibilidad con los scripts
    sudo ln -s /usr/bin/python3 /sbin/python

    # Definimos la carpeta donde almacenaremos los ejecutables
    mkdir -p "$HOME/bin"
    mkdir -p "$HOME/bin/2john"

    # Transferir los ejecutables
    cd "$1/john/run"
    for item in *(2john|tojohn)* ; do
        dest=$(cut -d "." -f 1 <<< $item)
        mv $item "${HOME}/bin/2john/$dest"
    done
    cd

    # Añadimos la carpeta al PATH
    echo -e "\nAñadiendo al PATH...\n"
    echo "export PATH=\"${HOME}/bin/2john:$PATH\"" >> $HOME/.zshrc
}

sudo $pac_man $1 -y $tools
clear

if [[ $1 = "install" ]]; then
    # Compilamos scripts adicionales de John
    build_john $(mktemp -d)
else 
    sudo $pac_man remove -y $john_deps
    sudo rm -rf "${HOME}/bin/2john"
fi