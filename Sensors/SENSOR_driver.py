import time
import smbus2
import socket
import struct
import RPi.GPIO as GPIO
from SENSOR_temp_hum import TEMP_HUM_SENSOR    # importing from my-own coded libraries
from SENSOR_co2 import CO2_SENSOR
from SENSOR_light import SPECTRAL_LIGHT_SENSOR
from SENSOR_air_velocity import AIRVELOCITY_SENSOR

bus = smbus2.SMBus(1)

def intialise_sensors(bus):
    TH_SENSOR = TEMP_HUM_SENSOR(bus)
    AQ_SENSOR = CO2_SENSOR(bus)
    SL_SENSOR = SPECTRAL_LIGHT_SENSOR(bus)
    AV_SENSOR = AIRVELOCITY_SENSOR(bus)
    return TH_SENSOR,AQ_SENSOR,SL_SENSOR,AV_SENSOR

def setup_sensors(temp_sensor,light_sensor,air_quality_sensor,air_velocity_sensor):
    setup_successful = False
    try:
        #get temp and hum to setup the co2 sensor
        temp,hum = temp_sensor.get_data()
        #co2 sensor setup
        air_quality_sensor.on_device_start()
        air_quality_sensor.get_mode()
        air_quality_sensor.set_mode(1)
        air_quality_sensor.set_conditions(temp,hum)
        #light sensor setup
        light_sensor.reset()
        light_sensor.set_mode()      
        setup_successful = True
    except:
        setup_successful = False
    return setup_successful,temp_sensor,light_sensor,air_quality_sensor,air_velocity_sensor



def get_all_data(temp_sensor,light_sensor,air_quality_sensor,air_velocity_sensor):
    data_valid = False
    co2,tvoc,temperature,humidity,light_data,air_velocity = 0,0,0,0,0,0
    try:
        co2,tvoc = air_quality_sensor.get_data()
        temperature,humidity = temp_sensor.get_data()
        light_data = light_sensor.get_data()
        air_velocity = air_velocity_sensor.get_data()
        data_valid = True
    except:
        data_valid = False
    return data_valid,co2,tvoc,temperature,humidity,light_data,air_velocity
        
def prepare_data(co2,tvoc,temperature,humidity,light_data,air_velocity):
    avg_light = round(sum(light_data)/len(light_data),3)
    data = [temperature,humidity,tvoc,co2,light_data,avg_light,air_velocity]
    data_as_string = ""
    for element in data:
        if type(element) == list: # light data is a list 
            for colour in element:
                data_as_string = data_as_string + str(colour) + ","
        else:
            data_as_string = str(element) + ","
    data_as_string += "HACK1"
    #formatted datafile to send
    text_file = open("temphum.txt","w")
    text_file.write(data_as_string)
    text_file.close()
    return data

def print_data_terminal(co2,tvoc,temperature,humidity,light_data,air_velocity,avg_light):
    print("TEMP: ", temperature, '\n', "HUMID: ", humidity, '\n',  "CO2:" , co2, '\n',  "TVOC: ", tvoc, '\n', 
              "VIOLET: ", light_data[0], '\n',  "BLUE: ", light_data[1], '\n',  "GREEN:" , light_data[2], '\n',
                "YELLOW: ", light_data[3], '\n', "ORANGE:" , light_data[4], '\n',  "RED: ", light_data[5], '\n',
                 "AVG_LIGHT: ", avg_light ,'\n', "AIR_VELOCITY: ", air_velocity ,'\n' 
        )

#main loop
temp_sensor,air_quality_sensor,light_sensor,air_velocity_sensor =  intialise_sensors(bus)
setup_successful = False
while setup_successful != True:
    setup_successful, temp_sensor,light_sensor,air_quality_sensor,air_velocity_sensor =  setup_sensors(temp_sensor,light_sensor,air_quality_sensor,air_velocity_sensor)
    if setup_successful == True:
        print("SETUP WAS SUCCESSFUL")
        break
    else:
        print("SETUP NOT SUCCESSFUL")
        time.sleep(5)
#data loop
data_valid = False
print_to_terminal = True
while True:
    data_valid,co2,tvoc,temperature,humidity,light_data,air_velocity = get_all_data(temp_sensor,light_sensor,air_quality_sensor,air_velocity_sensor)
    if data_valid == True:
        data = prepare_data(co2,tvoc,temperature,humidity,light_data,air_velocity)
        if print_to_terminal:
            print_data_terminal(co2,tvoc,temperature,humidity,light_data,air_velocity,data[5])
    else:
        print("DATA NOT AVAILABLE")
        time.sleep(0.5)








# TH_SENSOR = TEMP_HUM_SENSOR(bus)
# AQ_SENSOR = CO2_SENSOR(bus)
# AQ_SENSOR.on_device_start()
# AQ_SENSOR.get_mode()
# AQ_SENSOR.set_mode(1)
# SL_SENSOR = SPECTRAL_LIGHT_SENSOR(bus)
# SL_SENSOR.reset()
# SL_SENSOR.set_mode()
# AV_SENSOR = AIRVELOCITY_SENSOR(bus)

# optimum = True
# co2 , tvoc = 0,0
# while True:
    
#     try:
#         # if optimum:
#         #     GPIO.output(27,GPIO.HIGH) # red
#         # else:
#         #     GPIO.output(23,GPIO.HIGH) # red
#         co2, tvoc = AQ_SENSOR.get_data()
#         temperature,humidity = TH_SENSOR.get_data()
#         light_string,light_data = SL_SENSOR.get_data()
#         air_velocity = AV_SENSOR.get_data()
#         avg_light = round(sum(light_data)/len(light_data),3)

#         print("TEMP: ", temperature, '\n', "HUMID: ", humidity, '\n',  "CO2:" , co2, '\n',  "TVOC: ", tvoc, '\n', 
#               "VIOLET: ", light_data[0], '\n',  "BLUE: ", light_data[1], '\n',  "GREEN:" , light_data[2], '\n',  "YELLOW: ", light_data[3], '\n', 
#               "ORANGE:" , light_data[4], '\n',  "RED: ", light_data[5], '\n', "AVG_LIGHT: ", avg_light ,'\n', "AIR_VELOCITY: ", air_velocity ,'\n' 
#         )
    
#         data_to_file = str(str(temperature)+"," +str(humidity)+"," +str(tvoc)+"," +str(co2))
#         data_to_file += light_string
#         data_to_file = data_to_file +  "," +str(avg_light) + str(air_velocity)
#         data_to_file += ",HACK1"
#         # print("DATA_TO_FILE ", data_to_file)
#         # #print(send_data)
#         # #s.send(send_data.encode())s
#         text_file = open("temphum.txt","w")  #writes to new temphum.txt stored in pi
#         text_file.write(data_to_file)
#         #print(add_to_file)
#         text_file.close()

#         # leds
#         if co2 > 450:
#             optimum = False
            
#         else:
#             optimum = True

#         time.sleep(0.1)



#     except:
#         print("DATA NOT READY")
#         time.sleep(0.5)
    
    
#     # GPIO.output(27,GPIO.LOW)
#     # GPIO.output(23,GPIO.LOW)
#     # GPIO.output(17,GPIO.LOW)
