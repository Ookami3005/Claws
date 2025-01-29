#!/usr/bin/bash

mkdir -p ${HOME}/.local/src
git clone https://github.com/openwall/john.git ${HOME}/.local/src/john
cd ${HOME}/.local/src/john/src/ || exit 1
./configure && make -s clean && sudo make -sj4
sudo ln -sv ${HOME}/.local/src/john/run/ssh2john.py /usr/local/bin/ssh2john
