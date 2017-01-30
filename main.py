#!/usr/bin/env python3

from time import sleep, clock
from pprint import pprint
from statistics import median
import json
import requests
import logging
import sys
import subprocess
from w1thermsensor import W1ThermSensor

logging.basicConfig(format='%(asctime)s %(levelname)s\t%(message)s', level=logging.WARNING)
logger = logging.getLogger('hm-aquarium')
logger.setLevel(logging.INFO)

try:
    from config import *
except ImportError as err:
    print("The configuration file config.py does not exist. Have a look at config.sample.py for reference. (" +
          str(err) + ")")
    exit(1)


def main():
    logger.info("Hm, Aquarium!")

    # time between two measurements (seconds)
    measure_interval = send_measurements_interval / aggregated_measurements_count

    logger.info("Measuring every %s seconds, aggregating %s values and sending them to the server every %s seconds.",
                measure_interval, aggregated_measurements_count, send_measurements_interval)

    values_count = 0
    water_temperature_values = []
    room_temperature_values = []

    sensor = W1ThermSensor()

    def get_water_temperature():
        try:
            return sensor.get_temperature()
        except:
            logger.exception("Error reading water temperature sensor")
            return None

    while True:
        start_time = clock()
        water_temp = get_water_temperature()
        if water_temp is not None:
            water_temperature_values.append(water_temp)
        room_temp = get_room_temperature()
        if room_temp is not None:
            room_temperature_values.append(room_temp)
        values_count += 1
        if values_count >= aggregated_measurements_count:
            # only store values if we have enough to calculate a proper median
            if len(water_temperature_values) == values_count:
                median_water_temperature = median(water_temperature_values)
                send(median_water_temperature, "water")
            if len(room_temperature_values) == values_count:
                median_room_temperature = median(room_temperature_values)
                send(median_room_temperature, "room")
            water_temperature_values = []
            room_temperature_values = []
            values_count = 0
        processing_time = clock() - start_time
        sleep_time = max(measure_interval - processing_time, 0)
        sleep(sleep_time)


def send(temperature, name):
    url = get_service_endpoint("write?db=" + influx_database_name)
    headers = {}
    data = "temp,name=" + name + " value=" + str(temperature)
    logger.info("Sending " + name + " temperature: " + str(temperature))
    try:
        response = requests.post(url, data=data, headers=headers, timeout=5.0)
        response.raise_for_status()
    except:
        logger.exception("Communication error with server")


def get_service_endpoint(endpoint):
    if influx_url.endswith("/"):
        return influx_url + endpoint
    else:
        return influx_url + "/" + endpoint


def get_room_temperature():
    try:
        thermostat_data = subprocess.check_output(["/home/pi/software/heatmiser-wifi/bin/heatmiser_json.pl", "-h", "heat", "-p", "1234"])
        thermostat_json = json.loads(thermostat_data.decode(sys.stdout.encoding))
        # pprint(thermostat_json)
        return thermostat_json["heat"]["temperature"]["internal"]
    except:
        logger.exception("Communication error with thermostat")
        return None

main()
