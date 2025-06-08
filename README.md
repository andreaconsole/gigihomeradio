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
| `radio_stations.m3u`         | `/mnt/writestore`                        |

## ⚙️ Setup


1. Connect hardware (2 buttons + rotary encoder)
2. Edit `radio_stations.m3u` with your desired radio URLs
3. Run:

```bash
chmod +x install.sh
./install.sh
```

Enjoy!


# OSMC Read-Only Root & Writable Partition Setup

This document describes how to:

- Create a writable partition (`writestore`) for Kodi data and other write needs.
- Make the root filesystem read-only for stability and SD card protection.
- Configure Kodi to work with the writable partition.
- Use tmpfs for writable temporary directories.
- Control root mounting via kernel command line or `/etc/fstab`.

---

## Partition Setup

1. Create a third partition (`/dev/mmcblk0p3`) formatted as `ext4` for writable data:

```bash
sudo parted /dev/mmcblk0 mkpart primary ext4 100% 100%  # Example, adjust sizes accordingly
sudo mkfs.ext4 /dev/mmcblk0p3
sudo mkdir /mnt/writestore
sudo mount /dev/mmcblk0p3 /mnt/writestore
```

2. Add to `/etc/fstab` for automatic mounting:

```
/dev/mmcblk0p3 /mnt/writestore ext4 defaults,noatime,nofail,x-systemd.device-timeout=5 0 2
```

---

## Root Filesystem Read-Only Setup

### Mounting root (`/dev/mmcblk0p2`) read-only

You have two ways to make the root filesystem mount read-only:

1. **Via `/etc/fstab`**

   Add or keep this line in `/etc/fstab`:

   ```
   /dev/mmcblk0p2  /    ext4  ro,noatime  0 1
   ```

   - This remounts the root filesystem as read-only during boot.
   - May cause a slightly slower boot time.
   - Useful if you want explicit control in fstab.

2. **Via kernel command line (`/boot/cmdline.txt`)**

   If you comment out the root entry in `/etc/fstab`, the kernel mounts the root filesystem at boot using `/boot/cmdline.txt`.

   You must include the `ro` option there, for example:

   ```
   root=/dev/mmcblk0p2 ro rootfstype=ext4 rootwait quiet osmcdev=rbp2
   ```

   - The `ro` option tells the kernel to mount root as read-only initially.
   - This is the recommended way if you rely on initramfs or want faster boot.
   - Make sure `/etc/fstab` does **not** remount root read-write afterward.

---

### Verifying the root filesystem mode

After reboot, check the mount status:

```bash
mount | grep ' on / '
```

Look for `(ro,...)` in the mount options, confirming read-only root.

---

## Tmpfs for Writable Temporary Directories

To minimize writes to the SD card, mount these tmpfs filesystems by adding to `/etc/fstab`:

```
tmpfs /tmp tmpfs defaults,noatime,nosuid,nodev,size=100m 0 0
tmpfs /var/tmp tmpfs defaults,noatime,nosuid,nodev,size=50m 0 0
tmpfs /var/log tmpfs defaults,noatime,nosuid,nodev,mode=0755,size=20m 0 0
tmpfs /run tmpfs defaults,noatime,nosuid,nodev,mode=0755,size=10m 0 0
```

---

## Configuring Kodi for Read-Only Root

1. Move `.kodi` directory to the writable partition:

```bash
sudo systemctl stop mediacenter
sudo mv /home/osmc/.kodi /mnt/writestore/kodi
sudo ln -s /mnt/writestore/kodi /home/osmc/.kodi
sudo chown -h osmc:osmc /home/osmc/.kodi
```

2. Make sure `/mnt/writestore` is mounted before Kodi starts.

3. Adjust any permissions if needed.

---

## Example `/etc/fstab`

```fstab
/dev/mmcblk0p1  /boot    vfat     defaults,noatime,noauto,x-systemd.automount    0   0
# rootfs is not mounted in fstab as we do it via initramfs. Uncomment for remount (slower boot)
#/dev/mmcblk0p2  /    ext4      ro,noatime    0   1
/dev/mmcblk0p3 /mnt/writestore ext4 defaults,noatime,nofail,x-systemd.device-timeout=5 0 2
tmpfs /tmp tmpfs defaults,noatime,nosuid,nodev,size=100m 0 0
tmpfs /var/tmp tmpfs defaults,noatime,nosuid,nodev,size=50m 0 0
tmpfs /var/log tmpfs defaults,noatime,nosuid,nodev,mode=0755,size=20m 0 0
tmpfs /run tmpfs defaults,noatime,nosuid,nodev,mode=0755,size=10m 0 0
```

---

## Troubleshooting

- If Kodi fails to start, check for permission errors or missing write access to `/home/osmc/.kodi`.
- Make sure `/mnt/writestore` is mounted and writable.
- Verify that tmpfs mounts exist:

```bash
mount | grep tmpfs
```

- Use `dmesg` and Kodi logs to troubleshoot startup issues.

---

## Summary

- Use either `/etc/fstab` or `/boot/cmdline.txt` to set root read-only, **not both**.
- Create a dedicated writable partition for Kodi and other user data.
- Use tmpfs to reduce SD card wear from logs and temporary files.
- Symlink Kodi config to writable partition to maintain functionality.

---

This setup improves system stability and SD card lifespan for OSMC on Raspberry Pi.




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

