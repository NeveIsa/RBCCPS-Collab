import signal,sys,time
import json

def signal_handler(signal, frame):
        print('Exiting gracefully...')
        time.sleep(0.5)
        sys.exit(0)


import logging
import loggingcolormod


### ideam stuff

import ideamclient as ic

helper = ic.Helper()
mqttconf=helper.loadYaml("config/mqttConf")

icdev = ic.device


### mqtt stuff
import paho.mqtt.client as mqtt

import sys
if sys.version_info.major==2:
    import Queue as queue
else:
    import queue



CONF = mqttconf
class Manager(object):
    def __init__(self,deviceName):


        self.deviceName=deviceName
        self.IncomingSubtopics=[]

        # THREAD SAFE QUEUE TO BUFFER INCOMMING MESSAGES
        self.msgQueue = queue.Queue()

        # OUTGOING TOPICS
        self.sensorReportTopic = "{}/{}".format(CONF["FORWARD_DOMAINS"]["SENSE"] , self.deviceName)
        self.logTopic = "{}/{}".format(CONF["FORWARD_DOMAINS"]["LOG"] ,self.deviceName)
        self.gwManagerTopic = "{}/{}".format(CONF["FORWARD_DOMAINS"]["MANAGEMENT"] , self.deviceName)

        # INCOMING TOPICS
        self.actionListeningTopic = "{}/{}".format(CONF["INCOMING_DOMAINS"]["ACTION"] , self.deviceName)
        self.managerListeningTopic = "{}/{}".format(CONF["INCOMING_DOMAINS"]["MANAGEMENT"] , self.deviceName)

    def on_connect(self,client,userdata, flags, rc):
        # The callback for when the client receives a CONNACK response from the server.
        if rc==0:
            logging.warning("In on_connect -> Connected to MQTT Broker @ %s:%s with result code " % (CONF["MQTT_HOST"], CONF["MQTT_PORT"]) + str(rc)  )
        else:
            logging.error("In on_connect -> Failed to connect to MQTT Broker @ %s:%s with result code " % (CONF["MQTT_HOST"], CONF["MQTT_PORT"]) + str(rc)  )
            import sys
            sys.exit(1)

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        '''
            for key in CONF["INCOMING_DOMAINS"]:
            topic=CONF["INCOMING_DOMAINS"][key]
            client.subscribe(topic)
        '''
        # Note that 'client' here is passed in the callback(check parameters passed to this method) and is different from 'self.client'
        # self.sensorReportTopic += "/#"
        logging.warning("In on_connect -> Re-subscribing to sensorReport topic: %s" % self.sensorReportTopic+"/#")
        client.subscribe(self.sensorReportTopic + "/#")

        
        """for topic in self.IncomingSubtopics: 
            logging.warning("In on_connect -> Re-subscribing to %s" % topic)
            realtopic = "{}/{}".format(self.actionListeningTopic,topic)
            client.subscribe(realtopic)"""


    def on_message(self,client, userdata, msg):
        # The callback for when a PUBLISH message is received from the server.
        logging.warning("In on_message -> Topic: %s | Message: %s" % (msg.topic,str(msg.payload)[:30]) )
        
        #Get subtopic
        subtopic = msg.topic.replace(self.sensorReportTopic+"/","")
        msg={"subtopic":subtopic,"message":msg.payload}
        self.msgQueue.put(msg)

    def setup(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        try:
            
            self.client.connect(CONF["MQTT_HOST"], CONF["MQTT_PORT"], 60)
            logging.warning("In setup(services.py) --> Connecting to MQTT Broker @ %s:%s" % (CONF["MQTT_HOST"], CONF["MQTT_PORT"]))
        except Exception as e:
            logging.error("In setup(services.py) --> Couldn't connect to MQTT Broker.")
            sys.exit(1)

    def startListening(self):
        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.

        # NOTE: calling loop_start starts a new thread and handles callbacks using 
        # that thread and hence is concurrent

        logging.warning("In startListening -> Starting MQTT Loop")
        self.client.loop_start()

    def stopListening(self):
        """ STOP MQTT LOOP """
        logging.warning("In stopListening -> Stopping MQTT Loop")
        self.client.loop_stop()

    def messageInwaiting(self):
        return not self.msgQueue.empty()

    def messageGet(self):
        return self.msgQueue.get()



if __name__ == "__main__":
    manager = Manager("modbus")
    manager.setup()
    manager.startListening()
    
    import message
    m = message.Message()
    
    while True:
        if manager.messageInwaiting():
            mqttmsg=manager.messageGet()
            logging.info(mqttmsg)
            
            key = mqttmsg["subtopic"].split("/")[-1]
            message = json.loads(mqttmsg["message"].decode("utf"))[0]

            msg=m.create({key:message})
            logging.error("Received: %s" % msg)
            try:
                icdev.publish("cityssl.private",json.dumps(msg))
            except Exception as e:
                logging.error("Failed to publish to IDEAM: %s" % e)

            import requests
            requests.get("https://dweet.io/dweet/for/cityssl",params=msg)

