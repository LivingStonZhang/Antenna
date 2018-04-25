#!/bin/sh
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
sudo dpkg-reconfigure locales
sudo apt install sysstat iotop tree
sudo pip3 install -r requirement.txt
