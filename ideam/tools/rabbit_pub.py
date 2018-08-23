import sys
import pika

# Step #1: Connect to RabbitMQ using the default parameters
#parameters = pika.ConnectionParameters()

parameters = pika.URLParameters('amqp://test:test@server:5672/%2F')

connection = pika.BlockingConnection(parameters)


#connection = pika.SelectConnection(parameters, on_connected,)
channel = connection.channel()


msg = str({"brightness":int(sys.argv[1])}).replace("'",'"')

channel.basic_publish('test',
                      '',
                      msg,
                      )
