#!/usr/bin/env python3

from time import sleep, clock
from pprint import pprint
from statistics import median
import json
import requests
import logging
from w1thermsensor import W1ThermSensor

logger = logging.getLogger('hm-aquarium')

try:
    from config import *
except ImportError as err:
    print("The configuration file config.py does not exist. Have a look at config.sample.py for reference. (" +
          str(err) + ")")
    exit(1)


def main():
    print("Hm, Aquarium!")

    # time between two measurements (seconds)
    measure_interval = send_measurements_interval / aggregated_measurements_count

    print("Measuring every", measure_interval, "seconds, aggregating", aggregated_measurements_count,
          "values and sending them to the server every", send_measurements_interval, "seconds.")

    values_count = 0
    temperature_values = []

    sensor = W1ThermSensor()

    while True:
        start_time = clock()
        temperature_values.append(sensor.get_temperature())
        values_count += 1
        if values_count >= aggregated_measurements_count:
            values_count = 0
            median_temperature = median(temperature_values)
            temperature_values = []
            send(median_temperature)
        processing_time = clock() - start_time
        sleep_time = max(measure_interval - processing_time, 0)
        sleep(sleep_time)


def send(temperature):
    url = get_service_endpoint("write?db=" + influx_database_name)
    headers = {}
    data = "temp,name=water value=" + str(temperature)
    print("Logging water temperature: " + str(temperature))
    try:
        response = requests.post(url, data=data, headers=headers, timeout=5.0)
        response.raise_for_status()
    except Exception as e:
        logger.exception("Communication error with server", e)


def get_service_endpoint(endpoint):
    if influx_url.endswith("/"):
        return influx_url + endpoint
    else:
        return influx_url + "/" + endpoint


main()
