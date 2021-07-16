import RPi.GPIO as GPIO
import time
import datetime

LED_PIN_J = 18
LED_PIN_L = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN_J, GPIO.OUT)
while 1:
    GPIO.output(LED_PIN_J, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(LED_PIN_J, GPIO.LOW)
    time.sleep(1)

GPIO.cleanup()
