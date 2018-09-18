#!/bin/bash

[ -z $1 ] && sleep 20

cd RBCCPS-Collab/MBDriver/
screen -L -dmS drv python3 -B MBMASTER.py


cd ../tinc
screen -L -dmS tinc ./tinc.start

cd ../ideam/amqp
#screen -L -dmS m2i  sh start.sh
#screen -L -dmS i2m python3 ideam2modbus.py
sh start.sh

sleep 5
screen -ls

