#! /bin/bash


# Setup Development Env -- run this script on the pi after copying the repo to it and 
# following the instructions for setting up the SD card for SSH.
#######################

# Setup raspberrypi SD card for SSH over USB - MANUAL STEPS:
#############################################################
# 1. open sd card root on another system
# 2. append the following to config.txt: 
#	dtoverlay=dwc2 
# 3. put the folling in cmdline.txt after 'rootwait':
#   modules-load=dwc2,g_ether
# 4. create an empty file named 'ssh' in the root directory. 


# rmate for remote editing via sublime -- see https://github.com/randy3k/RemoteSubl

mv rmate /usr/local/bin/
sudo chmod +x /usr/local/bin/rmate

# to connect to the raspberrypi with rmate enabled: ssh -R 52698:localhost:52698 pi@raspberrypi.local