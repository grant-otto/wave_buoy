#! /usr/bin/python3

'''
Test script for processing accelerometer data
Grant Otto, Hunter Tipton, Taylor Deemer
University of Delaware
'''


l = length(a); % assume l even 
 w = 2*pi*fs/l*(-l/2:l/2-1);
 A = fftshift(fft(a));
 D = A./-w.^2;
