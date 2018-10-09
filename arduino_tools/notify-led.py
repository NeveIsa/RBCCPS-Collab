from pyfirmata import Arduino, util
import time



class device:
	def __init__(self,rpin,gpin,bpin,beeppin,activeLow=False):
		import serial.tools.list_ports
		ports=list(serial.tools.list_ports.comports()) 
		for _ in range(len(ports)):
			print ("{} -> {}".format(_,ports[_].device))
		
		self.device = ports[-1].device

		self.rpin = rpin
		self.gpin = gpin
		self.bpin = bpin

		self.beeppin = beeppin

		self.board = Arduino(self.device)
		self.activeLow = activeLow

		


	def glow(self,color,state=True,milliseconds=0):
		print(color,state)

		state ^= self.activeLow
		pincolormap = {"red":self.rpin,"green":self.gpin,"blue":self.bpin}
		pin=pincolormap[color]
		self.board.digital[pin].write(state)

	def dark(self):
		self.glow("red",False)
		self.glow("green",False)
		self.glow("blue",False)


	def beep(self,milliseconds=1000):
		pin=self.beeppin

		print ("beep "+ str(milliseconds))

		state=True
		state ^= self.activeLow
		self.board.digital[pin].write(state)

		time.sleep(milliseconds/1000)

		state=False
		state ^= self.activeLow
		self.board.digital[pin].write(state)






if __name__ == "__main__":

	arduino = device(9,10,11,12,activeLow=True)
	arduino.dark()
	
	import sys

	cmd = sys.argv[1]

	if cmd=="led":
		color = sys.argv[2]
		state = True if (int(sys.argv[3])) else False
		arduino.glow(color,state)

	elif cmd=="beep":
		ms=int(sys.argv[2])
		arduino.beep(ms)

	elif cmd=="mqtt":
		def on_message(client, userdata, message):
			#print (message.topic,message.payload)
			import json
			try:
				msg = json.loads(message.payload)
			except Exception as e:
				print(e)
				return
				
			print (msg)
			if "beep" in msg:
				arduino.beep(msg['beep'])
			elif "led" in msg:
				for color in msg['led']:
					arduino.glow(color,msg['led'][color])
			
			
		host=sys.argv[2]
		
		import paho.mqtt.client as paho
		client= paho.Client()

		client.on_message=on_message
		
		client.connect(host)
		client.loop_start()

		client.subscribe("notify/annotation")

		while 1:
			time.sleep(1)
