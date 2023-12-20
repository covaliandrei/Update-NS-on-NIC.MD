#!/bin/bash

while :
do
    echo "qwerty"
    cd /home/andrei/PycharmProjects/Update-NS-on-NIC.MD/
    python3 main.py
    while [ $(date +%H:%M) != "09:01" ]; do sleep 1; done
done
