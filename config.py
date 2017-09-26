import serial

from details import *

feedname = ["Sensor1","sensor2","actuator","actuator2",...]

feedtype = ["sensor","sensor","actuator","actuator",...]

feedpin = [15,17,31,8,...]

connectiontype = ["GPIO","GPIO","GPIO","zigbee",...]

timePeriod = 5

ser = 0

#ser = serial.Serial("/dev/ttyUSB0", 9600) # uncomment this line and edit with the USB port if you are using Zigbee

wifiDiscover = 1

bluetoothDiscover = 1
