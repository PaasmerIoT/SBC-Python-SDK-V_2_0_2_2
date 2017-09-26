from path import *
from config import *
from deviceType import *
import os
import serial
import time
import re


#......for bluetooth

from magicblue import MagicBlue
BlueIP = []
BlueStatus = []
bulb = 0
blue = 1
def DiscoverBlue():
        global bulb
        find = 0
        data = os.popen("sh PaasmerDiscoverBlue.sh LEDBlue").readlines()
        
        if data:
                for blue_ip in enumerate(data):
                        print "The Bluetooth Bulb MAC-ID is " + blue_ip[1].strip("\n")
                        #BlueIP.append(data[0])
                        #print BlueIP

                        for i in enumerate(BlueIP):
                                if i[1] == blue_ip[1].strip("\n"):
                                        find = 1
                                        break
                        if find == 1:
                                print "Feed is already available"
                        else:
                                BlueIP.append(blue_ip[1].strip("\n"))
                                BlueStatus.append(0)
                                bulb = bulb + 1
                                feedname.append("magicbulb" + str(bulb))
                                feedpin.append(bulb)
                                feedtype.append("actuator")
                                connectiontype.append("BLE")
                                print feedname
                                print BlueIP
                                print feedpin
                                print feedtype
                                print connectiontype
        else:
                print "No Data available"


def ConnectBlue(mac):
        global blue
        if mac:
                blue = MagicBlue(mac, 9)
                status = blue.connect()
                return status
        else :
                return false
def WriteBlue(number, state):
        global blue
        mac = BlueIP[number - 1]
        status = ConnectBlue(mac)
        if status:
                if state == "on":
                        print "BLE Bulb ON"
                        blue.turn_on()
                        BlueStatus[number - 1] = 1
                        #blue.disconnect()
                else:
                        print "BLE Bulb OFF"
                        blue.turn_off()
                        BlueStatus[number - 1] = 0
                        #blue.disconnect()
                time.sleep(1)
                blue.disconnect()
                
def ReadBlue(number):
        print "The bulb status is " + str(BlueStatus[number - 1])
        return BlueStatus[number - 1]

#................end for bluetooth


#..............for belkin.....................#

BelkinIP = []
BelkinCount = 0

def getBelkinIP():
	global BelkinCount
	find = 0
	ip_new = []
	grep = "Location"
	command = "gssdp-discover -t urn:Belkin:device:1 -n 3 -i wlan0 | grep " + grep
	data = os.popen(command).readlines()
	if data:
		i=0
		ip= re.sub('[^0-9]','', data[0])
		while i < 12:
			ip_new.append(ip[i])
			i = i + 1
			if i % 3 == 0:
				if i <12:
					ip_new.append('.')
		Belkin_ip = ''.join(ip_new)
		print "Belkin ip = " + Belkin_ip
		for i in enumerate(BelkinIP):
			if i[1] == Belkin_ip:
				find = 1
				break
		if find == 1:
			print "Feed is already available"
		else:
			BelkinIP.append(Belkin_ip)
			BelkinCount = BelkinCount + 1
			feedname.append("Belkin" + str(BelkinCount))
			feedpin.append(BelkinCount)
			feedtype.append("actuator")
			connectiontype.append("Wifi")
			print " ***********************************************"
			print feedname
			print feedpin
			print feedtype
			print connectiontype
			print " ***********************************************"
			
		return Belkin_ip
	else:
		 return 0

def Belkin_Write(belkinNumber,message):
	command = "wemo -h " + BelkinIP[belkinNumber - 1] + " -a " + message
	print "Belkin " + message
	os.system(command)

def Belkin_Read(belkinNumber):
        command = "wemo -h " + BelkinIP[belkinNumber - 1] + " -a GETSTATE"
	belkindata = os.popen(command).readlines()
	if "8" in belkindata[0]:
		return 1
	else:
		return 0

#.........end for belkin..................#

#...........for philips...................#

def getPhilipsIP():
	ip_new = []
	grep = "Location"
	command = "gssdp-discover -t urn:schemas-upnp-org:device:basic:1 -n 3 -i wlan0 | grep " + grep
	data = os.popen ( command).readlines()
	if data:
		i=0
		ip= re.sub('[^0-9]','', data[0])
		while i < 12:
			ip_new.append(ip[i])
			i = i + 1
			if i % 3 == 0:
				if i <12:
					ip_new.append('.')
		Philips_ip = ''.join(ip_new)
		print "Philips ip = " + Philips_ip
		return Philips_ip

def Philips_config():
	grep = "Location"
	command = "gssdp-discover -t urn:schemas-upnp-org:device:basic:1 -n 3 -i wlan0 | grep " + grep
	data = os.popen(command).readlines()
	if data:
		philips_ip = getPhilipsIP()
		if philips_ip:		

			os.system("hue -H " + philips_ip + " register")
			return 1
	else:
		print "The Philips Hue is OFF or not available in thw network"

def Philips_write(message):
	data = 1
	if data:
		incoming = "hue lights " + message
		os.system(incoming)
	else:
		print("Philips is not connected now")

def Philips_read(message):
	data = 1
	if data:
		incoming = "hue lights " + message
		read = os.popen(incoming).readlines()
		if "on" in read[0]:
			print("Philips is ON")
			return 1
		else:
			print("Philips is OFF")
			return 0

#.......end for philips....................#

#.....for wifi.............................#

def wifi_setup():
	os.system("./discover.sh")
        grep = "Location"
        command = "gssdp-discover -t urn:schemas-upnp-org:device:basic:1 -n 3 -i wlan0 | grep " + grep
        philips = os.popen(command).readlines()
        if philips:
                value = Philips_config()
                return value
        command =  "gssdp-discover -t urn:Belkin:device:1 -n 3 -i wlan0 | grep " + grep

def DiscoverWifi():
	status = wifi_setup()
        if status == 1:
                bulbs = os.popen("hue lights").readlines()
                print "Number of bulbs connected via HUE = " +  str(len(bulbs))
                i = 0
                for i in range(0,len (bulbs)):
			find = 0
			philipsbulbname = "philips" + str(bulbs[i][3])
			for j in enumerate(feedname):
				if j[1] == philipsbulbname:
					find = 1
					break
			if find == 1:
				print "Feeds is already available"
			else:
	                        feedname.append("philips" + str(bulbs[i][3]))
	                        feedtype.append("actuator")
	                        connectiontype.append("Wifi")
	                        feedpin.append(int(bulbs[i][3]))
	getBelkinIP()

def WifiWrite(feedname,feedpin,state):
	if "philips" in feedname:
		if state== "ON":
			philips = str(feedpin) + " on"
			Philips_write(philips)
		else:
			philips = str(feedpin) + " off"
			Philips_write(philips)
			
	elif "Belkin" in feedname:
		Belkin_Write(feedpin,state)

def WifiRead(feedname,feedpin,message):
	if "philips" in feedname:
		data = int(Philips_read(str(feedpin)))
		return data
	if "Belkin" in feedname:
		data =  int(Belkin_Read(feedpin))
		return data

#..........end for wifi.......................#


def gpioSetup():
        if ser :
		print ser
                ser.isOpen()
	if wifiDiscover == 1:
		print "Installing dependencies for Wifi"
		DiscoverWifi()
	if bluetoothDiscover == 1:
		print "Installing dependencies for Bluetooth"
		os.system("sh PaasmerBLEinstall.sh")
		DiscoverBlue()


def gpio_read(pinNum):
	n= "Read pin " + str(pinNum) + "*"
	print n
	ser.write(n)
	time.sleep(.5)
	incoming = ser.read()
	return int(incoming )

def zigbeeWrite(zigbee):
	ser.write(zigbee)


def gpioModesetup(pinNum, mode) :
	if deviceType == "raspberrypi" or deviceType== "bananapi" or deviceType=="orangepi" or deviceType== "ordroidxu4" :
		if mode== "OUT" :
			command= "gpio -1 mode " + str(pinNum) + " out"
			os.system (command)
			command="\0"
		elif mode == "IN" :
			command= "gpio -1 mode " + str(pinNum) + " in"
			os.system (command)
			command="\0"
	elif deviceType == "beaglebone" :
		if mode== "OUT" :
			command= "sudo echo " + str(pinNum) + " > /sys/class/gpio"
			os.system (command)
			command="\0"
			command= "sudo echo out > /sys/class/gpio/gpio" + str(pinNum) + "/direction"
			os.system (command)
			command="\0"
		elif mode == "IN" :
			command= "sudo echo " + str(pinNum) + " > /sys/class/gpio"
			os.system (command)
			command="\0"
			command= "sudo echo in > /sys/class/gpio/gpio" + str(pinNum) + "/direction"
			os.system (command)
			command="\0"

def gpioWrite(pinNum, state) :
	if deviceType == "raspberrypi" or deviceType== "bananapi" or deviceType=="orangepi" or deviceType== "ordroidxu4" :
		command = "gpio -1 write " + str(pinNum) + " " +  str(state)
		print(command) 
		os.system(command)
		command="\0"
	elif deviceType == "beaglebone" :
		command = "sudo echo " + str(state) + " > /sys/class/gpio/gpio" +  str(pinNum) + "/value"
		os.system(command)
		command="\0"
def gpioRead(pinNum) :
	res=0
	if deviceType == "raspberrypi" or deviceType== "bananapi" or deviceType=="orangepi" or deviceType== "ordroidxu4" :
		command = "gpio -1 read " + str(pinNum)
		data = os.popen(command).readlines()
		command = "\0"
		res = int(data[0])
	elif deviceType == "beaglebone" :
		command = "sudo cat /sys/class/gpio/gpio" + str(pinNum) + "/value"
		data = os.popen(command).readlines()
		command = "\0"
	res = int(data[0])
	return res
		

