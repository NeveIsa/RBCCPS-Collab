### Operation guide -> Elcita Smart Street light


#### Steps

1. Check gateway is powered on and Ethernet is up
2. Check IP is reachable - 192.168.10.220
3. If needed, login -> pi:raspberry
4. Go to /home/pi
5. Run `./begin all`
6. List of screens
	- drv 		=	Modbus Driver
	- pubamqp	=	Publish Sensors to CDX on resourceName.protected
	- subamqp	=	Subscribe to CDX for commands on resourceName.configure

#### Test procedures
1. Clone this repo
2. Install all python dependencies from files present in /req.txt of this repo and under /ideam/req.txt with `pip3 install -r req.txt`
3. In this folder, run the file test.py with integer argument to set brightness by publishing on resourceName.configure [e.g. `python3 test.py 50` ]
4. Next run `python3 test.py` (without arguments) to subscribe to resourceName queue
5. NOTE: outputLux is inversely proportional to the brightness value set.
