
import time
import smbus2
import socket
print("hello, inside pi")
si7021_ADD =  0x40 #Add the I2C bus address for the sensor here
si7021_READ_TEMPERATURE = 0xF3 #Add the command to read temperature here
si7021_READ_HUMIDITY = 0xF5 #Add the command to read temperature here
# s = socket.socket()
# s.connect(('',12008)) 
bus = smbus2.SMBus(1)
for i in range(10000):

    #Set up a write transaction that sends the command to measure temperature
    cmd_meas_temp = smbus2.i2c_msg.write(si7021_ADD,[si7021_READ_TEMPERATURE])

    #Set up a write transaction that sends the command to measure temperature
    cmd_meas_hum = smbus2.i2c_msg.write(si7021_ADD,[si7021_READ_HUMIDITY])

    #Set up a read transaction that reads two bytes of data
    read_result_temp = smbus2.i2c_msg.read(si7021_ADD,2)

    #Set up a read transaction that reads two bytes of data
    read_result_hum = smbus2.i2c_msg.read(si7021_ADD,2)

    #Execute the two transactions with a small delay between them
    bus.i2c_rdwr(cmd_meas_temp)
    time.sleep(0.1)
    bus.i2c_rdwr(read_result_temp)
    time.sleep(0.1)
    bus.i2c_rdwr(cmd_meas_hum)
    time.sleep(0.1)
    bus.i2c_rdwr(read_result_hum)

    #convert the result to an int

    time.sleep(1)
    temperature = int.from_bytes(read_result_temp.buf[0]+read_result_temp.buf[1],'big')
    hum = int.from_bytes(read_result_hum.buf[0]+read_result_hum.buf[1],'big')
    final_temp = ((175.72*temperature)/65536) -46.85  #tempeature conversion
    final_temp = round(final_temp,3)

    final_hum = ((125*hum)/65536) -6  #humidity conversion
    final_hum = round(final_hum,3)

    data_to_file = str(str(final_temp)+"," +str(final_hum))
    #print(send_data)
    #s.send(send_data.encode())
    text_file = open("temphum.txt","w")  #writes to new temphum.txt stored in pi
    text_file.write(data_to_file)
    #print(add_to_file)
    text_file.close()
    print("Temp: ", final_temp, "C" , "Hum:", final_hum, "%")

# s.close()