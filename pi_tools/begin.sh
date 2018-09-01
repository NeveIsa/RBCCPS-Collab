
sleep 20

cd RBCCPS-Collab/MBDriver/
screen -L -dmS drv python3 MBMASTER.py

cd ../ideam
screen -L -dmS m2i  sh start.sh

screen -L -dmS i2m python3 ideam2modbus.py
sleep 2
screen -ls
