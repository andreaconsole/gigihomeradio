import RPi.GPIO as GPIO
import time
import subprocess
import logging

BUTTON_NEXT = 17  # GPIO17 - Pin 11
BUTTON_PREV = 27  # GPIO27 - Pin 13
LOGFILE = "/home/osmc/gpio_log.txt"

logging.basicConfig(filename=LOGFILE, level=logging.INFO,
                    format='%(asctime)s - %(message)s')

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_NEXT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_PREV, GPIO.IN, pull_up_down=GPIO.PUD_UP)

logging.info("GPIO button script started.")

try:
    while True:
        if GPIO.input(BUTTON_NEXT) == GPIO.LOW:
            logging.info("Next button pressed.")
            subprocess.Popen(["kodi-send", "--action=RunScript(/home/osmc/radio_player.py,next)"])
            time.sleep(0.5)

        if GPIO.input(BUTTON_PREV) == GPIO.LOW:
            logging.info("Previous button pressed.")
            subprocess.Popen(["kodi-send", "--action=RunScript(/home/osmc/radio_player.py,prev)"])
            time.sleep(0.5)

        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
except Exception as e:
    logging.error("Error: %s", str(e))
    GPIO.cleanup()
