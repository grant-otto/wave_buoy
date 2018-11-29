#! /usr/bin/python3

'''
Main script for open-source wave buoy
Grant Otto, Hunter Tipton, Taylor Deemer
University of Delaware
'''
import numpy as np
import scipy.fftpack as fftpack
import scipy.signal as signal
from scipy.signal import butter, lfilter, freqz
import csv
from datetime import datetime
import time
import board
import busio
import adafruit_bno055
import os


#initialize accelerometer
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055(i2c)

#####
'''
Create and Open CSV file with header
'''
#####

date = datetime.strftime(datetime.now(),'%Y%m%d')

#Filename: uncomment for the correct machine
#filename = '/home/grant/Documents/2018_schoolyear/MAST632/wave_buoy/'+date+'wave_data.csv'
filename = '/home/pi/wave_data/'+date+'wave_data.csv'


open(filename,"w+")
line=['Time Stamp', 'Water Temperature (Degrees C)', 'Air Temperature (Degrees C)', 'Wave Period']
with open(filename, "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(line)


While True:
##############################
'''
read in accelerometer data
'''
##############################
a=[]
tic = time.clock()
toc= time.clock()+15
while float(time.clock())<toc:
    elem=float('{}'.format(sensor.accelerometer[0]))
    a.append(elem)

##############################
'''
Calculate wave period with FFT

delete outliars, then apply a low pass filter
finally take the max falue of the fft of acceleration data and get the corresponding frequency value
to get position data, simply double integrate the fft of acc. right now it isn't giving good results.
'''
##############################


for i in range(len(a)): #clean data, bisecting values >50
    if abs(a[i])>50:
        a[i]=(a[i-1]+a[i-1])/2
l = len(a) 
if l%2 != 0: #make a even by deleting the last element if it isn't already
	lis=list(a)
	del lis[-1]
	a=tuple(lis)
l=int(len(a)) #reset l after cleaning, evening
avg=np.average(a)
a=a-avg
Fs = 50  # sampling rate
Ts = 1.0/Fs # sampling interval
Ts=15/len(a)
Fs=1/Ts
k=np.arange(l)
T = l/Fs
frq = k/T # two sides frequency range
frq = frq[range(int(l/2))] # one side frequency range

#band pass filter
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

order =6
cutoff = 5 #cutoff frequency in hertz
a = butter_lowpass_filter(a, cutoff, Fs, order)#apply lowpass filter
A = np.fft.fftshift(np.fft.fft(a)/l) # fft computing and normalization
A = abs(np.fft.fft(a)/l) # fft computing and normalization
Apos = A[range(int(l/2))]
maxacc = max(Apos)
frq=list(frq)
Apos=list(Apos)


####
''' WAVE PERIOD '''
####
period = 1/abs(frq[Apos.index(maxacc)])


#################################
'''
Read in Thermometers
'''
#################################

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
 

#air temp
airtemp=float("%.3f" % read("28-020691770b3c"))

#water temp
watertemp=float("%.3f" % read("28-020391774c3f"))

#################################
'''
Write to a csv
'''
#################################


line=[datetime.now(), watertemp, airtemp, period]
with open(filename, "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(line)

a=[]


