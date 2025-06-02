# gigihomeradio

# Kodi Radio Button Controller

Control Kodi web radio streams using GPIO buttons on a Raspberry Pi.

## 🧩 Requirements

- Raspberry Pi with OSMC or Kodi
- Two pushbuttons for changing the station
- A volume control with pushbutton
- One USB stick with `stations.txt` file (web radio stream URLs)

## 🎚 Buttons

- **Next station**: GPIO 17 (Pin 11)
- **Previous station**: GPIO 27 (Pin 13)
- Both wired to GND (internal pull-up used)
- **Volume control**: CLK on GPIO 5 (Pin 29) and DT on GPIO 6 (Pin 31)
- **Mute control**: GPIO22 (Pin 15) – Optional pushbutton
  
## 📂 File Placement

| File                    | Destination                              |
|-------------------------|------------------------------------------|
| `radio_player.py`       | `/home/osmc/`                            |
| `gpio_radio_button.py`  | `/home/osmc/`                            |
| `gpio_rotary_volume.py` | `/home/osmc/`                            |
| `radio-buttons.service` | `/etc/systemd/system/`                   |
| `rotary-volume.service` | `/etc/systemd/system/`                   |
| `stations.txt`          | `/media/usb/stations.txt`                |
| `autoexec.py`           | `/home/osmc/.kodi/userdata/autoexec.py`  |

## ⚙️ Setup


1. Connect hardware (2 buttons + rotary encoder)
2. Edit `stations.txt` with your desired radio URLs
3. Run:

```bash
chmod +x install.sh
./install.sh
```

Enjoy!


## Optional: instead of setting a service, you can edit /etc/rc.local to Auto-Start GPIO Script:

```bash
sudo -u osmc python3 /home/osmc/gpio_radio_button.py &
sudo -u osmc python3 /home/osmc/gpio_rotary_volume.py &
```

and then manually copy autoexec.py to /home/osmc/.kodi/userdata/autoexec.py


## 📁 Automatically Mount USB on Boot

To make sure Kodi can access your USB stick at startup:

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

