#!/usr/bin/env python
#reads both temperature sensors. the sensors have their own serial numbers that should not change.

import os


def read(ds18b20):
    location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
    tfile = open(location)
    text = tfile.read()
    tfile.close()
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    celsius = temperature / 1000
    return celsius
 
while True:
	print("air temperature:   %0.3f C" % read("28-020691770b3c"))
	print("water temperature: %0.3f C" % read("28-020391774c3f"))
