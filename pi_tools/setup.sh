sudo apt update

sudo apt install python python-dev python-pip python3 python3-dev python3-pip screen fish nmap tinc

sudo apt install git mosquitto  mosquitto-clients

#sudo pip install virtualenv


systemctl enable mosquitto

sudo service mosquitto start


[ ! -e RBCCPS-Collab ] && git clone https://github.com/neveisa/RBCCPS-Collab


#[ ! -e smartcity_venv ]  && virtualenv smartcity_venv
#source smartcity_venv/bin/activate

cd RBCCPS-Collab
git pull
echo "PWD: `pwd`"
cat req.txt
pip install -r req.txt
pip3 install -r req.txt
cd ..


cp RBCCPS-Collab/pi_tools/begin.sh .


crontab -l > crontab.tmp
echo "@reboot `realpath begin.sh`" >> crontab.tmp
crontab crontab.tmp


cd RBCCPS-Collab/tinc/tinc_conf

echo ""
echo "*************************"
echo "Change the TINC_SUBNET_IP"
echo "*************************"
sleep 3


nano Makefile
make

cd ../../..

#deactivate


