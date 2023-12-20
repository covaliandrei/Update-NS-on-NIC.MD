#!/bin/bash

while :
do
    echo "Wait for 09:01 next morning"
    while [ $(date +%H:%M) != "09:01" ]; do sleep 1; done

    echo "Starting main.py"
    cd /home/andrei/PycharmProjects/Update-NS-on-NIC.MD/
    python3 main.py
done

