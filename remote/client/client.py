#!/usr/bin/env python

import Pyro.core # Pyro 3.8.1
import sys

# you have to change the URI below to match your own host/port.
remote = Pyro.core.getProxyForURI("PYRO://"+sys.argv[1])

print "Ping:", remote.ping()

# test pwm
duty = 0.5
print "setting pwm to duty:",duty,"... ",
remote.pwm_set_duty(duty)
print "done"

print "enabling pwm... "
remote.pwm_enable()
print "done"

print "reading adc... "
v = remote.adc_read()
print "read:", v
