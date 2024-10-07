#!/bin/zsh
# Script que automatiza la instalación de las herramientas
# que más utilizo en el Hacking Fight Club

if [[ $# -ne 1 ]] ; then
    echo "No se recibio una instrucción"
    exit 1
fi

if [[ $1 != "install" ]] && [[ $1 != "remove" ]] ; then
    echo "Argumento incorrecto"
    exit 1
fi

pac_man=nala

if ! command -v nala > /dev/null ; then
    pac_man=apt
fi

# Herramientas principales en los repositorios oficiales
tools=(nmap ffuf hydra gobuster sqlmap)

john_deps=(git build-essential libssl-dev zlib1g-dev yasm pkg-config libgmp-dev libpcap-dev libbz2-dev)

echo -e "Instalando herramientas del repositorio...\n"
sudo $pac_man $1 -y $tools

if [[ $1 = "install" ]]; then
    elec="s"
    echo -n "Desea instalar 'John The Reaper jumbo'? [s/n]: "
    read elec

    if [[ $elec = s ]]; then

        # Borrar (si existe) la versión de John del repositorio
        command -v john > /dev/null && sudo $pac_man remove -y john 2> /dev/null

        # Dependencias
        sudo $pac_man install -y $john_deps

        # Clonado del repo oficial
        echo -e "Clonando John del repositorio oficial...\n"
        temp_dir=$(mktemp -d)
        git clone https://github.com/openwall/john -b bleeding-jumbo "$temp_dir/john"
        echo -e "Compilando John...\n"
        cd "$temp_dir/john/src" && ./configure && make -s clean && make -sj4

        echo -e "\nExtrayendo scripts...\n"
        sudo ln -s /usr/bin/python3 /sbin/python
        cd "$temp_dir/john/run"
        mkdir -p "$HOME/bin"
        mkdir -p "$HOME/bin/2john"
        mv john "${HOME}/bin/2john/."
        for item in *(2john|tojohn)* ; do
            dest=$(cut -d "." -f 1 <<< $item)
            mv $item "${HOME}/bin/2john/$dest"
        done

        echo -e "\nAñadiendo al PATH...\n"
        echo "export PATH=\"${HOME}/bin/2john:$PATH\"" >> $HOME/.zshrc
        cd
    fi
fi

