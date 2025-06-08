import RPi.GPIO as GPIO
import os
import time

# Rotary encoder pins
CLK = 5     # GPIO5 (Pin 29)
DT = 6      # GPIO6 (Pin 31)
SW = 13     # GPIO13 (Pin 33) – Optional pushbutton

def set_volume(vol):
    global volume
    volume = max(0, min(100, vol))
    os.system(f"amixer set PCM -- {volume}%")
    print(f"Volume: {volume}%")

def adjust_volume(direction):
    global volume
    if direction == "up":
        set_volume(volume + 5)
    elif direction == "down":
        set_volume(volume - 5)

def clk_callback(channel):
    global last_clk_state
    clk_state = GPIO.input(CLK)
    dt_state = GPIO.input(DT)

    if clk_state != last_clk_state:
        if dt_state != clk_state:
            adjust_volume("up")
        else:
            adjust_volume("down")
    last_clk_state = clk_state

def button_callback(channel):
    global volume, last_volume
    if volume > 0:
        last_volume = volume
        set_volume(0)
    else:
        set_volume(last_volume)

GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(CLK, GPIO.FALLING, callback=clk_callback, bouncetime=200)
GPIO.add_event_detect(SW, GPIO.FALLING, callback=button_callback, bouncetime=300)

print("Rotary volume control started. Press Ctrl+C to exit.")
volume = 100
last_volume = volume
set_volume(volume)
last_clk_state = GPIO.input(CLK)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()
