#!/bin/bash

PASTE_BIN_URL_SERVER_KEY="https://pastebin.com/raw/52emnhCm"

apt install tinc

TINC_CLOUD_SERVER_NODE_NAME=externalnyc
TINC_CLOUD_SERVER_USER=root
TINC_CLOUD_SERVER_IP=ideam
TINC_CLOUD_SERVER_NET_NAME=netname

TINC_CLOUD_SERVER_TINC_DIR="~/test/tinc/"
TINC_CLOUD_SERVER_NET_NAME_DIR="$TINC_CLOUD_SERVER_TINC_DIR/$TINC_CLOUD_SERVER_NET_NAME"


NODE_NAME=$(hostname)


TINC_DIR="test/tinc"
NET_NAME=netname
NET_NAME_DIR="$TINC_DIR/$NET_NAME"

[ -z $TINC_SUBNET_IP ] && TINC_SUBNET_IP=$1
[ -z $TINC_SUBNET_IP ] && TINC_SUBNET_IP=10.0.0.101


echo "TINC_SUBNET_IP: $TINC_SUBNET_IP"
sleep 2

TINC_SUBNET_MASK=24
TINC_SUBNET="$TINC_SUBNET_IP/$TINC_SUBNET_MASK"


[ "$TINC_SUBNET_MASK" -eq "24" ] && TINC_SUBNET_MASK_EXPANDED="255.255.255.0"
[ "$TINC_SUBNET_MASK" -eq "16" ] && TINC_SUBNET_MASK_EXPANDED="255.255.0.0"
[ "$TINC_SUBNET_MASK" -eq "8" ] && TINC_SUBNET_MASK_EXPANDED="255.0.0.0"


mkdir -p "$NET_NAME_DIR/hosts"

echo "$NET_NAME" >> "$TINC_DIR/nets.boot"


echo "Name = $NODE_NAME
AddressFamily = ipv4
Interface = tun0
ConnectTo = $TINC_CLOUD_SERVER_NODE_NAME" > "$NET_NAME_DIR/tinc.conf"

echo "Subnet = $TINC_SUBNET_IP/32" > "$NET_NAME_DIR/hosts/$NODE_NAME"


echo "ifconfig \$INTERFACE $TINC_IP netmask $TINC_SUBNET_MASK_EXPANDED" > "$NET_NAME_DIR/tinc-up"
echo "ifconfig \$INTERFACE down" > "$NET_NAME_DIR/tinc-down"

chmod 755 $NET_NAME_DIR/tinc-*




#Run key gen
#sudo tinc -n $NET_NAME -K4096



#copy server to local
#scp $TINC_CLOUD_SERVER_USER@$TINC_CLOUD_SERVER_IP:$TINC_CLOUD_SERVER_NET_NAME_DIR/hosts/$TINC_CLOUD_SERVER_NODE_NAME $NET_NAME_DIR/hosts
wget $PASTE_BIN_URL_SERVER_KEY -O $NET_NAME_DIR/hosts/$TINC_CLOUD_SERVER_NODE_NAME

#fix for pastebin stripping \n
echo -e "\n" >> $NET_NAME_DIR/hosts/$TINC_CLOUD_SERVER_NODE_NAME 


#copy local to server
#scp $NET_NAME_DIR/hosts/$NODE_NAME $TINC_CLOUD_SERVER_USER@$TINC_CLOUD_SERVER_IP:$TINC_CLOUD_SERVER_NET_NAME_DIR/hosts/


echo "*******************************************************************************"
echo "*******************************************************************************"

cat $NET_NAME_DIR/hosts/$NODE_NAME


echo "*******************************************************************************"
echo "*******************************************************************************"
