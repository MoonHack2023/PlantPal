# adc docs https://www.ti.com/lit/ds/symlink/ads1115.pdf
import smbus2 
import time

bus = smbus2.SMBus(1)
# DATASHEET COEFFICIENTS:
const_A = -2.2534
const_B = 40.87142
const_C = -68.14970
const_D = 117.16178
const_E = -111.95726
const_F = 58.03388
const_G = -12.55428 

class AIRVELOCITY_SENSOR():
    ADDR = 0x48
    CONVERESION = 0x00  # starts at 0 then contains value of last conversion in 2s complement (16bit)
    CONFIG = 0x01   # change operating modes and status
    LO_THRESH = 0x02  # dont think need these
    HI_THRESH = 0x03 

    def __init__(self, bus):
        self.bus = bus
    
    def conversion(self, val):
        out = abs(const_A*val**6 + const_B*val**5 + const_C*val**4 + const_D*val**3 + const_E*val**2 + const_F*val + const_G)
        print("val " , round(val,3) , "out ", out)
        if out > 3.0:
            out = 3.0
        return round(out,3)
    
    def sign(self,low,high):
        # convert to 16-bit signed value.
        value = (high << 8) | (low ) 
        high_str = format(high, '016b')[2:] 
        if high_str[0] == "1":
            value -= 1 << 16
        return value

    def get_data(self):
        # go from power-down to power up 
        status = 0x8000 # bit 15 needs to be 1
        stat_as_string = format(status, '#016b')[2:] 
        config_code = "1 1 0 0  0 0 1 1  1 0 0 0  0 0 1 1"
        config_code = config_code.replace(" ", "")
        hi_byte = int(config_code[:8],2)
        lo_byte = int(config_code[8:],2)
        self.bus.write_i2c_block_data(self.ADDR, self.CONFIG,[hi_byte, lo_byte])
        time.sleep(0.25)
        reading = self.bus.read_i2c_block_data(self.ADDR, self.CONVERESION,2)
        reading_hi = reading[0]
        reading_lo = reading[1]
        reading_hi_str = format(reading_hi, '#010b')[2:]
        reading_lo_str = format(reading_lo, '#010b')[2:]
        result = reading_hi_str + reading_lo_str
        value = int(result,2)

        signed_value = self.sign(reading_lo,reading_hi)
        voltage = (signed_value*4.096)/((2**15) -1) #  using 16bit adc
        print("DATA AVAILABLE VELOCITY")
        velocity = self.conversion(voltage)
        #print("Velocity = " , velocity , " m/s")
        #print("VOLTAGE  = ", voltage )
        #print("FINAL VAL = " , final)
        return velocity

