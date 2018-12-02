Open Source Wave Buoy

Created by Grant Otto, Hunter Tipton, and Taylor Deemer
University of Delaware School of Marine Science and Policy


Installation instructions for Raspberry Pi:

open a terminal and enter:

	git clone https://github.com/seaotto/wave_buoy.git
Accelerometer (BN055):
enable I2C and SPI using 
	sudo raspi-config
under Interfacing Options
install circuit python:

	sudo pip3 install adafruit-circuitpython-bno055
Thermometers (DS18B20):
The thermometers use the One Wire Protocol and can be put in parallel on the same pin.
Use

	sudo raspi-config
and enable the One Wire Protocol under Interfacing Options.
For final One Wire configuration, use:

	sudo modprobe w1-gpio
	suod modprobe w1-therm
Next,

	sudo nano boot/config.txt
add a line at the bottom:

	dtoverlay=w1-gpio,gpiopin=XXX
where XXX is the number of the pin you plug your thermometers into. The default is pin 4.
To check the thermometers, 

	cd /sys/bus/w1/devices
	ls
for each thermometer you plug in, you should see a folder starting with 28-[...]

	cd 28-[...]
	cat w1_slave
you should see in the bottom right a number in the 10's of thousands. Divide by 1000 and that is your temperature in *C. There is a parser in temptest.py for this.


Running Instructions:
Currently, there is no support for wave height, only sea temp, air temp, and period (still quite buggy).
However, there is a script that can log all accelerometer data directly every 1/2 second.

As of right now, only one of the two scripts (main.py and accelLog.py) can be run at once due to their common use of the i2c port.
to run one of them, add 

	./main.py & 
or 

	./accelLog.py &
to the bottom of your ~/.bashrc. This will make it run on boot in the background. To stop it,

	ps
	kill [PID]
where the PID is the PID of the script you are running as displayed by the ps command.

The log files are kept in ~/wave_data/ and timestamped at the start of the log with UTC time. All timestamps in all files are UTC.


U of D Wave buoy notes:

ip address in lewes: 128.4.232.122
ip address in newark: 128.4.208.190
temp sensors: 69 is air
	      39 is water
