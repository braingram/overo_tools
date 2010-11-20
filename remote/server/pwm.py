#!/usr/bin/env python

import time

import pydevmem

class OmapPwm:
    VALID_PINS = [8,9,10,11]
    #
    # TODO these are probably better to do as base + offsets
    #
    # CM_CLKSEL_(CORE/PER)
    # register information for selecting which clock drives the pwm
    #  1: 32K clock
    #  0: sys clock
    CLKSEL_ADDR = { 11: 0x48004a40,
                    10: 0x48004a40,
                     9: 0x48005040,
                     8: 0x48005040 }
    CLKSEL_MASK = { 11: 0x00000080,
                    10: 0x00000040,
                     9: 0x00000080,
                     8: 0x00000040 }
    # CM_ICLKEN(1)_(CORE/PER)
    # register information for enabling the interface clock for the pwm
    #  1: enable
    #  0: disable
    # this must be set BEFORE the FCLK can be enabled
    ICLKEN_ADDR = { 11: 0x48004a10,
                    10: 0x48004a10,
                     9: 0x48005010,
                     8: 0x48005010 }
    ICLKEN_MASK = { 11: 0x00001000,
                    10: 0x00000800,
                     9: 0x00000400,
                     8: 0x00000200 }
    # CM_FCLKEN(1)_(CORE/PER)
    # register information for enabling the functional clock for the pwm
    #  1: enable
    #  0: disable
    # this must be set AFTER the ICLK is enabled
    FCLKEN_ADDR = { 11: 0x48004a00,
                    10: 0x48004a00,
                     9: 0x48005000,
                     8: 0x48005000 }
    FCLKEN_MASK = { 11: 0x00001000,
                    10: 0x00000800,
                     9: 0x00000400,
                     8: 0x00000200 }
    # pin muxing register information
    MUX_ADDR = {    11: 0x48002178,
                    10: 0x48002174,
                     9: 0x48002174,
                     8: 0x48002178 }
    MUX_MASK = {    11: 0x0000001f,
                    10: 0x001f0000,
                     9: 0x0000001f,
                     8: 0x001f0000 }
    MUX_VAL = {     11: 0x00000002,
                    10: 0x00020000,
                     9: 0x00000002,
                     8: 0x00020000 }
    # GPTi_TCLR
    # register to control the timer
    TCLR_ADDR = {   11: 0x48088024,
                    10: 0x48086024,
                     9: 0x49040024,
                     8: 0x4903e024 }
    TCLR_OFF = 0x00000000
    TCLR_ON =  0x00001843
    # GPTi_TLDR (no mask needed)
    # timer load registers:
    #  when the counter (TCRR) overflows it is reset to the load value (TLDR)
    #  and the output goes high
    TLDR_ADDR = {   11: 0x4808802c,
                    10: 0x4808602c,
                     9: 0x4904002c,
                     8: 0x4903e02c }
    # GPTi_TMAR (no mask needed)
    # timeer match registers
    #  when the counter (TCRR) matches the match value (TMAR) the output goes low
    TMAR_ADDR = {   11: 0x48088038,
                    10: 0x48086038,
                     9: 0x49040038,
                     8: 0x4903e038 }
    # GPTi_TCRR (no mask needed)
    # timer counter registers
    TCRR_ADDR = {   11: 0x48088028,
                    10: 0x48086028,
                     9: 0x49040028,
                     8: 0x4903e028 }
    #
    #
    def __init__(self, pin=10):
        if not pin in self.VALID_PINS:
            raise Exception("invalid OmapPwm pin: "+str(pin)+" not in "+str(self.VALID_PINS))
        self.pin = pin
        # enable 32k clock for pin
        pydevmem.write(self.CLKSEL_ADDR[pin], 0xffffffff, self.CLKSEL_MASK[pin])
        # enable interface clock (ICLK)
        pydevmem.write(self.ICLKEN_ADDR[pin], 0xffffffff, self.ICLKEN_MASK[pin])
        # enable functional clock (FCLK)
        pydevmem.write(self.FCLKEN_ADDR[pin], 0xffffffff, self.FCLKEN_MASK[pin])
        # pause to allow changes to settle
        time.sleep(1)
        # disable timer (TCLR)
        pydevmem.write(self.TCLR_ADDR[pin], self.TCLR_OFF)
        # set mux (MUX)
        pydevmem.write(self.MUX_ADDR[pin], self.MUX_VAL[pin], self.MUX_MASK[pin])
    def enable(self):
        # set the counter (CRR) to it's highest value, this makes the counter overflow
        # on the first clock cycle, bringing the output high
        pydevmem.write(self.TCRR_ADDR[self.pin], 0xffffffff)
        pydevmem.write(self.TCLR_ADDR[self.pin], self.TCLR_ON)
    def disable(self):
        pydevmem.write(self.TCLR_ADDR[self.pin], self.TCLR_OFF)
    def set_load(self, value):
        pydevmem.write(self.TLDR_ADDR[self.pin], value)
    def set_match(self, value):
        pydevmem.write(self.TMAR_ADDR[self.pin], value)
    def set_duty(self, value):
        print "!!!!!!!!NOT YET IMPLEMENTED"

class FakeOmapPwm(OmapPwm):
    def __init__(self, pin=10):
        if not pin in self.VALID_PINS:
            raise Exception("invalid OmapPwm pin: "+str(pin)+" not in "+str(self.VALID_PINS))
        self.pin = pin
    def enable(self):
        pass
    def disable(self):
        pass
    def set_load(self, value):
        pass
    def set_match(self, value):
        pass

class TpsPwm:
    VALID_PINS = [0,1]
    def __init__(self, pin=0):
        if not pin in self.VALID_PINS:
            raise Exception("invalid TpsPwm pin: "+str(pin)+" not in "+str(self.VALID_PINS))
        # mux pin for pwm0 (0x04 for pwm0, 0x30 for pwm1, 0x34 for both)
        #i2cset -f -y 1 0x49 0x92 0x04
        # turn on pwm0 clock and enable pwm0 (0x05 for pwm0, 0x0a for pwm1, 0x0f for both)
        #i2cset -f -y 1 0x49 0x91 0x05
        # set pwn0_on time (0xf8 for pwm0, 0xfb for pwm1)
        # bit order [7:pwm length 0=128 1=64][6-0:pwm data]
        #i2cset -f -y 1 0x4a 0xf8 0x08
        # set pwm0 off time (0xf9 for pwm0, 0xfc for pwm1)
        # bit order [7:reserved][6-0:pwm data]
        #i2cset -f -y 1 0x4a 0xf9 0x40
        print "created tpspwm for pin",pin
        print "TPS is unimplemented"
        raise Exception("TPS is unimplemented")
    def enable(self):
        # turn on pwm0 clock and enable pwm0 (0x05 for pwm0, 0x0a for pwm1, 0x0f for both)
        #i2cset -f -y 1 0x49 0x91 0x05
        pass
    def disable(self):
        # turn on pwm0 clock and enable pwm0 (0x05 for pwm0, 0x0a for pwm1, 0x0f for both)
        #i2cset -f -y 1 0x49 0x91 0x05
        pass
    def set_on_time(self, on):
        # set pwn0_on time (0xf8 for pwm0, 0xfb for pwm1)
        # bit order [7:pwm length 0=128 1=64][6-0:pwm data]
        #i2cset -f -y 1 0x4a 0xf8 0x08
        pass
    def set_off_time(self, off):
        # set pwm0 off time (0xf9 for pwm0, 0xfc for pwm1)
        # bit order [7:reserved][6-0:pwm data]
        #i2cset -f -y 1 0x4a 0xf9 0x40
        pass
    def set_duty(self, duty):
        pass