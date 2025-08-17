# IMPORTANT EDIT USER:PASSWORD AND PORT!!!
import RPi.GPIO as GPIO
import time
import os
import json
import subprocess # Use subprocess for better control and to capture output

# GPIO pins
CLK = 5 #Rotary encoder pin 1
DT = 6 # Rotary encoder pin 2
SW = 13 # Pushbutton for mute

# Volume state
current_volume = 100 # This will be updated with the value from Kodi
last_volume = current_volume
muted = False

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# --- Kodi API Communication ---
def get_kodi_volume():
    """
    Retrieves the current volume from Kodi using its JSON-RPC API.
    Returns the volume as an integer, or 100 if the call fails.
    """
    try:
        # Construct the JSON-RPC command to get the 'volume' property
        json_cmd = '{"jsonrpc": "2.0", "method": "Application.GetProperties", "params": {"properties": ["volume"]}, "id": 1}'
        # Use subprocess to run curl and capture its output
        result = subprocess.run(
            # IMPORTANT EDIT "-U USER:PASSWORD" AND PORT!!!
            ['curl', '-s', '-u', 'user:password', '-X', 'POST', '-H', 'Content-Type: application/json', '-d', json_cmd, 'http://localhost:8080/jsonrpc'],
            capture_output=True,
            text=True,
            check=True
        )
        # Parse the JSON response
        response_json = json.loads(result.stdout)
        # Extract the volume from the response
        volume = response_json.get('result', {}).get('volume', 100)
        return int(volume)
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"[ERROR] Could not connect to Kodi or parse response: {e}")
        print("[INFO] Defaulting to initial volume of 100.")
        return 100

# --- Volume Control ---
def set_volume(volume):
    global current_volume
    volume = max(0, min(100, volume))
    # Update the volume in Kodi even if it's the same, to ensure sync
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
        print(f"[MUTE] Unmuted from {last_volume}%")

# --- Polling Loop ---
print("[START] Volume control active.")
# Get the initial volume from Kodi at startup
current_volume = get_kodi_volume()
set_volume(current_volume) # This call now synchronizes the script's state with Kodi's

# Initialize a timer for periodic volume checks
last_sync_time = time.time()
SYNC_INTERVAL_SECONDS = 60 # Check every minute

try:
    clk_last = GPIO.input(CLK)

    while True:
        # Check if it's time to sync with Kodi
        if time.time() - last_sync_time >= SYNC_INTERVAL_SECONDS:
            kodi_volume = get_kodi_volume()
            set_volume(kodi_volume)
            last_sync_time = time.time()
            print("[SYNC] Aligned with Kodi volume.")

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
