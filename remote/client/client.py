#!/usr/bin/env python

import Pyro.core
import sys

# you have to change the URI below to match your own host/port.
remote = Pyro.core.getProxyForURI("PYRO://"+sys.argv[1])

print remote.hello()

# test pwm
duty = 0.5
print "setting pwm to duty:",duty,"... ",
ratRemote.pwm_set_duty(duty)
print "done"

print "enabling pwm... "
remote.pwm_enable()
print "done"

print "reading adc... "
v = remote.adc_read()
print "read:", v
