import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.OUT)

def readTemp(sensor):
	f = open(sensor, "r")
	temp = f.read().strip()
	return temp

temp = float(readTemp("/mnt/1wire/28.365327060000/temperature12"))
print(temp)
if temp > 30:
	GPIO.output(18, False)
else:
	GPIO.output(18, True)

#GPIO.cleanup()
