import RPi.GPIO as GPIO
import time
import os

# GPIO pin definitions
CLK = 5     # Rotary encoder CLK
DT = 6      # Rotary encoder DT
SW = 13     # Pushbutton for mute


# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(CLK, GPIO.FALLING, callback=clk_callback, bouncetime=200)
GPIO.add_event_detect(SW, GPIO.FALLING, callback=button_callback, bouncetime=300)

# Set initial volume
def set_volume(volume):
    global current_volume
    volume = max(0, min(100, volume))
    current_volume = volume
    os.system(f'kodi-send --action="SetVolume({volume})"')
    print(f"[VOLUME] Set to {volume}%")

# Mute/unmute toggle
def mute_volume(channel):
    global muted, last_volume, current_volume
    if not muted:
        last_volume = current_volume
        set_volume(0)
        muted = True
        print("[MUTE] Muted")
    else:
        set_volume(last_volume)
        muted = False
        print(f"[MUTE] Restored to {last_volume}%")

# Volume adjust based on rotation
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

def adjust_volume(direction):
    global current_volume
    if direction == "up":
        new_volume = current_volume + 2
    else:
        new_volume = current_volume - 2
    set_volume(new_volume)

# Register interrupts
GPIO.add_event_detect(CLK, GPIO.FALLING, callback=clk_callback, bouncetime=200)
GPIO.add_event_detect(SW, GPIO.FALLING, callback=mute_volume, bouncetime=300)

# Initialize
print("[START] Kodi volume control active.")
print("Rotary volume control started. Press Ctrl+C to exit.")
current_volume = 100
last_volume = volume
muted = False
last_clk_state = GPIO.input(CLK)
set_volume(current_volume)


try:
    while True:
        time.sleep(0.1)  # Just wait for GPIO events

except KeyboardInterrupt:
    print("\n[EXIT] Cleaning up GPIO.")
    GPIO.cleanup()

except Exception as e:
    print(f"[ERROR] {e}")
    GPIO.cleanup()
