import xbmc
import os
import time
import logging
import sys

STATION_FILE = "/mnt/writestore/stations.m3u"
CURRENT_INDEX_FILE = "/mnt/writestore/.current_station"
LOGFILE = "/mnt/writestore/radio_log.txt"

logging.basicConfig(filename=LOGFILE, level=logging.INFO,
                    format='%(asctime)s - %(message)s')

def get_station_list():
    try:
        with open(STATION_FILE, "r") as f:
            stations = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]
        logging.info(f"Station list loaded: {stations}")
        return stations
    except Exception as e:
        logging.error("Error reading station list: %s", str(e))
        return []

def get_current_index():
    try:
        idx = int(open(CURRENT_INDEX_FILE).read().strip())
        stations = get_station_list()
        if not stations:
            return 0
        if idx < 0 or idx >= len(stations):
            return 0
        return idx
    except:
        return 0

def save_current_index(index):
    try:
        with open(CURRENT_INDEX_FILE, "w") as f:
            f.write(str(index))
        logging.info(f"Saved current station index: {index}")
    except Exception as e:
        logging.error(f"Failed to save current station index: {e}")


def play_current_station():
    stations = get_station_list()
    if not stations:
        logging.error("No stations found.")
        return

    idx = get_current_index() % len(stations)
    stream_url = stations[idx]
    xbmc.executebuiltin(f'PlayMedia("{stream_url}")')
    save_current_index(idx)
    logging.info("Playing current station: %s", stream_url)

def play_next_station():
    stations = get_station_list()
    if not stations:
        return

    idx = (get_current_index() + 1) % len(stations)
    save_current_index(idx)
    xbmc.executebuiltin(f'PlayMedia("{stations[idx]}")')
    logging.info("Switched to next station: %s", stations[idx])

def play_previous_station():
    stations = get_station_list()
    if not stations:
        return

    idx = (get_current_index() - 1 + len(stations)) % len(stations)
    save_current_index(idx)
    xbmc.executebuiltin(f'PlayMedia("{stations[idx]}")')
    logging.info("Switched to previous station: %s", stations[idx])

if __name__ == '__main__':
    time.sleep(5)  # Wait for USB/network
    if len(sys.argv) > 1:
        if sys.argv[1] == "next":
            play_next_station()
        elif sys.argv[1] == "prev":
            play_previous_station()
    else:
        play_current_station()
