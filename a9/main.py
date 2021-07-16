import RPi.GPIO as GPIO
import time
import requests
import threading

LED_PIN_J = 18
LED_PIN_L = 21
A9_NOTIF_URL = 'http://81.70.151.102:8000/notif'
BLINK_THRESOLD = 300  # 5 mins
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN_J, GPIO.OUT)
GPIO.setup(LED_PIN_L, GPIO.OUT)

# 0 - low, 1 - high, 2 - blink
led_j = 0
led_l = 0

thread_stop = 0


def led_control(pin):
    while True:
        if thread_stop:
            return
        if pin == LED_PIN_J:
            flag = led_j
        else:
            flag = led_l
        try:
            if flag == 0:
                GPIO.output(pin, GPIO.LOW)
                time.sleep(1)
            if flag == 1:
                GPIO.output(pin, GPIO.HIGH)
                time.sleep(1)
            if flag == 2:
                GPIO.output(pin, GPIO.HIGH)
                time.sleep(.5)
                GPIO.output(pin, GPIO.LOW)
                time.sleep(.5)
        except Exception:
            continue


tj = threading.Thread(target=led_control, args=(LED_PIN_J,))
tl = threading.Thread(target=led_control, args=(LED_PIN_L,))
tj.start()
tl.start()

while True:
    try:
        result = requests.get(A9_NOTIF_URL).text.split(',')
        user = result[0]
        timestamp = int(result[1])
        now = int(time.time())
        if user == 'J':
            led_j = 1
            led_l = 0
            if now - timestamp < BLINK_THRESOLD:
                led_j = 2
        if user == 'L':
            led_l = 1
            led_j = 0
            if now - timestamp < BLINK_THRESOLD:
                led_l = 2
        time.sleep(5)
    except KeyboardInterrupt:
        print('Exiting...')
        GPIO.cleanup()
        thread_stop = 1
        tj.join()
        tl.join()
        break
    except Exception:
        continue
