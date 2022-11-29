#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
from subprocess import call

C = [31,33,35,37,21]
L0 = 32
L1 = 36
L2 = 38
L3 = 40
L4 = 29
L5 = 23
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(L0, GPIO.OUT)
GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)
GPIO.setup(L5, GPIO.OUT)
GPIO.setup(C[0], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C[1], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C[2], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C[3], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C[4], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
lastkey = []
key = None
def readLine(line, characters):
    global lastkey
    global key
    ctr = 0
    GPIO.output(line, GPIO.HIGH)
    for x in range(5):
      if(GPIO.input(C[x]) == 1):
        #print(characters[0])
        key = characters[x]
        if key in lastkey:
          rc = call("echo \'hold " + str(key) + "\' | /home/pi/pizero-usb-hid-keyboard/hid-gadget-test /dev/hidg0 keyboard",shell=True)
        else:
          rc = call("echo \'" + str(key) + "\' | /home/pi/pizero-usb-hid-keyboard/hid-gadget-test /dev/hidg0 keyboard",shell=True)
          lastkey.append(key)
    for y in range(5):
      if(GPIO.input(C[y]) == GPIO.LOW):
        rc = call("echo \'quit "+ characters[y] + "\' | /home/pi/pizero-usb-hid-keyboard/hid-gadget-test /dev/hidg0 keyboard",shell=True)
        if characters[y] in lastkey: lastkey.remove(characters[y])
    GPIO.output(line, GPIO.LOW)

try:
    while True:
        readLine(L0, ["tab","esc","left-alt tab","left-shift left-ctrl esc",""])
        readLine(L1, ["q","w","e","r",""])
        readLine(L2, ["a","s","d","f",""])
        readLine(L3, ["left-shift","c","t","v",""])
        readLine(L4, ["left-ctrl","G","enter","space",""])
        readLine(L5, ["","","","","kp-0"])
        #rc = call("./pizero-usb-hid-keyboard/sendkeys ",shell=True)
        time.sleep(0.085)
except KeyboardInterrupt:
    print("\nProgram is stopped")







