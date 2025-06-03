# GiGiHomeRadio

This is a lightweight plugin for OSMC that turns a Raspberry Pi into a dedicated web radio tuner for use with a hi-fi audio system. On startup, it automatically begins streaming a predefined internet radio station.
The system is designed for simple, hardware-based control:
- A rotary encoder acts as a volume knob, allowing smooth analog-style adjustment.
- Two pushbuttons let the user switch between preset stations stored on a USB stick.

The goal is to replicate the intuitive feel of a traditional radio tuner, while leveraging the flexibility of modern internet radio and Kodi-based media playback.

## 🧩 Requirements

- Raspberry Pi with OSMC or Kodi
- Two pushbuttons for changing the station
- A volume control with pushbutton
- One USB stick with `radio_stations.m3u` file (web radio stream URLs)

## 🎚 Buttons

| Function         | GPIO Pin | Physical Pin        | Connection to                         |
| ---------------- | -------- | ------------------- | ------------------------------------- |
| **Next Station** | GPIO17   | Pin 11              | Pushbutton 1 leg                      |
| **Prev Station** | GPIO27   | Pin 13              | Pushbutton 2 leg                      |
| **Volume CLK**   | GPIO5    | Pin 29              | Rotary encoder CLK pin                |
| **Volume DT**    | GPIO6    | Pin 31              | Rotary encoder DT pin                 |
| **Mute Button**  | GPIO13   | Pin 33              | Pushbutton (optional)                 |
| **GND**          | —        | Pin 14 (or any GND) | Shared ground for all buttons/encoder |

On the Raspberry Pi, pins are numbered physically, from top-left to bottom-right, like this (on Pi 3A+ 40-pin GPIO header) when viewed from above (usb ports facing down, GPIO header on the right):

| left | right |
| ----------: | :---------- |
|  3.3V (1)| (2) 5V|
| GPIO2 (3)| (4) 5V|
| GPIO3 (5)| (6) GND|
| GPIO4 (7)| (8) GPIO14|
|   GND (9)| (10) GPIO15|
|**GPIO17** (11)| (12) GPIO18|
|**GPIO27** (13)| (14) **GND**|
|GPIO22 (15)| (16) GPIO23|
| 3.3V (17)| (18) GPIO24|
|GPIO10 (19)| (20) GND|
| GPIO9 (21)| (22) GPIO25|
|GPIO11 (23)| (24) GPIO8|
|   GND (25)| (26) GPIO7|
| GPIO0 (27)| (28) GPIO1|
| **GPIO5** (29)| (30) GND|
| **GPIO6** (31)| (32) GPIO12|
|**GPIO13** (33)| (34) **GND**|
|GPIO19 (35)| (36) GPIO16|
|GPIO26 (37)| (38) GPIO20|
|   GND (39)| (40) GPIO21|



  
## 📂 File Placement

| File                         | Destination                              |
|------------------------------|------------------------------------------|
| `radio_player.py`            | `/home/osmc/`                            |
| `gpio_radio_button.py`       | `/home/osmc/`                            |
| `gpio_rotary_volume.py`      | `/home/osmc/`                            |
| `radio_player.service`       | `/etc/systemd/system/`                   |
| `gpio_radio_button.service`  | `/etc/systemd/system/`                   |
| `gpio_rotary_volume.service` | `/etc/systemd/system/`                   |
| `radio_stations.m3u`         | `/media/usb/`                            |

## ⚙️ Setup


1. Connect hardware (2 buttons + rotary encoder)
2. Edit `radio_stations.m3u` with your desired radio URLs
3. Run:

```bash
chmod +x install.sh
./install.sh
```

Enjoy!


##  :white_check_mark: Automatically Mount USB on Boot

To make sure Kodi can access your USB stick at startup as media/usb:

1. Plug in the USB stick and run:

   ```bash
   lsblk -o NAME,FSTYPE,SIZE,MOUNTPOINT,UUID
   ```

2. Find your USB partition (e.g. `sda1`) and copy its UUID.

3. Edit `/etc/fstab`:

   ```bash
   sudo nano /etc/fstab
   ```

4. Add this line (replace UUID and filesystem type if needed):

   ```
   UUID=YOUR-UUID-HERE  /media/usb  vfat  defaults,noauto,x-systemd.automount,x-systemd.device-timeout=5  0  0
   ```

5. Create the mount folder:

   ```bash
   sudo mkdir -p /media/usb
   ```

6. Test it:

   ```bash
   sudo mount -a
   ls /media/usb
   ```

If you see the contents of your USB, it will now auto-mount at boot time.

## :x: Possible issues

 ```bash
error: File "/home/osmc/gpio_radio_button.py", line 1, in <module>
    import RPi.GPIO as GPIO
ModuleNotFoundError: No module named 'RPi'
 ```

This error means the RPi.GPIO Python module isn't installed on your system — a common issue on OSMC, since it’s not included by default.

 ```bash
sudo apt-get update
sudo apt-get install python3-rpi.gpio
 ```
This installs the correct GPIO library for Python 3.

