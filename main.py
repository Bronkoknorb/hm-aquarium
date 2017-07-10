#!/usr/bin/env python3

import asyncio
from time import sleep
from pprint import pprint, pformat
from statistics import median
from gpiozero import DigitalOutputDevice
import json
import logging
import sys
import subprocess
import datetime
import websockets
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


class Fan:
    """
    A fan which cools the aquarium switched by a relay.

    :param int pin:
        The GPIO pin (in BCM numbering) that the relay is connected to.

    :param bool active_high:
        Whether the relay is active on high or low. Relays are usually active on low, therefore the default is False.
    """
    def __init__(self, pin: int, active_high: bool = False):
        self._relay = DigitalOutputDevice(pin=pin, active_high=active_high)

    def on(self):
        self._relay.value = True

    def off(self):
        self._relay.value = False

    @property
    def is_on(self) -> bool:
        return self._relay.value

    @property
    def is_off(self):
        return not self.is_on


class AutomaticAndManualSwitch:
    """
    Wraps a switch for automatic and manual control.
    """
    def __init__(self, switch):
        self._switch = switch
        self.is_on = switch.is_on
        self.is_auto_on = None  # initially unknown

    def switch(self, on: bool):
        self.is_on = on
        self._switch.switch(on)

    def switch_auto(self, on: bool):
        if self.is_auto_on != on:
            self.is_auto_on = on
            self.switch(on)


class RemotePowerSocket:
    """
    Allows to control a remote power socket via a 433Mhz sender.
    """
    def __init__(self, name: str, system_code: str, unit_code: str):
        self.name = name
        self.system_code = system_code
        self.unit_code = unit_code
        self.is_on = None  # initially unknown

    def on(self):
        self.switch(True)

    def off(self):
        self.switch(False)

    def switch(self, on: bool):
        logger.info("Turning " + self.name + " " + ("on" if on else "off"))
        on_off_param = "1" if on else "0"
        # let's try it three times and also sleep afterwards a bit to not interfere with other calls
        # (I am probably overly cautious)
        self.send_signal(self.system_code, self.unit_code, on_off_param)
        sleep(0.6)
        self.send_signal(self.system_code, self.unit_code, on_off_param)
        sleep(0.5)
        self.send_signal(self.system_code, self.unit_code, on_off_param)
        sleep(0.5)
        self.is_on = on

    @staticmethod
    def send_signal(system_code: str, unit_code:str, on_off_param: str):
        # this is the send tool from https://github.com/xkonni/raspberry-remote
        # (compiled with 'make send')
        subprocess.call(["/home/pi/software/raspberry-remote/send", system_code, unit_code, on_off_param])


loop = asyncio.get_event_loop()


class Communicator:
    def __init__(self, command_callback):
        self.command_callback = command_callback
        self.websocket = None

    @asyncio.coroutine
    def connect(self):
        delay_reconnect = False
        while True:
            try:
                logger.info("Connecting to: " + server_websocket)
                self.websocket = yield from websockets.connect(server_websocket)
                logger.info("WebSocket connected: " + server_websocket)
                delay_reconnect = False

                try:
                    while True:
                        command = yield from self.websocket.recv()
                        self.command_callback(json.loads(command))
                finally:
                    websocket_local = self.websocket
                    self.websocket = None
                    yield from websocket_local.close()
            except:
                logger.exception("Websocket connection error")
                # if this was already a reconnect, then let's sleep a bit
                if delay_reconnect:
                    yield from asyncio.sleep(3)
                delay_reconnect = True

    @asyncio.coroutine
    def send(self, measurements):
        logger.info("Sending measurements: " + str(measurements))
        if self.websocket is not None:
            try:
                yield from self.websocket.send(json.dumps(measurements))
            except:
                logger.exception("Websocket connection error")
        else:
            logger.error("Cannot send measurements. WebSocket is not connected.")


def float_to_bool(f):
    return f == 1


@asyncio.coroutine
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

    fan = Fan(pin=14)
    fan_turn_on_temperature = 26.0
    fan_turn_off_temperature = 25.5

    sunlight = AutomaticAndManualSwitch(RemotePowerSocket("Sunlight", "01000", "1"))
    moonlight = AutomaticAndManualSwitch(RemotePowerSocket("Moonlight", "01000", "2"))

    def handle_command(commands):
        values = commands["values"];
        logger.info("Received commands: " + pformat(values))
        if "moonlight" in values:
            moonlight.switch(float_to_bool(values["moonlight"]))
        if "sunlight" in values:
            sunlight.switch(float_to_bool(values["sunlight"]))

    communicator = Communicator(handle_command)

    # asynchrounsly connect to websocket
    # All this is written in a way so that even if the server is down main functionality still works
    loop.create_task(communicator.connect())

    def get_water_temperature():
        try:
            return sensor.get_temperature()
        except KeyboardInterrupt:
            raise
        except:
            logger.exception("Error reading water temperature sensor")
            return None

    def control_fan(current_water_temp):
        if current_water_temp is None:
            if fan.is_on:
                logger.error("Water temperature unknown. Turning off fan.")
                fan.off()
        else:
            if fan.is_off:
                if current_water_temp >= fan_turn_on_temperature:
                    logger.info("Turning fan on")
                    fan.on()
            else:  # fan is on
                if current_water_temp <= fan_turn_off_temperature:
                    logger.info("Turning fan off")
                    fan.off()
        return fan.is_on

    while True:
        start_time = loop.time()
        water_temp = get_water_temperature()
        logger.info("Water temperature: " + str(water_temp))
        if water_temp is not None:
            water_temperature_values.append(water_temp)
        room_temp = get_room_temperature()
        if room_temp is not None:
            room_temperature_values.append(room_temp)
        sunlight.switch_auto(sunlight_on_condition())
        moonlight.switch_auto(moonlight_on_condition())
        values_count += 1
        if values_count >= aggregated_measurements_count:
            measurements = {}
            median_water_temperature = None
            # only store values if we have enough to calculate a proper median
            if len(water_temperature_values) == values_count:
                median_water_temperature = median(water_temperature_values)
                measurements["temperature_water"] = median_water_temperature
            if len(room_temperature_values) == values_count:
                median_room_temperature = median(room_temperature_values)
                measurements["temperature_room"] = median_room_temperature
            fan_is_on = control_fan(median_water_temperature)
            measurements["fan"] = 1 if fan_is_on else 0
            measurements["sunlight"] = 1 if sunlight.is_on else 0
            measurements["moonlight"] = 1 if moonlight.is_on else 0
            state = {
                "controllerId": "aqua",
                "values": measurements
            }
            yield from communicator.send(state)
            water_temperature_values = []
            room_temperature_values = []
            values_count = 0
        processing_time = loop.time() - start_time
        sleep_time = max(measure_interval - processing_time, 0)
        yield from asyncio.sleep(sleep_time)


def get_room_temperature():
    try:
        # this is the heatmiser-wifi json tool from https://github.com/thoukydides/heatmiser-wifi
        thermostat_data = subprocess.check_output(["/home/pi/software/heatmiser-wifi/bin/heatmiser_json.pl",
                                                   "-h", "heat", "-p", "1234"])
        thermostat_json = json.loads(thermostat_data.decode(sys.stdout.encoding))
        # pprint(thermostat_json)
        return thermostat_json["heat"]["temperature"]["internal"]
    except KeyboardInterrupt:
        raise
    except:
        logger.exception("Communication error with thermostat")
        return None


def sunlight_on_condition():
    return datetime.time(9, 30) <= datetime.datetime.now().time() <= datetime.time(19, 00)


def moonlight_on_condition():
    return datetime.time(19, 00) <= datetime.datetime.now().time() <= datetime.time(20, 30)
    #return False


if __name__ == "__main__":
    loop.create_task(main())
    loop.run_forever()
