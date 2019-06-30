import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)

# pump ids
STRAWBERRIES = 1 
PHYSALIS  = 2

pumpe_1_gpio = 17
pumpe_2_gpio = 18

def setup():
    gpio.setwarnings(False)
    print("Setup pumps, init them to OFF")
    gpio.setup(pumpe_1_gpio, gpio.OUT)
    gpio.setup(pumpe_2_gpio, gpio.OUT)

def switch_pump(pump_id=1, state="on", switch_time=0):
    if pump_id == 1:
        pump_gpio = pumpe_1_gpio
    elif pump_id == 2:
        pump_gpio = pumpe_2_gpio
    else:
        print("Warning: unknown pump")
        return

    if state == "on":
        print("switch pump {} ON for {} seconds".format(pump_id, switch_time))
        gpio.output(pump_gpio, gpio.LOW)
        time.sleep(switch_time)
        gpio.output(pump_gpio, gpio.HIGH)
    else:
        gpio.output(pump_gpio, gpio.HIGH)


def pump_on(pump=1, ontime=1):
    switch_pump(pump, "on", ontime)

def pump_off(pump=1):
    switch_pump(pump, "off")


# main program

setup()

for i in range(1):
    print("Water the strawberries...")
    pump_on(STRAWBERRIES, 5)
    
    print("Water the physalis...")
    pump_on(PHYSALIS, 5)

    print("sleep 2sec")
    time.sleep(5)

