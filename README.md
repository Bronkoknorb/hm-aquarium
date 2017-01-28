# hm-aquarium
Raspberry Pi Aquarium Controller

## Prerequisites

If you haven't installed an Operating System on your Raspberry Pi then follow my instructions here: [Raspberry Pi Installation](https://github.com/oh-balcony/oh-balcony.github.io/wiki/Raspberry-Pi-Installation)

The following additional software packages will be required:

Python 3:

    sudo apt-get install python3
    
Python [requests HTTP library](http://docs.python-requests.org):

    sudo apt-get install python3-requests

Python [gpiozero library](http://gpiozero.readthedocs.io):

    sudo apt-get install python3-gpiozero
    
Python [w1thermsensor library](https://github.com/timofurrer/w1thermsensor/):

    sudo apt-get install python3-w1thermsensor

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

    @reboot sleep 5 && screen -dmS hm-aquarium /home/pi/software/hm-aquarium/main.py

(Replace the full path to the script with the location where you installed it.)

Prerequisite: screen needs to be installed:

    sudo apt-get install screen
