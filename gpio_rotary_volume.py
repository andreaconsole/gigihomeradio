import RPi.GPIO as GPIO
import time
import subprocess

CLK = 5     # GPIO5 (Pin 29)
DT = 6      # GPIO6 (Pin 31)
SW = 13     # GPIO13 (Pin 33) – Optional pushbutton

GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)

counter = 0
clkLastState = GPIO.input(CLK)

def adjust_volume(direction):
    action = "VolumeUp" if direction == "up" else "VolumeDown"
    subprocess.call(["kodi-send", "--action=Action({})".format(action)])

try:
    while True:
        clkState = GPIO.input(CLK)
        dtState = GPIO.input(DT)
        if clkState != clkLastState:
            if dtState != clkState:
                adjust_volume("up")
            else:
                adjust_volume("down")
        clkLastState = clkState

        if GPIO.input(SW) == GPIO.LOW:
            subprocess.call(["kodi-send", "--action=Action(Mute)"])
            time.sleep(0.3)

        time.sleep(0.01)

except KeyboardInterrupt:
    GPIO.cleanup()
