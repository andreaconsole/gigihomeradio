#!/bin/bash

echo "Copying scripts to /home/osmc..."
cp radio_player.py gpio_radio_button.py /home/osmc/

chmod +x /home/osmc/*.py

# Install and enable systemd services
echo "Installing systemd services..."
sudo cp gpio_radio_button.service gpio_rotary_volume.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable gpio_radio_button.service gpio_rotary_volume.service
sudo systemctl start gpio_radio_button.service gpio_rotary_volume.service

echo "Done. To edit your stations, modify /media/usb/stations.txt"
