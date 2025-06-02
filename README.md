# gigihomeradio

# Kodi Radio Button Controller

Control Kodi web radio streams using GPIO buttons on a Raspberry Pi.

## 🧩 Requirements

- Raspberry Pi with OSMC or Kodi
- Two pushbuttons
- One USB stick with `stations.txt` file (web radio stream URLs)

## 🎚 Buttons

- **Next station**: GPIO 17 (Pin 11)
- **Previous station**: GPIO 27 (Pin 13)
- Both wired to GND (internal pull-up used)

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

```bash
chmod +x install.sh
./install.sh
```



## Optional: instead of setting a service, you can edit /etc/rc.local to Auto-Start GPIO Script:

```bash
sudo -u osmc python3 /home/osmc/gpio_radio_button.py &
sudo -u osmc python3 /home/osmc/gpio_rotary_volume.py &
```

## and manually copy autoexec.py to /home/osmc/.kodi/userdata/autoexec.py
