import time
import smbus2
import socket
import struct

# SENSOR DOCUMENTATION
# https://www.mouser.com/datasheet/2/588/AS7262_DS000486_2-00-1082195.pdf

class SPECTRAL_LIGHT_SENSOR():
    STATUS = 0x00  # read status reg
    WRITE  = 0x01  # for writing
    READ   = 0x02  # for reading
    TX_VALID = 0b00000010  # bit string
    RX_VALID = 0b00000001 # bit string
    ADDR = 0x49 # i2c address of sensor
    CONTROL = 0x04
    INT_TIME = 0x05
    COLOURS = [["Violet",0],["Blue",0],["Green",0],["Yellow",0],["Orange",0],["Red",0]] 

    def __init__(self,bus):
        self.bus = bus
        self.C_REGS =  {"Violet": [0x17,0x16,0x15,0x14],
                        "Blue": [0x1B,0x1A,0x19,0x18],
                        "Green": [0x1F,0x1E,0x1D,0x1C],
                        "Yellow": [0x23,0x22,0x21,0x20],
                        "Orange": [0x27,0x26,0x25,0x24],
                        "Red": [0x2B,0x2A,0x29,0x28],
                }
        self.C_DATA = {"Violet": [0 for i in range(4)],
                        "Blue": [0 for i in range(4)],
                        "Green":[0 for i in range(4)],
                        "Yellow": [0 for i in range(4)],
                        "Orange": [0 for i in range(4)],
                        "Red": [0 for i in range(4)],
                }
        self.output = [0,0,0,0,0,0]


    def read(self,read_reg_addr):  # as hex
        # pseudocode found in datasheet
        while True:
            status = self.bus.read_byte_data(self.ADDR, self.STATUS)
            if (status & self.TX_VALID) == 0:
                break
            else:
                pass
        self.bus.write_byte_data(self.ADDR, self.WRITE, read_reg_addr)  
        time.sleep(0.1)
        while True:
            status = self.bus.read_byte_data(self.ADDR, self.STATUS)
            if (status & self.RX_VALID) == 0x01:
                break
        data = self.bus.read_byte_data(self.ADDR, self.READ)
        #print("READ DATA ", data)
        return data

    def write(self,write_reg_addr,data_to_write):
        # pseudocode found in datasheet
        while True:
            status = self.bus.read_byte_data(self.ADDR, self.STATUS)
            if (status & self.TX_VALID) == 0:
                break
        write_reg_addr = (write_reg_addr | 0x80) # datasheet says to set bit 7 
        self.bus.write_byte_data(self.ADDR, self.WRITE, write_reg_addr) 
        time.sleep(0.1)
        while True:
            status = self.bus.read_byte_data(self.ADDR, self.STATUS)
            if (status & self.TX_VALID) == 0:
                break
        self.bus.write_byte_data(self.ADDR, self.WRITE, data_to_write)

    def reset(self):
        print("RESETTING LIGHT SENSOR")
        SOFT_RESET = 0b10000000
        self.write(self.CONTROL,SOFT_RESET)
        time.sleep(1)

    def set_int_time(self,i_time=120):
        # for time being using int_time 120
        # increasing int_time means readings take longer
        self.write(self.INT_TIME,i_time)
    

    def set_mode(self,mode=2):
        # mode 2 will read all colours, mode 0 and mode 1 read only some colours,
        # see docs for which colours...
        status = self.get_status()
        new_status_with_mode = status[:4] + "10" + status[-2:]  # using bin10 =2 
        #print("new mode , ", new_status_with_mode)
        self.write(self.CONTROL,int(new_status_with_mode,2))
        status = self.get_status()
        #print("new status ", status)

    def get_status(self):
        status = self.read(self.CONTROL)
        status_return_byte = format(status, '#010b')[2:]  # converts to 8 bit string e.g. 01001101
        #print("STATUS " , status, status_return_byte)
        return status_return_byte

    
    def get_data(self):
        status = self.read(self.CONTROL)
        status_return_byte = format(status, '#010b')[2:]
        time.sleep(0.3)
        data_av = status_return_byte[6]   # bit  1 that tells if new data is ready
        #print("status in get_data", status_return_byte)
        if data_av == "1":
            print("DATA AVAILABILE LIGHT SENSOR")
            # get calibrated data
            for key in self.C_REGS.keys() & self.C_DATA.keys():
                index = 0
                for register,data in zip(self.C_REGS[key],self.C_DATA[key]):
                    data = self.read(register)
                    self.C_DATA[key][index] = data
                    index +=1
            #print(self.C_DATA)
            return self.conversion()
        else:
            print("light_not_ready")
            time.sleep(0.3)
    
    def conversion(self):
        #print("IN CONVERSION")
        #print(self.C_DATA) #prints
        #print("COLOURS >L " , self.COLOURS[0][1])
        for index,key in enumerate(self.C_DATA.keys()):
            data_as_byte_array = bytearray(self.C_DATA[key])
            output_data = struct.unpack("f",data_as_byte_array)[0]
            self.output[index] = round(float(output_data),3)
        #self.print_output()
        # print("SELF OUTPUT ", self.output)
        return self.return_data_as_string()
        # return self.output

    def return_data_as_string(self):
        #print("IN STRING")
        string_for_text_file = ""
        for color in self.output:
            string_for_text_file+= ","
            string_for_text_file+= str(color)
        #print("IN LIGHT", string_for_text_file)
        return self.output



    def print_output(self):
        print("_________________")
        for colour,data in zip(self.COLOURS,self.output):
            print(colour[0], data)