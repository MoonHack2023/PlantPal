import time
import smbus2
import socket

class CO2_SENSOR():
    STATUS = 0x00  # read status reg
    MEAS_MODE = 0x01 # read/write measurement mode
    ALG_RESULT_DATA = 0x02 # read algo result
    RAW_DATA = 0x03
    HW_ID = 0x20
    ENV_DATA = 0x05  # write env condition
    ERROR = 0xE0  # read error code
    SW_RESET = 0xFF  # write to reset device to boot up mode
    APP_START = 0xF4  # write to start application
    APP_VERIFY = 0x0E  # write ?
    ERROR = 0x0E  # read error code
    ADDR = 0x5A # check using i2c detect

    def __init__(self, bus):
        self.bus = bus
        self.reset()
        self.status_at_start = self.get_status()
        self.fw_mode = int(self.status_at_start[0])  # firmware mode
        print("FW_MODE = " , self.fw_mode)
        


    def on_device_start(self):
        if self.fw_mode != 0:
            self.reset()
            status = self.get_status()
            time.sleep(0.1)
            FW_MODE = int(status[0])
            print("FW_MODE = " , FW_MODE)
        elif self.fw_mode == 0: 
            print("Transfer from boot to application")
            self.start()
            time.sleep(0.5)
            status = self.get_status()


    def get_status(self):
        status = self.bus.read_byte_data(self.ADDR,self.STATUS)
        status_return_byte = format(status, '#010b')[2:]  # converts to 8 bit string e.g. 01001101
        print("STATUS " , status ,status_return_byte)
        time.sleep(0.1)
        return status_return_byte

    def get_mode(self):
        mode = self.bus.read_byte_data(self.ADDR,self.MEAS_MODE)
        mode_return_byte = format(mode, '#010b')[2:]
        print("MODE " , mode, mode_return_byte)
        time.sleep(0.1)
        return mode_return_byte

    def get_error(self):
        error = self.bus.read_byte_data(self.ADDR,self.ERROR) #returns decimal number
        error_return_byte = format(error, '#010b')[2:]
        print("ERROR " , error, error_return_byte)
        time.sleep(0.1)
        return error_return_byte
    
    def start(self):
        print("STARTING APP MODE")
        self.bus.write_i2c_block_data(self.ADDR, self.APP_START, [])
        time.sleep(0.1)

    def reset(self):
        print("RESETTING SENSOR")
        self.bus.write_i2c_block_data(self.ADDR, self.SW_RESET, [0x11, 0xE5, 0x72, 0x8A])  # these 4 bytes trigger reset and reboot   
        time.sleep(0.1)

    def set_mode(self,nextmode=1):    #nextmode=1 sets to mode 0x01 (sample every second)
        print("SETTING MEASURE MODE")
        MODE_CODE = "{0:03b}".format(nextmode)
        write_data = int(f"0{MODE_CODE}0000",2)
        self.bus.write_byte_data(self.ADDR, self.MEAS_MODE, write_data)
        time.sleep(1)
    

    def get_data(self):
        status = self.get_status()
        time.sleep(1)
        data_av = status[4]   # bit that tells if new data is ready
        if data_av == "1":
            print("DATA AVAILABILE")
            data = self.bus.read_i2c_block_data(self.ADDR, self.ALG_RESULT_DATA, 8)
            co2 = data[0:2]   # first 2 bytes give co2
            tvoc = data[2:4]  # second 2 bytes give tvoc
            co2_int = int.from_bytes(bytes(co2), 'big')
            tvoc_int = int.from_bytes(bytes(tvoc), 'big')
            print("CO2 ", co2_int ," ppm , TVOC ",tvoc_int , " ppb")
            return co2_int, tvoc_int
        elif status == "00010001":
            
            self.get_error()
            print("RESETTING........................")
            self.reset()
            time.sleep(5)
            self.set_mode(1)
        else:
            time.sleep(0.3)









