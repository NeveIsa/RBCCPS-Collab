import logging
import loggingcolormod
import json
import paho.mqtt.client as mqtt

import pika



client =mqtt.Client()
client.connect("localhost", 1883, 60)
client.loop_start()

def decode_msg_and_publish(msg):
    try:
        msg = msg.decode("utf")
        msg=json.loads(msg)
        if "brightness" in msg:
            topic="deviceAction/modbus/brightness_percent"

        client.publish(topic,str([msg["brightness"]]))

    except Exception as e:
        logging.error("In decode_msg_and_publish -> Exception: %s" % e)

    


# Create a global channel variable to hold our channel object in
channel = None

# Step #2
def on_connected(connection):
    """Called when we are fully connected to RabbitMQ"""
    # Open a channel
    connection.channel(on_channel_open)

# Step #3
def on_channel_open(new_channel):
    """Called when our channel has opened"""
    global channel
    channel = new_channel
    channel.queue_declare(queue="test", durable=True, exclusive=False, auto_delete=False, callback=on_queue_declared)

# Step #4
def on_queue_declared(frame):
    """Called when RabbitMQ has told us our Queue has been declared, frame is the response from RabbitMQ"""
    channel.basic_consume(handle_delivery, queue='test',no_ack=True)

# Step #5
def handle_delivery(channel, method, header, body):
    """Called when we receive a message from RabbitMQ"""
    logging.info("In handle_delivery -> Received: %s" % body)
    decode_msg_and_publish(body)


# Step #1: Connect to RabbitMQ using the default parameters
#parameters = pika.ConnectionParameters()

credentials = pika.PlainCredentials('test', 'test')
parameters = pika.ConnectionParameters('server',
                                       5672,'/',
                                       credentials)

connection = pika.SelectConnection(parameters, on_connected,)

try:
    # Loop so we can communicate with RabbitMQ
    connection.ioloop.start()
except KeyboardInterrupt:
    # Gracefully close the connection
    connection.close()
    # Loop until we're fully closed, will stop on its own
    connection.ioloop.start()
    client.loop_stop()