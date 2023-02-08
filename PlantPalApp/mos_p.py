import paho.mqtt.client as mqtt
import time
import random
# from blog.models import Device

client_id = f'python-mqtt-{random.randint(0, 100)}'
client = mqtt.Client(client_id)
# broker = "mqtt.eclipseprojects.io" 
broker = "test.mosquitto.org"
client.tls_set(ca_certs="mosquitto.org.crt", certfile="client.crt",keyfile="client.key")

client.connect(broker,port=8884)

while True:
    # f = open("score.txt","r")
    # string = f.readline()
    string = "hi"
    # print(Device.objects.all())
    MSG_INFO = client.publish("IC.embedded/MoonHack/test1", string)
    print(string)
    mqtt.error_string(MSG_INFO.rc)
    time.sleep(5)