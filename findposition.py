#! /usr/bin/python3

'''
Test script for processing accelerometer data
sample frequency should be 10us.
Grant Otto, Hunter Tipton, Taylor Deemer
University of Delaware
'''
import time
import board
import busio
import adafruit_bno055
import numpy as np

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055(i2c)



print(format(sensor.accelerometer[0]))

store=()
tic=time.clock()
toc=time.clock()+5
print(tic, toc)
while time.clock()<toc:
	store=store+(float(format(sensor.accelerometer[0])),)
print(store)



a=store

#do fft and find amplitude

l = len(a) # assume l even
print(len(a)) 
if l%2 != 0:
	lis=list(a)
	del lis[-1]
	a=tuple(lis)
	

w = 2*np.pi*.00001/l*(np.linspace(-l/2,l/2-1))
A=np.fft.fftshift(np.fft.fft((np.array(a))))
D = A/-w**2

