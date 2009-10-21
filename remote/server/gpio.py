#!/usr/bin/env python

import pydevmem

class Gpio:
    availablePins = [144, 145, 146, 147]
    # TODO make these uppercase
    # pin muxing register information
    MUX_ADDR = {    144: 0x48002174,
                    145: 0x48002174,
                    146: 0x48002178,
                    147: 0x48002178 }
    MUX_MASK = {    144: 0x0000001f,
                    145: 0x001f0000,
                    146: 0x0000001f,
                    147: 0x001f0000 }
    MUX_VAL = {     144: 0x0000001c,
                    145: 0x001c0000,
                    146: 0x0000001c,
                    147: 0x001c0000 }
    # bit mask for the following registers:
    #  OE_ADDR, DATA_ADDR
    BIT_MASK = {    144: 0x00010000,
                    145: 0x00020000,
                    146: 0x00040000,
                    147: 0x00080000 }
    # output enable register
    #  0: enable output
    #  1: disable output
    OE_ADDR = {     144: 0x49056034,
                    145: 0x49056034,
                    146: 0x49056034,
                    147: 0x49056034 }
    # output data register
    #  0: set output low
    #  1: set output high
    DATA_ADDR = {   144: 0x4905603c,
                    145: 0x4905603c,
                    146: 0x4905603c,
                    147: 0x4905603c }
    def __init__(self, pin=145):
        if not pin in self.availablePins:
            raise Exception("Gpio: invalid pin:"+str(pin)+" not in "+str(self.availablePins))
        self.pin = pin
        # mux pin, attaching gpio to the pin
        pydevmem.write(self.MUX_ADDR[pin], self.MUX_VAL[pin], self.MUX_MASK[pin])
        #pydevmem.write(self.muxRegs[self.pin], self.muxVals[self.pin], self.muxMasks[self.pin])
        # enable output
        pydevmem.write(self.OE_ADDR[pin], 0x00000000, self.BIT_MASK[pin])
        #pydevmem.write(self.oeReg[self.pin], 0x00000000, self.masks[self.pin])
        print "gpio created on pin",self.pin
    def set_output(self, level):
        pydevmem.write(self.DATA_ADDR[self.pin], level, self.BIT_MASK[self.pin])
        #pydevmem.write(self.dataOut[self.pin], level, self.masks[self.pin])
        print "set output to",level
    def set_high(self):
        self.set_output(0xffffffff)
    def set_low(self):
        self.set_output(0x00000000)