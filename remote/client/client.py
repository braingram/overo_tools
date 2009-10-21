#!/usr/bin/env python

import Pyro.core
import sys

# you have to change the URI below to match your own host/port.
remote = Pyro.core.getProxyForURI("PYRO://"+sys.argv[1])

print remote.hello()

duty = 0.5
print "setting pwm to duty:",duty,"... ",
#ratRemote.pwm.set_duty(duty)
remote.pwm.enable()
remote.pwm.disable()
print "done"

print "enabling pwm... "
remote.pwm.enable()
print "done"

print "reading adc... "
v = remote.adc.read()
print "read:", v
