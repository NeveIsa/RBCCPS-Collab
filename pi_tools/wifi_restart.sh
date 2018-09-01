wget --spider http://iiitd.zenatix.com:9103/time
if [[ $? -eq 0 ]]; then
        echo "Online"
else
        echo "Offline"
        sudo ifdown --force wlan0
        # let things settle
        sleep 2
        # restart the interface
        sudo ifup --force wlan0
fi

