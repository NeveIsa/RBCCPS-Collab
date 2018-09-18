
import paho.mqtt.client as pahomqtt
import datetime

class Mosquitto:
    def __init__(self,host='localhost',port=1883):
        self.mqttc = pahomqtt.Client()
        #self.pubTopic = pubTopic
        #self.subTopic = subTopic
        self.mqttc.connect(host,port)
        self.cb = lambda x: print(x.payload) 
        self.mqttc.on_message = self.callback

    def publish(self,topic,msg):
        self.mqttc.publish(topic,msg)
    
    def registerCallback(self,_cb=None):
        self.cb = _cb

    def callback(self,client,userdata,message):
        print('Recvd MQTT Message -> {} | @ {}'.format(datetime.datetime.now().isoformat(),message.topic))
        self.cb(message)

    def subscribe(self,topic):
        self.mqttc.subscribe(topic)

    def loop(self):
        try:
            self.mqttc.loop_start()
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.mqttc.loop_stop()


if __name__ == "__main__":

    m = Mosquitto()
    import sys
    topic = sys.argv[1]
    print("Subscribed to %s" % topic)
    m.subscribe(topic)
    m.loop()



