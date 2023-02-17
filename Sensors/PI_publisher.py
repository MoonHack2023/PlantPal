import paho.mqtt.client as mqtt
import time
import random

client_id = f'python-mqtt-{random.randint(0, 100)}'
client = mqtt.Client(client_id)
# broker = "mqtt.eclipseprojects.io" 
broker = "test.mosquitto.org"
#client.tls_set(ca_certs="mosquitto.org.crt", certfile="client.crt",keyfile="client.key")

client.connect(broker,port=1883)

while True:
    f = open("temphum.txt","r")
    string = f.readline()
    MSG_INFO = client.publish("IC.embedded/MoonHack/test1", string)
    print(string)
    mqtt.error_string(MSG_INFO.rc)
    time.sleep(2)

# import paho.mqtt.client as mqtt
# from random import randrange, uniform
# import time

# mqttBroker = "test.mosquitto.org"
# port = 8884
# client = mqtt.Client("Temperature_Inside")
# client.connect(mqttBroker,port)
# # client.tls_set(ca_certs="mosquitto.org.crt", certfile="client.crt",keyfile="client.key")
# client.tls_set(ca_certs="broker.emqx.io-ca.crt", certfile="client.crt",keyfile="client.key")

# while True:
#     randNumber = uniform(20.0, 21.0)
#     client.publish("TEMPERATURE", randNumber)
#     print("Just published " + str(randNumber) + " to Topic TEMPERATURE")
#     time.sleep(1)