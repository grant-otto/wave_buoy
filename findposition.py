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
from numpy import linspace
from numpy import pi
from numpy import fft

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
	a.pop(-1)
	

w = 2*pi*.00001/l*tuple(linspace(-l/2,l/2-1))
A = fftshift(fft(a))
D = A/-w**2

