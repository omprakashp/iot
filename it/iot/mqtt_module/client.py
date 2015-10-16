import paho.mqtt.client as mqtt


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, obj, flags, rc):
    print("Connected with Result Code: "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

# The callback for when a PUBLISH message is received from the server.
def on_message(client, obj, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

def on_publish(client, obj, mid):
    print("Publish mesage > mid: "+str(mid))

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(client, obj, level, string):
    print(string)

print "client created"
client = mqtt.Client()
client.on_message = on_message
print "assigned on message"
client.on_connect = on_connect
print "assigned on connect"
client.on_publish = on_publish
print "assigned on publish"
client.on_subscribe = on_subscribe
print "assigned on subscribe"
client.connect("10.99.90.32", 1883, 60)
print "client connected!!!!!!!!!!!!!!!"
client.subscribe("emb/iot/gateway/")
print "Subscribed to iot server commands"



#LOGIC FOR CONTINUOS PUBLISHING
import threading
import time
from random import randint 
def publish_messages():
    while True:
        time.sleep(5)
        client.publish("emb/iot/autocar", '{"device_id":"AutoCar", "command": "reverse", "speed":30}')

t = threading.Thread(name='publish_messages', target=publish_messages)
t.start()




print "LOOP FOREVER"
client.loop_forever()
