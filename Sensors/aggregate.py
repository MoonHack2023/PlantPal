import time
import smbus2
import socket

from temp_hum_sensor import TEMP_HUM
from co2_sensor import CO2_SENSOR

bus = smbus2.SMBus(1)


TH_SENSOR = TEMP_HUM(bus)
AQ_SENSOR = CO2_SENSOR(bus)
AQ_SENSOR.on_device_start()
AQ_SENSOR.get_mode()
AQ_SENSOR.set_mode(1)
co2 , tvoc = 0,0
while True:
    
    try:
        temperature,humidity = TH_SENSOR.get_data()
        co2, tvoc = AQ_SENSOR.get_data()
        print("TEMP : ", temperature, "HUMID: ", humidity, "co2 :" , co2, "TVOC : ", tvoc)
        data_to_file = str(str(temperature)+"," +str(humidity)+"," +str(tvoc)+"," +str(co2))
        #print(send_data)
        #s.send(send_data.encode())
        text_file = open("temphum.txt","w")  #writes to new temphum.txt stored in pi
        text_file.write(data_to_file)
        #print(add_to_file)
        text_file.close()
        time.sleep(1)
    except:
        print("co2 not ready")
        time.sleep(0.5)
    
    #