import RPi.GPIO as GPIO
import time
import subprocess
import logging
import os
import wave
import struct
import math
import tempfile

# GPIO pins
BUTTON_NEXT = 17 # GPIO17 - Pin 11
BUTTON_PREV = 27 # GPIO27 - Pin 13
LOGFILE = "/mnt/writestore/gpio_log.txt"

# --- Audio Feedback ---
def play_beep(frequency=8000, duration_ms=100):
    """
    Generates a short beep and plays it using a temporary WAV file.
    This provides precise control over the duration.
    """
    try:
        sample_rate = 44100
        num_samples = int(sample_rate * duration_ms / 1000.0)
        # Generate the sine wave data
        data = []
        for i in range(num_samples):
            # The sine wave equation, scaled for a 16-bit audio sample
            value = int(32767 * math.sin(2.0 * math.pi * frequency * i / sample_rate))
            data.append(struct.pack('<h', value))

        # Create a temporary WAV file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
            wav_file = wave.open(tmp_file.name, 'wb')
            wav_file.setnchannels(1) # Mono
            wav_file.setsampwidth(2) # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(b''.join(data))
            wav_file.close()
            tmp_filename = tmp_file.name
        # Play the WAV file with aplay in the background
        # We redirect stdout and stderr to /dev/null to keep the terminal clean.
        subprocess.Popen(['aplay', tmp_filename], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Clean up the temporary file after a short delay
        time.sleep(duration_ms / 1000.0 + 0.1)
        os.remove(tmp_filename)

    except Exception as e:
        # Log an error if the command fails, so the main script doesn't crash.
        logging.error(f"Failed to play beep: {e}")

# --- GPIO Callbacks ---

def handle_next(channel):
    """
    Callback function for the next button.
    """
    logging.info("Next button pressed.")
    play_beep() # Call the beep function
    subprocess.Popen(["kodi-send", "--action=RunScript(/home/osmc/radio_player.py,next)"])

def handle_prev(channel):
    """
    Callback function for the previous button.
    """
    logging.info("Previous button pressed.")
    play_beep() # Call the beep function
    subprocess.Popen(["kodi-send", "--action=RunScript(/home/osmc/radio_player.py,prev)"])

# --- Setup and Main Loop ---
logging.basicConfig(filename=LOGFILE, level=logging.ERROR,
                    format='%(asctime)s - %(message)s')

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_NEXT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_PREV, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Attach event detection with a generous debounce time
# to prevent multiple triggers from a single button press.
GPIO.add_event_detect(BUTTON_NEXT, GPIO.FALLING, callback=handle_next, bouncetime=300)
GPIO.add_event_detect(BUTTON_PREV, GPIO.FALLING, callback=handle_prev, bouncetime=300)

logging.info("GPIO button script started (interrupt mode).")
print("GPIO button script started.")

try:
    while True:
        time.sleep(1) # Sleep to keep the script alive
except KeyboardInterrupt:
    logging.info("Script manually terminated.")
    print("\n[EXIT] Cleaning up GPIO.")
    GPIO.cleanup()
except Exception as e:
    logging.error("Error: %s", str(e))
    print(f"\n[ERROR] An unexpected error occurred: {str(e)}")
    GPIO.cleanup()
