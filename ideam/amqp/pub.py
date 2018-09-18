import pika

import logging
logging.basicConfig(level=logging.ERROR)

from connect import *

class Pub:
    def __init__(self):

        #credentials = pika.PlainCredentials('guest', 'guest')
        #parameters =  pika.ConnectionParameters('localhost', credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def publish(self,message,exchange,routingKey='#'):
        print('Publishing --> ex: {} | rk: {} | msg: {}'.format(exchange,routingKey,message))
        self.channel.basic_publish(exchange,
                          routingKey,
                          message,
                          pika.BasicProperties(content_type='text/plain',delivery_mode=1))

    def __del__(self):
        self.connection.close()




if __name__=='__main__':
    import time
    from message import Message
    import json

    Msg = Message()
    p = Pub()

    try:
        for _ in range(10):
            count = (_ * 10) % 100
            m=json.dumps(Msg.pack({"helloworld":count}))
            p.publish(m,config['device']['name'] + ".protected")
            #time.sleep(1)


        def handle_mqtt(msg):
            try:
                subtopic = msg.topic.split("/")[-1]
                msg_val = json.loads(msg.payload.decode())[0]
                ideam_msg=Msg.pack({subtopic: msg_val})
                ideam_msg=json.dumps(ideam_msg)
                p.publish(ideam_msg,config['device']['name']+".protected")
            except Exception as e:
                print("Exception in handle_mqtt -> %s" % e)


        from mosquitto import Mosquitto
        mq = Mosquitto()
        mq.registerCallback(handle_mqtt)
        mq.subscribe("sensed/modbus/#")
        mq.loop()

    except KeyboardInterrupt:
        del(p)

