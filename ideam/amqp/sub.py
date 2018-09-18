#!/usr/bin/env python
import pika
import datetime

from connect import *


class AMQPsub:
    #self.cb = lambda body: print(body)

    def __init__(self):
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.cb = lambda msg: print ("[x] Rcvd: {}".format(msg)) 

    def registerCallback(self,_cb):
        self.cb = lambda msg: _cb(msg)

    def callback(self,ch, method, properties, body):
        print('[x] %s --> %r' % (datetime.datetime.now().isoformat(),body))
        self.cb(body.decode())

    def subscribe(self,_queue):
        self.channel.basic_consume(self.callback,
                      #queue='iiscstreetlight',
                      queue=_queue,
                      no_ack=True)

    def consume(self):
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.connection.close()





if __name__=='__main__':

    import json
    
    from message import Message
    Msg = Message()
    
    from mosquitto import Mosquitto
    mqtt = Mosquitto()

    
    amqp = AMQPsub()
    
    amqp.registerCallback(lambda data: mqtt.publish('deviceAction/modbus/brightness_percent', data))
    amqp.subscribe(config['device']['name'])

    amqp.consume()
