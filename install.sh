#!/bin/bash

echo "Copying scripts to /home/osmc..."
cp radio_player.py gpio_radio_button.py /home/osmc/

echo "Installing Kodi autoexec..."
mkdir -p /home/osmc/.kodi/userdata/
cp autoexec.py /home/osmc/.kodi/userdata/

chmod +x /home/osmc/*.py

echo "Installing systemd service..."
sudo cp radio-buttons.service /etc/systemd/system/
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable radio-buttons.service
sudo systemctl start radio-buttons.service
sudo systemctl enable rotary-volume.service
sudo systemctl start rotary-volume.service

echo "Done. To edit your stations, modify /media/usb/stations.txt"