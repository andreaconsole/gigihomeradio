import RPi.GPIO as GPIO
import time
import os
import requests
import json

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
def get_kodi_volume():
    try:
        response = requests.post(
            "http://localhost:8080/jsonrpc",
            headers={"Content-Type": "application/json"},
            data=json.dumps({
                "jsonrpc": "2.0",
                "method": "Application.GetProperties",
                "params": {"properties": ["volume"]},
                "id": 1
            })
        )
        result = response.json()
        return result["result"]["volume"]
    except Exception as e:
        print(f"[WARN] Could not read volume from Kodi: {e}")
        return 100  # fallback

def set_volume(volume):
    global current_volume
    volume = max(0, min(100, volume))
    if volume != current_volume:
        current_volume = volume
        try:
            requests.post(
                "http://localhost:8080/jsonrpc",
                headers={"Content-Type": "application/json"},
                data=json.dumps({
                    "jsonrpc": "2.0",
                    "method": "Application.SetVolume",
                    "params": {"volume": volume},
                    "id": 1
                })
            )
            print(f"[VOLUME] {volume}%")
        except Exception as e:
            print(f"[ERROR] Failed to set volume: {e}")


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
current_volume = get_kodi_volume()
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
            time.sleep(0.1)
        clk_last = clk_now

        if GPIO.input(SW) == GPIO.LOW:
            mute_toggle()
            time.sleep(0.5)

        time.sleep(0.005)

except KeyboardInterrupt:
    print("\n[EXIT] Cleaning up GPIO.")
    GPIO.cleanup()
