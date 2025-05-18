#! /usr/bin/python3

import argparse
import random
import datetime
import json
from math import floor
import paho.mqtt.client as mqtt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a', '--addr', type=str, default="localhost",
        help="Endereço do broker MQTT."
    )
    parser.add_argument(
        '-p', '--port', type=int, default=1883,
        help="Porto do broker MQTT."
    )
    parser.add_argument(
    '-t', '--topic', type=str, default="sensors",
    help="Tópico de destino."
    )

    args = parser.parse_args()

    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.connect(args.addr, args.port)
    mqttc.loop_start()

    time_start = datetime.datetime.now(datetime.timezone.utc)

    while True:
        time_now = datetime.datetime.now(datetime.timezone.utc)
        dt = floor((time_now - time_start).seconds)
        print(f"dt: {dt}")

        bvp_on = 1
        gsr_on = 1

        if dt % 6 == 0:
            bvp_on = not bvp_on
        if dt % 9 == 0:
            gsr_on = not gsr_on

        data = {
            "timestamp": time_now.isoformat() + "Z",
            "deviceId": 1,
            "bvp": random.random() * gsr_on,
            "gsr": random.random() * gsr_on
        }

        mqttc.publish(args.topic, json.dumps(data))


if __name__ == "__main__":
    main()