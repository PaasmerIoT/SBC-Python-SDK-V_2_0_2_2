# SBC-Python-SDK-V_2_0_2_2
**Paasmer IoT SBC-Python-SDK-V_2_0_2_2** for Single Board Computers Running Linux

## Overview
The **Paasmer SBC-Python-SDK-V_2_0_2_2** for **Single Board Computers (SBC)** like Raspberry-PI, Banana-PI, Orange-PI, Odroidxu4 and BeagleBone is a collection of source files that enables you to connect to the Paasmer IoT Platform. It includes the transport client for **MQTT** with **TLS** support.  It is distributed in source form and intended to be built into customer firmware along with application code, other libraries and RTOS.

## Features
The **SBC-Python-SDK-V_2_0_2_2** simplifies access to the Pub/Sub functionality of the **Paasmer IoT** broker via **MQTT**.The SDK has been tested to work on the **Raspberry PI 3, Banana-PI, Orange-PI, Odroidxu4 and BeagleBone**.

## MQTT Connection
The **SBC-Python-SDK-V_2_0_2_2** provides functionality to create and maintain a mutually authenticated TLS connection over which it runs **MQTT**. This connection is used for any further publish operations and allow for subscribing to **MQTT** topics which will call a configurable callback function when these topics are received.

## Protocols Supported
The **SBC-Python-SDK-V_2_0_2_2** is equipped with the Zigbee, WiFi and Bluetooth (BLE) protocol support along with Board GPIO's.

## Pre Requisites
Registration on the [PAASMER portal](http://developers.paasmer.co/) is necessary to connect the devices to the **Paasmer IoT Platform** .

##  Optional Requisites
* WiFi devices - Paasmer IoT is supports Belkin Wemo and Philips Hue bridge.
* Bluetooth Light - Paasmer IoT supports Magic Light smart LED bulbs.
* ZigBee modules

**Note- The WiFi devices must be connected to the local network same as that of your SBC.**

### ZigBee Requisites
In order to use the Zigbee the following is required.

* Raspberry PI 3 Model B Board.

* Arduino UNO Board.

* 2 ZigBee modules.

* XCTU Software installed on your system for ZigBee configuration. [XCTU software](https://www.digi.com/products/xbee-rf-solutions/xctu-software/xctu)

* Lastest version of Arduino IDE to installed on your computer. [Arduino software](https://www.arduino.cc/en/main/software)

# Installation

* Download the SDK or clone it using the command below.

```
$ git clone https://github.com/PaasmerIoT/SBC-Python-SDK-V_2_0_2_2.git
$ cd SBC-Python-SDK-V_2_0_2_2
```
* To install dependencies, follow the commands below

```
$ sudo chmod 777 ./*
$ sudo ./install.sh
```
This will take some time to install the required softwares and packages.

## Device Registration
The Device Registration can be done in two ways, either through Web UI or Using command line.

#### Using Command line

* To register the device to the Paasmer IoT Platform, the following command need to be executed.

```
$ sudo ./paasmerDeviceRegistration.sh
```

This will ask for the UserName and DeviceName. Give a unique DeviceName for your device and that must be alphanumeric without any spaces[a-z A-Z 0-9].

* Upon successful completion of the above command, the following commands need to be executed.
```
1) sudo su 
2) source ~/.bashrc 
3) PAASMER_THING 
4) PAASMER_POLICY 
5) sed -i 's/alias PAASMER/#alias PAASMER/g' ~/.bashrc 
6) exit 
```

* Edit the config.py file to include the user name(Email),feed names , feed types, connnectiontype and feed pin details. 

```c
import serial

from details import *

feedname = ["Sensor1","sensor2","actuator","actuator2",...] # Do not provide any space for feedname

feedtype = ["sensor","sensor","actuator","actuator",...]

feedpin = [15,17,31,8,...]

connectiontype = ["GPIO","GPIO","GPIO","zigbee",...]

timePeriod = 5

ser = 0

#ser = serial.Serial("/dev/ttyUSB0", 9600) # uncomment this line and edit with the USB port if you are using Zigbee

wifiDiscover = 1

bluetoothDiscover = 0

```
#### Using Web UI
* Login to http://developers.paasmer.co/, create a device and download the credentials.
* Copy the credential files from downloaded `zip` file and place them in the `<certs>` directory of the SDK.
* Copy the `config.py` file in the main `<installation dir>`.

### ZigBee Configuration (Optional)

To establish, the ZigBee protocol the 2 ZigBee modules are to configured as a Coordinator and a Router. The ZigBee at the RaspberryPi side is to be configured as a Coordinator and the one at the Arduino side as a Router. Use XCTU software to Configure the ZigBee's as explained in the `ZigBEE_config.pdf` file.

 
## Arduino Board 

* Connect the ZigBee Router device to the Arduino UNO as give below

| Arduino   | XBee |
| --------- | -----|
| 5V        | 5V   |
| GND       | GND  |
| TX        | RX   |
| RX        | TX   |


* Open a new Sketch, Copy and Paste from the `ZigBee.ino` file in `<Arduino Sketch_DIR>/`.

* Connect the Arduino UNO board to your system, open the Arduino IDE and click on the `TOOLS` icon, select the `Board` as **Arduino/Genuino UNO** and select the port in which the board is connected in the `Port` option. 

* Also edit the `config.h` in the Arduino Sketch similar to our `config.py` file in RaspberryPi. The code sample is as below,

```
#define devicename "Zigbee" //your device name

#define timePeriod 2 //change the time delay as you required for sending sensor values to paasmer cloud

char feedname[][10]={"Feed1","Feed2","Feed3","feed4","feed5","feed6"};

String feedtype[]={"sensor","sensor","sensor","actuator","actuator","actuator"};

String connectiontype[]= {"GPIO","GPIO","zigbee","GPIO","GPIO","zigbee"};

int feedpin[]={2,4,5,6,32,8};
```
* Save and Run the code in Arduino UNO.

* Connect the ZigBee Coordinator device to the RaspberryPi through the USB2.0 cable. (Only if ZigBee is used)

## Execution 
* Go to the diectory below.

```
$ cd samples/basicPubSub/
```
      
* Run the code using the command below.

```
$ sudo python basicPubSub.py
```

* The device would now be connected to the Paasmer IoT Platform and publishing sensor values are specified intervals.

## Support

The support forum is hosted on the GitHub, issues can be identified by users and the Team from Paasmer would be taking up requests and resolving them. You could also send a mail to support@paasmer.co with the issue details for quick resolution.

## Note

* The Paasmer IoT SBC-Python-SDK-V_2_0_2_2 utilizes the features provided by AWS-IOT-SDK for Python.
