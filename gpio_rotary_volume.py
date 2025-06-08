import RPi.GPIO as GPIO
import time
import os

# GPIO pins
CLK = 5     # Rotary encoder pin 1
DT = 6      # Rotary encoder pin 2
SW = 13     # Pushbutton for mute

# Volume state
current_volume = 100
last_volume = current_volume
muted = False

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# --- Volume Control ---
def set_volume(volume):
    global current_volume
    volume = max(0, min(100, volume))
    if volume != current_volume:
        current_volume = volume
        os.system(f'kodi-send --action="SetVolume({volume})"')
        print(f"[VOLUME] {volume}%")

def mute_toggle():
    global muted, last_volume, current_volume
    if not muted:
        last_volume = current_volume
        set_volume(0)
        muted = True
        print("[MUTE] Muted")
    else:
        set_volume(last_volume)
        muted = False
        print(f"[MUTE] Unmuted → {last_volume}%")

# --- Polling Loop ---
print("[START] Volume control active.")
set_volume(current_volume)

try:
    clk_last = GPIO.input(CLK)

    while True:
        clk_now = GPIO.input(CLK)
        if clk_now != clk_last and clk_now == 0:
            dt_now = GPIO.input(DT)
            if dt_now == 1:
                set_volume(current_volume + 2)
            else:
                set_volume(current_volume - 2)
            time.sleep(0.05)
        clk_last = clk_now

        if GPIO.input(SW) == GPIO.LOW:
            mute_toggle()
            time.sleep(0.5)

        time.sleep(0.005)

except KeyboardInterrupt:
    print("\n[EXIT] Cleaning up GPIO.")
    GPIO.cleanup()
