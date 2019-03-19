# TreeSway

## Setup from scratch for Development

*these steps have already been completed for the two pis we have*


### Raspberry Pi SD card Setup for SSH over USB 


1. open sd card root on another system
2. append the following to config.txt: 

	`dtoverlay=dwc2`

3. put the folling in cmdline.txt after `rootwait`:
	
	`modules-load=dwc2,g_ether`

4. create an empty file named 'ssh' in the root directory. 

### Setup bluetooh connection 

from https://hacks.mozilla.org/2017/02/headless-raspberry-pi-configuration-over-bluetooth/

1. run the following commands (on the pi (somehow))

```
mv setup/btserial.sh /home/pi/
sudo chmod +755 /home/pi/btserial.sh
```

2. add `sudo /home/pi/btserial.sh &` to /etc/rc.local

3. reboot pi


### Installing rmate for remote editing via sublime -- see https://github.com/randy3k/RemoteSubl

1. Run the following commands from this directory after copying this repo to a raspberry pi

```
mv setup/rmate /usr/local/bin/
sudo chmod +x /usr/local/bin/rmate
```

2. Install sublime text on development machine

3. Install the RemoteSubl package 

4. Run `rmate FILE` on the raspberry pi to edit the file in sublime text on the dev machine. Will automatically save to the pi. 

## Connecting to the Raspberry Pi remotely (only confirmed working on MacOs/Unix -- might work on WSL)

### via ssh 

* (with rmate enabled) `ssh -R 52698:localhost:52698 pi@<HOSTNAME>.local`
* (without rmate port) `ssh pi@<HOSTNAME>.local`

`<HOSTNAME>` is "raspberrypi0" for the reciever raspberry pi and "raspberrypi1" for the sender. 

### via Bluetooth
1. Boot the pi
2. turn on bluetooth
3. `ls /dev/cu.*` to look for the pi
4. `screen /dev/cu.raspberrypi-SerialPort 115200`

## Other useful things

Tmux -- https://www.hamvocke.com/blog/a-quick-and-easy-guide-to-tmux/ (installed on linux systems, available on homebrew for macos)
