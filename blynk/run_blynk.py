# -*- coding: utf-8 -*-
"""
References:
- https://github.com/blynkkk/lib-python/blob/master/examples/raspberry/01_weather_station_pi3b.py
"""
import os
import RPi.GPIO as GPIO
import dht11
import blynklib


BLYNK_AUTH = os.getenv('BLYNK_AUTH_TOKEN')
blynk = blynklib.Blynk(BLYNK_AUTH, heartbeat=15)

T_COLOR = '#f5b041'
H_COLOR = '#85c1e9'
ERR_COLOR = '#444444'

T_VPIN = 7
H_VPIN = 8
GPIO_DHT11_PIN = 17

# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)


@blynk.handle_event('read V{}'.format(T_VPIN))
def read_handler(vpin):
    dht11_sensor = dht11.DHT11(pin=GPIO_DHT11_PIN)
    result = dht11_sensor.read()
    temperature = result.temperature
    humidity = result.humidity
    # check that values are not False (mean not None)
    if all([humidity, temperature]):
        print('temperature={} humidity={}'.format(temperature, humidity))
        blynk.set_property(T_VPIN, 'color', T_COLOR)
        blynk.set_property(H_VPIN, 'color', H_COLOR)
        blynk.virtual_write(T_VPIN, temperature)
        blynk.virtual_write(H_VPIN, humidity)
    else:
        print('[ERROR] reading DHT11 sensor data')
        # show aka 'disabled' that mean we errors on data read
        blynk.set_property(T_VPIN, 'color', ERR_COLOR)
        blynk.set_property(H_VPIN, 'color', ERR_COLOR)


###########################################################
# infinite loop that waits for event
###########################################################
while True:
    blynk.run()