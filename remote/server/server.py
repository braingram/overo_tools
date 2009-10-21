#!/usr/bin/env python

import Pyro.core
import sys

import pwm
import adc
import gpio

class Remote(Pyro.core.ObjBase):
    """Creates a pretty useless class that just contains an adc (self.adc) and pwm (self.pwm)"""
    def __init__(self):
        Pyro.core.ObjBase.__init__(self)
        self.adc = adc.Adc()
        self.pwm = pwm.OmapPwm()
        self.gpio = gpio.Gpio()
    # pwm
    def pwm_enable(self):
        self.pwm.enable()
    def pwm_disable(self):
        self.pwm.diable()
    def pwm_set_duty(self, duty):
        self.pwm.set_duty(duty)
    # adc
    def adc_read(self):
        return self.adc.read()
    # gpio
    def gpio_set_high(self):
        self.gpio.set_high()
    def gpio_set_low(self):
        self.gpio.set_low()

if __name__ == "__main__":
    Pyro.core.initServer()
    daemon=Pyro.core.Daemon(host=sys.argv[1])
    uri=daemon.connect(Remote(),"remote")
    
    print "The daemon runs on port:",daemon.port
    print "The object's uri is:",uri
    
    daemon.requestLoop()
