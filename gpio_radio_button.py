import RPi.GPIO as GPIO
import time
import subprocess
import logging

BUTTON_NEXT = 17  # GPIO17 - Pin 11
BUTTON_PREV = 27  # GPIO27 - Pin 13
LOGFILE = "/mnt/writestore/gpio_log.txt"

logging.basicConfig(filename=LOGFILE, level=logging.INFO,
                    format='%(asctime)s - %(message)s')

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_NEXT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_PREV, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def handle_next(channel):
    logging.info("Next button pressed.")
    subprocess.Popen(["kodi-send", "--action=RunScript(/home/osmc/radio_player.py,next)"])

def handle_prev(channel):
    logging.info("Previous button pressed.")
    subprocess.Popen(["kodi-send", "--action=RunScript(/home/osmc/radio_player.py,prev)"])

# Attach event detection with debounce
GPIO.add_event_detect(BUTTON_NEXT, GPIO.FALLING, callback=handle_next, bouncetime=300)
GPIO.add_event_detect(BUTTON_PREV, GPIO.FALLING, callback=handle_prev, bouncetime=300)

logging.info("GPIO button script started (interrupt mode).")

try:
    while True:
        time.sleep(1)  # Sleep to keep the script alive
except KeyboardInterrupt:
    GPIO.cleanup()
except Exception as e:
    logging.error("Error: %s", str(e))
    GPIO.cleanup()

