import paho.mqtt.client as mqtt
from paho.mqtt import client as mqtt_client
import time
import random
import ssl

# broker = "mqtt.eclipseprojects.io" 
broker = "test.mosquitto.org"
port = 8883
client_id = f'python-mqtt-{random.randint(0, 100)}'

# mqtt_client = mqtt.Client(client_id)
# mqtt_client.connect("broker.mqttdashboard.com", port)
# username = 'moon'
# password = 'em'
topic = "IC.embedded/MoonHack/test1"

def on_message(client, userdata, message) :
    print("Received message:{} on topic {}".format(message.payload, message.topic))

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.tls_set(ca_certs="mosquitto.org.crt", certfile="client.crt",keyfile="client.key")
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        f = open("blog/text_files/thsensor.txt", "w")
        f.write(msg.payload.decode())

    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

# client.tls_set(ca_certs="mosquitto.org.crt", certfile="client.crt",keyfile="client.key")

# client.loop_start()
# client.loop_start() 
# print("inside loop")
# client.subscribe("IC.embedded/Moonhack/test1")
# client.on_message = on_message

# time.sleep(5)
# client.loop_stop()
# 

if __name__ == '__main__':
    run()


# import paho.mqtt.client as mqtt
# import time

# def on_message(client, userdata, message):
#     print("Received message: ", str(message.payload.decode("utf-8")))

# mqttBroker = "test.mosquitto.org"
# port = 8884
# client = mqtt.Client("Smartphone")
# client.connect(mqttBroker,port)
# # client.tls_set(ca_certs="mosquitto.org.crt", certfile="client.crt",keyfile="client.key")

# client.subscribe("TEMPERATURE")
# client.on_message = on_message
# time.sleep(1)
# client.loop_forever()