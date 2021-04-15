#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import numpy as np
import time

DHTPIN = 17

GPIO.setmode(GPIO.BCM)


def read_dht11_dat():

    GPIO.setup(DHTPIN, GPIO.OUT)
    GPIO.output(DHTPIN, GPIO.HIGH)
    time.sleep(0.05)
    GPIO.output(DHTPIN, GPIO.LOW)
    time.sleep(0.02)
    GPIO.output(DHTPIN, GPIO.HIGH)
    GPIO.setup(DHTPIN, GPIO.IN, GPIO.PUD_UP)

    # DHT11 的 DATA 引脚检测到外部信号有低电平时，等待外部信号低电平结束，
    # 延迟后 DHT11 的 DATA 引脚处于输出状态，DHT11 输出 80 微秒的低电平作为应答信号，
    # 紧接着输出 80 微秒的高电平通知外设准备接收数据
    print("Waiting for DHT11 response")
    while GPIO.input(DHTPIN) == GPIO.LOW:
        continue
    print("DHT11 responds LOW")
    while GPIO.input(DHTPIN) == GPIO.HIGH:
        continue
    print("DHT11 responds HIGH")
    print("Ready to receive data")

    # 开始接收数据
    j = 0  # 计数器
    data = []  # 收到的二进制数据
    kk = []  # 存放每次高电平结束后的k值的列表
    while j < 40:
        k = 0
        while GPIO.input(DHTPIN) == GPIO.LOW:  # 先是 50 微秒的低电平
            print("getting LOW")
            continue

        while GPIO.input(DHTPIN) == GPIO.HIGH:  # 接着是26-28微秒的高电平，或者 70 微秒的高电平
            print("getting HIGH")
            k += 1
            if k > 100:
                break
        kk.append(k)
        if k < 18:
            data.append(0)
        else:
            data.append(1)
        j += 1

    print("sensor is working.")
    print("data: %s" % data)
    print("kk: %s" % kk)

    m = np.logspace(7, 0, 8, base=2, dtype=int)  # logspace()函数用于创建一个于等比数列的数组
    # 即[128 64 32 16 8 4 2 1]，8位二进制数各位的权值
    data_array = np.array(data)  # 将data列表转换为数组
    # dot()函数对于两个一维的数组，计算的是这两个数组对应下标元素的乘积和(数学上称之为内积)
    humidity = m.dot(data_array[0:8])  # 用前8位二进制数据计算湿度的十进制值
    humidity_point = m.dot(data_array[8:16])
    temperature = m.dot(data_array[16:24])
    temperature_point = m.dot(data_array[24:32])
    check = m.dot(data_array[32:40])

    print("data transformed:", humidity, humidity_point,
          temperature, temperature_point, check)

    expected_check = humidity + humidity_point + temperature + temperature_point

    if check == expected_check:
        return humidity, temperature
    else:  # 错误输出错误信息
        return False


def main():
    print("Raspberry Pi DHT11 Test\n")
    time.sleep(1)  # 通电后前一秒状态不稳定，时延一秒
    while True:
        result = read_dht11_dat()
        if result:
            humidity, temperature = result
            print("Humidity: %s %%,  Temperature: %s  ℃\n" %
                  (humidity, temperature))
            time.sleep(1)
        else:
            print("Data error, skip\n")
            time.sleep(1)


def destroy():
    GPIO.cleanup()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        destroy()
