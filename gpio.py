#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import os
import datetime

GPIO.setmode(GPIO.BCM)

#GPIO.setup(18, GPIO.OUT)

CONFIG_DIRECTORY = "/home/pi/hackaton/sensors/"
WIRE_MOUNT_DIRECTORY = "/mnt/1wire/"

class Sensor:
	id = ""
	name = ""
	pinNo = ""
	configs = []

def readTemp(sensor):
	f = open(sensor.strip(), "r")
	temp = float(f.read().strip())
	return temp

def readSensors():
	files = os.listdir(CONFIG_DIRECTORY)
	sensors = [];
	for file in files:
		path = CONFIG_DIRECTORY +  file
		f = open(path, "r")
		configs = f.read().splitlines()
		if configs:
			sensor = Sensor()
			values = configs[0].split(";")
			sensor.id = values[0]
			sensor.name = values[2]
			sensor.pinNo = int(values[1])
			for config in configs:
				sensor.configs.append(config.split(";")[3:])
			sensors.append(sensor)

	return sensors


def initPins(sensors):
	for sensor in sensors:
		GPIO.setup(sensor.pinNo, GPIO.OUT)

def control(sensors):
	for sensor in sensors:
		controlSensor(sensor)

def controlSensor(sensor):
	i = datetime.datetime.now()
	currentTime = i.hour * 60 + i.minute
	useConfig = sensor.configs[-1]
	for config in sensor.configs:
		timeParts = config[2].split(":")
		time = int(timeParts[0]) * 60 + int(timeParts[1])
		if (currentTime > time):
			useConfig = config
		else:
			break

	temp = float(readTemp(WIRE_MOUNT_DIRECTORY + sensor.id + "/temperature12"))

	if temp < float(useConfig[0]):
		GPIO.output(sensor.pinNo, False)
	elif temp > float(useConfig[1]):
		GPIO.output(sensor.pinNo, True)



#temp = float(readTemp("/mnt/1wire/28.365327060000/temperature12"))
#print(temp)
#if temp > 30:
#	GPIO.output(18, False)
#else:
#	GPIO.output(18, True)
#
sensors = readSensors()
initPins(sensors)
control(sensors)
#GPIO.cleanup()
