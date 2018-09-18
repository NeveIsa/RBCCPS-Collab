from pub import Pub
from message import Message
from sub import AMQPsub

import json

p=Pub()
Msg=Message()

import sys
if len(sys.argv)>1:
    brightness_val = int(sys.argv[1])
else:
    s=AMQPsub()
    s.subscribe('iiscstreetlight')
    s.consume()
    exit()


m=json.dumps(Msg.pack({'brightness': brightness_val}))
p.publish(m,'iiscstreetlight.configure')


