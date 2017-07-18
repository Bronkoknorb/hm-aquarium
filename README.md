# hm-aquarium
Raspberry Pi Aquarium Controller

## Prerequisites

If you haven't installed an Operating System on your Raspberry Pi then follow my instructions here: [Raspberry Pi Installation](https://github.com/oh-balcony/oh-balcony.github.io/wiki/Raspberry-Pi-Installation)

The following additional software packages will be required:

Python 3:

    sudo apt-get install python3

PIP for installing Python libraries:

    sudo apt-get install python3-pip

Python [gpiozero library](http://gpiozero.readthedocs.io):

    sudo apt-get install python3-gpiozero

Python [w1thermsensor library](https://github.com/timofurrer/w1thermsensor/):

    sudo apt-get install python3-w1thermsensor

Python [websockets library](https://websockets.readthedocs.io/):

    sudo pip3 install websockets
    
Python [PySisPM library](https://github.com/xypron/pysispm):

    sudo pip3 install pyusb
    sudo pip3 install pysispm
    
Ensure that your user has rights to control the SIS-PM power sockets (Gembird EG-PM2):

```
sudo groupadd sispmctl
sudo usermod -a -G sispmctl pi

sudo bash -c "cat > /lib/udev/rules.d/60-sispmctl.rules" <<EOL
SUBSYSTEM=="usb", ATTR{idVendor}=="04b4", ATTR{idProduct}=="fd10", GROUP="sispmctl", MODE="660"
SUBSYSTEM=="usb", ATTR{idVendor}=="04b4", ATTR{idProduct}=="fd11", GROUP="sispmctl", MODE="660"
SUBSYSTEM=="usb", ATTR{idVendor}=="04b4", ATTR{idProduct}=="fd12", GROUP="sispmctl", MODE="660"
SUBSYSTEM=="usb", ATTR{idVendor}=="04b4", ATTR{idProduct}=="fd13", GROUP="sispmctl", MODE="660"
EOL

sudo udevadm control --reload-rules
```

## Usage

Clone the git repository:

    git clone https://github.com/Bronkoknorb/hm-aquarium.git

### Configuration

Copy the file `config.sample.py` to `config.py` and adapt it to your needs.

### Starting

Run:

    ./main.py

### Autostart

To automatically start the script when the Raspberry Pi is rebooted, execute:

    crontab -e

... and then add the following line to the crontab:

    @reboot sleep 5 && /home/pi/software/hm-aquarium/start.sh

(Replace the path of the script with the location where you installed it.)

### Logrotate

To avoid that the log file grows infinite create the following logrotate rule as `/etc/logrotate.d/hm-aquarium`:

```
/home/pi/software/hm-aquarium/hm-aquarium.log {
   weekly
   rotate 4
   compress
   missingok
   copytruncate
}
```
(Replace the path of the logfile with the location where you installed it.)
