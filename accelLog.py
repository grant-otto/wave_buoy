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
line=['Time Stamp', 'Inside Temperature', 'Accelerometer X', 'Accelerometer Y', 'Accelerometer Z', 'Mag X', 'Mag Y', 'Mag Z', 'Gyro X', 'Gyro Y', 'Gyro Z', 'Euler X', 'Euler Y', 'Euler Z', 'Quaternion X', 'Quaternion Y', 'Quaternion Z', 'Lin Acc X', 'Lin Acc Y', 'Lin Acc Z', 'Gravity X', 'Gravity Y', 'Gravity Z']
with open(filename, "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(line)
###
'''
csv indices:
0: time stamp
1: inside temperature
2: acc x
3: acc y
4: acc z
5: mag x
6: mag y
7: mag z
8: gyro x
9: gyro y
10: gyro z
11: Euler x
12: Euler y
13: Euler z
14: quaternion x
15: quaternion y
16: quaternion z
17: linear acceleration x
18: linear acceleration y
19: linear acceleration z
20: gravity x
21: gravity y
22: gravity z

'''

while True:
        ##############################
        '''
        read in accelerometer data
        '''
        ##############################
        line=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        line[0]=datetime.utcnow()
        #line[1]=float('{}'.format(sensor.temperature()))
        for i in range(3):
                line[i+2]=float('{}'.format(sensor.accelerometer[i]))
        for i in range(3):
                line[i+5]=float('{}'.format(sensor.magnetometer[i]))
        for i in range(3):
                line[i+8]=float('{}'.format(sensor.gyroscope[i]))
        for i in range(3):
                line[i+11]=float('{}'.format(sensor.euler[i]))
        for i in range(3):
                line[i+14]=float('{}'.format(sensor.quaternion[i]))
        for i in range(3):
                line[i+17]=float('{}'.format(sensor.linear_acceleration[i]))
        for i in range(3):
                line[i+20]=float('{}'.format(sensor.gravity[i]))

        with open(filename, "a") as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                writer.writerow(line)

        time.sleep(0.5)

