#! /usr/bin/python3

'''
Main script for open-source wave buoy
Grant Otto, Hunter Tipton, Taylor Deemer
University of Delaware
'''

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

date = datetime.strftime(datetime.utcnow(),'%Y%m%d%H%M%S')

#Filename: uncomment for the correct machine
#filename = '/home/grant/Documents/2018_schoolyear/MAST632/wave_buoy/'+date+'acc_data.csv'

filename= '/home/pi/wave_data/'+date+'acc_data.csv'

open(filename,"w+")
line=['Time Stamp','Outside Air Temp', 'Water Temp', 'Inside Temperature', 'Accelerometer X', 'Accelerometer Y', 'Accelerometer Z', 'Mag X', 'Mag Y', 'Mag Z', 'Gyro X', 'Gyro Y', 'Gyro Z', 'Euler X', 'Euler Y', 'Euler Z', 'Quaternion X', 'Quaternion Y', 'Quaternion Z', 'Lin Acc X', 'Lin Acc Y', 'Lin Acc Z', 'Gravity X', 'Gravity Y', 'Gravity Z']
with open(filename, "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(line)
###
'''
csv indices:
0: time stamp
1: outside air temp
2: water temp
3: inside temperature
4: acc x
5: acc y
6: acc z
7: mag x
8: mag y
9: mag z
10: gyro x
11: gyro y
12: gyro z
13: Euler x
14: Euler y
15: Euler z
16: quaternion x
17: quaternion y
18: quaternion z
19: linear acceleration x
20: linear acceleration y
21: linear acceleration z
22: gravity x
23: gravity y
24: gravity z

'''

while True:
        ##############################
        '''
        read in accelerometer data
        '''
        ##############################
        line=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        line[0]=int(datetime.strftime(datetime.utcnow(),'%Y%m%d%H%M%S'))
        #line[3]=float('{}'.format(sensor.temperature()))
        for i in range(3):
                line[i+4]=float('{}'.format(sensor.accelerometer[i]))
        for i in range(3):
                line[i+7]=float('{}'.format(sensor.magnetometer[i]))
        for i in range(3):
                line[i+10]=float('{}'.format(sensor.gyroscope[i]))
        for i in range(3):
                line[i+13]=float('{}'.format(sensor.euler[i]))
        for i in range(3):
                line[i+16]=float('{}'.format(sensor.quaternion[i]))
        for i in range(3):
                line[i+19]=float('{}'.format(sensor.linear_acceleration[i]))
        for i in range(3):
                line[i+22]=float('{}'.format(sensor.gravity[i]))
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

        line[1]=airtemp
        line[2]=watertemp
        ### Write to a file

        with open(filename, "a") as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                writer.writerow(line)
        #print(line)

        time.sleep(0.5)

