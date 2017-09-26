
import time
import os
import RPi.GPIO as GPIO
import eeml
import sys  
sys.path.append('/home/pi/aws-iot-device-sdk-python/')
from config import *



# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        
	
	
	GPIO.setmode(GPIO.BCM)
	DEBUG = 1
	LOGGER = 1

	# set up the SPI interface pins
	GPIO.setup(SPIMOSI, GPIO.OUT)
	GPIO.setup(SPIMISO, GPIO.IN)
	GPIO.setup(SPICLK, GPIO.OUT)
	GPIO.setup(SPICS, GPIO.OUT)

	if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:   
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)

        adcout /= 2       # first bit is 'null' so drop it

	return adcout

def convertTempr(milvolt):
	millivolts = 3.3 - ((milvolt * 3.3)/1024)
        temp_C = (millivolts * 100.0)
        temp_F = ( temp_C * 9.0 / 5.0 ) + 32
	
        temp_C = "%.1f" % temp_C
        temp_F = "%.1f" % temp_F
	return temp_C


def findObstacle(PIN):
	GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN, GPIO.IN)
	return GPIO.input(PIN)

def readUltrasonic(TRIGGER,ECHO):

	
	GPIO.setmode(GPIO.BCM)
	DEBUG = 1
	LOGGER = 1

	#print "Ultrasonic Measurement"

	GPIO.setup(TRIGGER,GPIO.OUT)  # Trigger
	GPIO.setup(ECHO,GPIO.IN)      # Echo

	GPIO.output(GPIO_TRIGGER, False)

	time.sleep(0.5)

	GPIO.output(GPIO_TRIGGER, True)
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, False)
	start = time.time()

	while GPIO.input(GPIO_ECHO)==0:
  		start = time.time()

	while GPIO.input(GPIO_ECHO)==1:
  		stop = time.time()

	elapsed = stop-start

	distance = elapsed * 34300
	distance = distance / 2
	distance = "%.2f" % distance
	return distance


if __name__ == "__main__":

	# temperature sensor connected channel 0 of mcp3008
	adcnum = 0


	SPICLK = tmpspiclk
	SPIMISO = tmpspimiso
	SPIMOSI = tmpspimosi
	SPICS = tmpcs
	GPIO_TRIGGER = distancepin1
	GPIO_ECHO    = distancepin2
	GPIO_OBST_IN = sensorpin3
	
	if (len(sys.argv)==2):
		if (int(sys.argv[1]) == 1):
        		adc = readadc(tmpchanelpin1, SPICLK, SPIMOSI, SPIMISO, SPICS)
			temp = convertTempr(adc)
                	print(temp)	
			GPIO.cleanup()
		elif (int(sys.argv[1]) == 2):
			print(findObstacle(GPIO_OBST_IN))
			GPIO.cleanup()
		elif (int(sys.argv[1]) == 3):
			dist = readUltrasonic(GPIO_TRIGGER,GPIO_ECHO)
			print(dist)
			GPIO.cleanup()
		else:
			print("Please enter values below 3")
	else:
		print("Invalid Arguments")	
 

        # hang out and do nothing for 10 seconds, avoid flooding cosm
        	#time.sleep(2)

