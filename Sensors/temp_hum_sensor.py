import time
import smbus2
import socket

class TEMP_HUM():
    si7021_ADD =  0x40 
    si7021_READ_TEMPERATURE = 0xF3 #command to read temperature here
    si7021_READ_HUMIDITY = 0xF5 #command to read humidity here

    def __init__(self, bus):
        self.bus = bus
    
    def convert_to_temp(self,temp_code):
        temperature = int.from_bytes(temp_code.buf[0]+temp_code.buf[1],'big')
        final_temp = ((175.72*temperature)/65536) -46.85  #tempeature conversion
        final_temp = round(final_temp,3)
        return final_temp

    def convert_to_hum(self,hum_code):
        humidity = int.from_bytes(hum_code.buf[0]+hum_code.buf[1],'big')
        final_hum = ((175.72*humidity)/65536) -46.85  #tempeature conversion
        final_hum= round(final_hum,3)
        return final_hum

    def get_temp(self):
        #Set up a write transaction that sends the command to measure temperature
        cmd_meas_temp = smbus2.i2c_msg.write(self.si7021_ADD,[self.si7021_READ_TEMPERATURE])
        #Set up a read transaction that reads two bytes of data
        read_result_temp = smbus2.i2c_msg.read(self.si7021_ADD,2)
        #execute transactions
        self.bus.i2c_rdwr(cmd_meas_temp)
        time.sleep(0.1)
        self.bus.i2c_rdwr(read_result_temp)
        return self.convert_to_temp(read_result_temp)

    def get_hum(self):
        #Set up a write transaction that sends the command to measure humidity
        cmd_meas_hum = smbus2.i2c_msg.write(self.si7021_ADD,[self.si7021_READ_HUMIDITY])
        #Set up a read transaction that reads two bytes of data
        read_result_hum = smbus2.i2c_msg.read(self.si7021_ADD,2)
        #execute transactions
        self.bus.i2c_rdwr(cmd_meas_hum)
        time.sleep(0.1)
        self.bus.i2c_rdwr(read_result_hum)
        return self.convert_to_hum(read_result_hum)


    def get_data(self):
        temperature = self.get_temp()
        humidity = self.get_hum()
        # print("Temp: ", temperature, "C" , "Hum:", humidity, "%")
        time.sleep(0.5)
        return temperature, humidity







