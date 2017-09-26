'''
/*
 * Copyright 2010-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''

import sys
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import serial
import time
import getopt
import os
import subprocess
import json
import commands
from path import *
from pprint import pprint
from uuid import getnode as get_mac
from paasmerGpio import *

if (len(feedname) == len(feedpin) == len(connectiontype) == len( feedtype)):
	print " Starting the Execution......"
else:
	print " Error : Please check the Feed details in the Config file"
	sys.exit(0)
	

gpioSetup()

print feedname	
print feedpin
index=0


for i in enumerate(feedtype):
	if (i[1] == "sensor"):
			print ( connectiontype[index])
			if connectiontype[index]=="GPIO" :
				gpioModesetup(feedpin[index],"IN")
				index = index + 1
			else :
				index= index + 1
	elif (i[1] == "actuator"):
			if connectiontype[index]=="GPIO" :
				gpioModesetup(feedpin[index],"OUT")
				index = index + 1
			else :
				index = index + 1


# Custom MQTT message callback
def customCallback(client, userdata, message):
	print("Received a new message:----------->>>> ")
	print(message.payload)
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")
	subscribeMsg = (message.payload)	
        for i in range(0, len(subscribeMsg)):
                if subscribeMsg[i] == ' ':
                        myFeed = subscribeMsg[0:i]
                	myStatus = subscribeMsg[i+1:len(subscribeMsg)]
	print("*********************")
	print(myFeed)
	print(myStatus)
	print("*********************")
	
	if myFeed in feedname:
		index=feedname.index(myFeed)
		if myStatus == "on" or myStatus == "ON":
			if connectiontype[index]== "GPIO":
				gpioWrite(feedpin[index],1)	
			elif connectiontype[index]== "zigbee":
				zigbee= "GPIO " + str(feedpin[index]) + " ON*"
				zigbeeWrite(zigbee)
			elif connectiontype[index]== "Wifi":
				WifiWrite(feedname[index],feedpin[index],"ON")
			elif connectiontype[index] == "BLE":
				WriteBlue(feedpin[index],"on")

				 		 
		elif myStatus == "off" or myStatus == "OFF":
			if connectiontype[index]== "GPIO":
				gpioWrite(feedpin[index],0)	
		
			elif connectiontype[index]== "zigbee":
				zigbee= "GPIO " + str(feedpin[index]) + " OFF*"
				zigbeeWrite(zigbee)
			
			elif connectiontype[index]== "Wifi":
				WifiWrite(feedname[index],feedpin[index],"OFF")
			elif connectiontype[index] == "BLE":
				WriteBlue(feedpin[index],"off")
			

# Usage
usageInfo = """Usage:

Use certificate based mutual authentication:
python basicPubSub.py -e <endpoint> -r <rootCAFilePath> -c <certFilePath> -k <privateKeyFilePath>

Use MQTT over WebSocket:
python basicPubSub.py -e <endpoint> -r <rootCAFilePath> -w

Type "python basicPubSub.py -h" for available options.
"""
# Help info
helpInfo = """-e, --endpoint
	Your AWS IoT custom endpoint
-r, --rootCA
	Root CA file path
-c, --cert
	Certificate file path
-k, --key
	Private key file path
-w, --websocket
	Use MQTT over WebSocket
-h, --help
	Help information


"""

# Read in command-line parameters
useWebsocket = False
host = "a3rwl3kghmkdtx.iot.us-west-2.amazonaws.com"
rootCAPath = path + "certs/rootCA.crt"
certificatePath = path + "certs/" + DeviceName + "-certificate.pem.crt"
privateKeyPath = path + "certs/" + DeviceName + "-private.pem.key"


# Missing configuration notification
missingConfiguration = False
if not host:
	print("Missing '-e' or '--endpoint'")
	missingConfiguration = True
if not rootCAPath:
	print("Missing '-r' or '--rootCA'")
	missingConfiguration = True
if not useWebsocket:
	if not certificatePath:
		print("Missing '-c' or '--cert'")
		missingConfiguration = True
	if not privateKeyPath:
		print("Missing '-k' or '--key'")
		missingConfiguration = True
if missingConfiguration:
	exit(2)

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
	myAWSIoTMQTTClient = AWSIoTMQTTClient("basicPubSub", useWebsocket=True)
	myAWSIoTMQTTClient.configureEndpoint(host, 443)
	myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
	myAWSIoTMQTTClient = AWSIoTMQTTClient("basicPubSub")
	myAWSIoTMQTTClient.configureEndpoint(host, 8883)
	myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(100)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(50)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe(UserName+"_"+DeviceName, 1, customCallback)

time.sleep(5)

# Publish to the same topic in a loop forever
loopCount = 0
MyMac = open('/sys/class/net/eth0/address').read()
MyMac = MyMac[0:len(MyMac)-1]


#myAWSIoTMQTTClient.publish("paasmer_device_details",jsonbasestring, 1)
i=0
while True:
		k=0
		while k < len(feedpin) :
			if connectiontype[k]== "GPIO" :
				sout1 = gpioRead(feedpin[k])
			elif connectiontype[k]== "zigbee" :
				sout1= gpio_read(feedpin[k])
			elif connectiontype[k]== "Wifi":
				sout1 = WifiRead(feedname[k],feedpin[k],"GETSTATE") 
			elif connectiontype[k] == "BLE":
				sout1 = ReadBlue(feedpin[k])
				
			jsonstring="{\n\"feeds\":[{\"feedname\":\"%s\",\n\"feedtype\":\"%s\",\n\"feedpin\":\"%d\",\"feedvalue\":\"%d\",\"ConnectionType\":\"%s\"}," % (feedname[k],feedtype[k],feedpin[k],sout1,connectiontype[k])
			k=k+1
			if k < len(feedpin):
				if connectiontype[k]== "GPIO" :
					sout2 = gpioRead(feedpin[k])
				elif connectiontype[k]== "zigbee" :
                                        sout2= gpio_read(feedpin[k])
				elif connectiontype[k]== "Wifi":
					sout2 = WifiRead(feedname[k],feedpin[k],"GETSTATE") 
				elif connectiontype[k] == "BLE":
					sout2 = ReadBlue(feedpin[k])
					
				jsonstring= jsonstring + "\n{\"feedname\":\"%s\",\n\"feedtype\":\"%s\",\n\"feedpin\":\"%d\",\"feedvalue\":\"%d\",\"ConnectionType\":\"%s\"}," % (feedname[k],feedtype[k],feedpin[k],sout2,connectiontype[k]) 
				k=k+1
			else :
				jsonstring= jsonstring + "\n{\"feedname\":\"\",\n\"feedtype\":\"\",\n\"feedpin\":\"\",\"feedvalue\":\"\",\"ConnectionType\":\"\"},"
			if k < len(feedpin):
				if connectiontype[k]== "GPIO" :
					sout3 = gpioRead(feedpin[k])
				elif connectiontype[k]== "zigbee" :
                                        sout3= gpio_read(feedpin[k])
				elif connectiontype[k]== "Wifi":
					sout3 = WifiRead(feedname[k],feedpin[k],"GETSTATE") 
				elif connectiontype[k] == "BLE":
					sout3 = ReadBlue(feedpin[k])

				jsonstring= jsonstring + "\n{\"feedname\":\"%s\",\n\"feedtype\":\"%s\",\n\"feedpin\":\"%d\",\"feedvalue\":\"%d\",\"ConnectionType\":\"%s\"}]," % (feedname[k],feedtype[k],feedpin[k],sout3,connectiontype[k])
                                k=k+1
                        else :
                                jsonstring= jsonstring + "\n{\"feedname\":\"\",\n\"feedtype\":\"\",\n\"feedpin\":\"\",\"feedvalue\":\"\",\"ConnectionType\":\"\"}],"

			jsonstring= jsonstring + "\"messagecount\": \"%d\",\"paasmerid\": \"%s\",\"username\":\"%s\",\"devicename\":\"%s\",\"devicetype\":\"SBC\",\"Language\": \"Python\",\"Bluetooth\":\"%d\",\"Wifi\":\"%d\",\"ThingName\":\"%s\",\"ThingARN\":\"%s\"}" % (loopCount,MyMac,UserName,DeviceName,bluetoothDiscover,wifiDiscover,ThingName,ThingArn)
			time.sleep(5)
			
			myAWSIoTMQTTClient.publish("paasmerv2_device_online",jsonstring, 1)
		
		
		
		loopCount += 1
		print "loop count is " + str(loopCount)
		if loopCount%10 == 0 :
			DiscoverWifi()
			DiscoverBlue()
		time.sleep(timePeriod)

