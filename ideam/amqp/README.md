### Operation guide -> Elcita Smart Street light


##### All services are brought up on reboot

#### Steps to debug if reboot doesn't solve the issues
---
1. Check gateway is powered on and Ethernet is up
2. Check IP is reachable - 192.168.10.220
3. If needed, login -> pi:raspberry


4. Become root by `sudo su`

5. Run `screen -ls`

6. Check if 3 screens named `drv`, `pubamqp` and `subamqp` are running [ `tinc` may be running aswell ]

7. If the anyone of the screens above are not running then proceed below
8. Go to /home/pi
9. Run `./begin all`
10. List of screens
	- drv 		=	Modbus Driver
	- pubamqp	=	Publish Sensors to CDX on resourceName.protected
	- subamqp	=	Subscribe to CDX for commands on resourceName.configure

#### Test procedures [Not on the gateway, but a separate machine]
1. Clone this repo
2. Install all python dependencies from files present in /req.txt of this repo and under /ideam/req.txt with `pip3 install -r req.txt`
3. In this folder, run the file test.py with integer argument to set brightness by publishing on resourceName.configure [e.g. `python3 test.py 50` ]
4. Next run `python3 test.py` (without arguments) to subscribe to resourceName queue
5. NOTE: outputLux is inversely proportional to the brightness value set.
