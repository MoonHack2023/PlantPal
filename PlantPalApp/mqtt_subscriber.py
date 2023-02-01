import random
from paho.mqtt import client as mqtt_client
import ssl

broker = 'broker.emqx.io'
# broker = 'test.mosquitto.org'
port = 1883 # specific to the broker
topic = "temperature&humidity"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
print(client_id)
username = 'moonhack'
password = 'embbed'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    # client.tls_set(certfile=None,keyfile=None,cert_reqs=ssl.CERT_REQUIRED)
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


if __name__ == '__main__':
    run()
