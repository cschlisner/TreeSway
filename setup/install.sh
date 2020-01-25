
# Setup connection to UCB Guest
echo 'ctrl_interface=DIR=/var/run/wpa/_supplicant GROUP=netdev\nupdate_config=1\n\nnetwork={\n\tssid="UCB Guest"\n\tkey_mgmt=NONE\n}' > /etc/wpa_supplicant/wpa_supplicant.conf
wpa_cli -i wlan0 reconfigure

python3 ../python/modules/run-log.py

