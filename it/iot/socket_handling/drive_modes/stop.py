import paho.mqtt.client as mqtt
def on_connect(client, obj, flags, rc):
    print("Connected with Result Code: "+str(rc))

def on_publish(client, obj, mid):
    print("Publish mesage > mid: "+str(mid))

if __name__ == "__main__":

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.connect("10.99.90.32", 1883, 60)

    client.publish("emb/iot/autocar", '{"device_id":"AutoCar", "command": "stop", "speed":30}')
