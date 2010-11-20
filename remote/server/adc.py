#!/usr/bin/env python

import struct
import fcntl

class Adc:
    VALID_PINS = [2,3,4,5,6,7]
    # TWL4030_MADC_IOC_MAGIC '`' # or ord('`') = 96
    # TWL4030_MADC_IOCX_ADC_RAW_READ _IO(TWL4030_MADC_IOC_MAGIC, 0)
    # op = group << (4*2) | type
    #raw_read = 96 << (4*2) | 0
    TWL_RAW_READ = 24576
    DEVICE = '/dev/twl4030-madc'
    # 2.5 / 1024.0 = 0.00244140625
    SCALE = 0.00244140625
    def __init__(self, pin=3, average=1):
        self.dev = open(self.DEVICE, 'rw')
        # if not pin in self.VALID_PINS:
        #     raise ValueError("Adc: invalid pin: "+str(pin)+" not in "+str(self.VALID_PINS))
        # if not average in (0,1):
        #     raise ValueError("Adc: average("+str(average)+") must be 0 or 1")
        self.set_pin(pin,average)
        # disable carkit and allow madc inputs
        #i2cset -f -y 1 0x48 0xbb 0x08
        # setup madc clock
        #i2cset -f -y 0x49 0x91 0x90
        # enable sw1 triggering
        #i2cset -f -y 0x4a 0x62 0x0d
        # turn on power to madc
        #i2cset -f -y 0x4a 0x00 0x01
        # select adc pin 4
        #i2cset -f -y 0x4a 0x06 0x10
        #i2cset -f -y 0x4a 0x07 0x00
        print "created adc for pin",pin
    def set_pin(self, pin, average):
        """Set the adc pin and average flag (0/1) for future reads [No error checking]"""
        if not pin in self.VALID_PINS:
            raise ValueError("Adc: invalid pin: "+str(pin)+" not in "+str(self.VALID_PINS))
        if not average in (0,1):
            raise ValueError("Adc: average("+str(average)+") must be 0 or 1")
        self.read_struct = struct.pack("iiiH", pin, average, 0, 0)
    def raw_read(self):
        """Returns the raw (unscaled) adc reading on pin defined in self.read_struct"""
        return struct.unpack("iiiH",fcntl.ioctl(self.dev, self.TWL_RAW_READ, self.read_struct))[3]
    def read(self):
        """Returns the adc voltage reading on pin defined in self.read_struct"""
        #ret = read_madc_struct(fcntl.ioctl(self.dev,self.raw_read,self.read_struct))
        # trigger conversion
        #i2cset -f -y 0x4a 0x12 0x20
        # check status of conversion (look for 0x01 [busy bit] to go low)
        #i2cget -f -y 0x4a 0x12
        # reset interrupt (0x02 [sw interrupt bit should be high])
        #i2cget -f -y 0x4a 0x61
        # read value (lsb then msb)
        #lsb = i2cget -f -y 0x4a 0x3f
        #msb = i2cget -f -y 0x4a 0x40
        # convert bit
        #val = msb<<2 + lsb>>6 #check that this is correct
        #print "read adc value"
        # 2.5 / 1024.0 = 0.00244140625
        #return ret[3] * 0.00244140625
        return self.raw_read() * self.SCALE
    def read_pin(self,pin,average):
        """Returns the adc voltage reading on pin. This call changes self.read_struct"""
        self.set_pin(pin,average)
        return self.read()

class FakeAdc(Adc):
    def __init__(self, pin=3, average=1):
        self.set_pin(pin, average)
    def set_pin(self, pin, average):
        if not pin in self.VALID_PINS:
            raise ValueError("Adc: invalid pin: "+str(pin)+" not in "+str(self.VALID_PINS))
        if not average in (0,1):
            raise ValueError("Adc: average("+str(average)+") must be 0 or 1")
    def raw_read(self):
        return 0.