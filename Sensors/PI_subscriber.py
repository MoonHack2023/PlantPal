import paho.mqtt.client as mqtt
from paho.mqtt import client as mqtt_client
import time
import random
import ssl
import RPi.GPIO as GPIO

# broker = "mqtt.eclipseprojects.io" 
broker = "test.mosquitto.org"
port = 1883
client_id = f'python-mqtt-{random.randint(0, 100)}'


topic = "IC.embedded/MoonHack/webtopi"

RED_LED = 23
GREEN_LED = 27
YELLOW_LED = 18
FAN_PIN = 10


def setup_GPIO_pins():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(RED_LED,GPIO.OUT)    #red led
    GPIO.setup(GREEN_LED,GPIO.OUT)  #green led
    GPIO.setup(YELLOW_LED,GPIO.OUT) #yellow led
    GPIO.setup(FAN_PIN,GPIO.OUT)    #fan pin

def turn_on_led(color):
    #assert color in ["RED","GREEN", "YELLOW"], f"{color} not valid colour"
    if color == "RED":
        GPIO.output(RED_LED,GPIO.HIGH) # red on
        GPIO.output(GREEN_LED,GPIO.LOW)
        GPIO.output(YELLOW_LED,GPIO.LOW)
        time.sleep(0.1)
    elif color == "GREEN":
        GPIO.output(GREEN_LED,GPIO.HIGH) # green on
        GPIO.output(RED_LED,GPIO.LOW)
        GPIO.output(YELLOW_LED,GPIO.LOW)
        time.sleep(0.1)
    elif color == "YELLOW":
        GPIO.output(YELLOW_LED,GPIO.HIGH) # yellow on
        GPIO.output(RED_LED,GPIO.LOW)
        GPIO.output(GREEN_LED,GPIO.LOW)
        time.sleep(0.1)
    
def turn_on_fan():
    GPIO.output(FAN_PIN, True)
    

def turn_off_fan():
    GPIO.output(FAN_PIN, False)
    



def on_message(client, userdata, message) :
    print("Received message:{} on topic {}".format(message.payload, message.topic))

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.tls_set(ca_certs="mosquitto.org.crt", certfile="client.crt",keyfile="client.key")
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        message = msg.payload.decode()
        #print(message)
        print(f"Received `{message}` from `{msg.topic}` topic")
        score = float(message.split(', ')[0])
        fan_var = message[-2:]
        print("FAN_VAR = " , fan_var)
        print("SCORE = " , score)
        if score >90: # green led
            print("GREEN")
            turn_on_led("GREEN")
        elif score < 50:
            print("RED")
            turn_on_led("RED")
        else:
            print("YELLOW")
            turn_on_led("YELLOW")

        if fan_var == "Of":
            print("FAN OFF")
            turn_off_fan()
        elif fan_var == "On":
            print("FAN ON")
            turn_on_fan()


    client.subscribe(topic)
    client.on_message = on_message

def run():
    setup_GPIO_pins()
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()