#! /usr/bin/python3

import argparse
import random
import datetime
import time
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
    parser.add_argument(
        '-i', '--deviceId', type=int, default=1,
        help="Número do dispositivo."
    )

    args = parser.parse_args()

    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.connect(args.addr, args.port)
    mqttc.loop_start()

    time_start = datetime.datetime.now(datetime.timezone.utc)

    bvp_on = 1
    gsr_on = 1

    while True:
        time_now = datetime.datetime.now(datetime.timezone.utc)
        dt = (time_now - time_start).seconds

        if dt % 6 == 0:
            bvp_on = not bvp_on
        if dt % 9 == 0:
            gsr_on = not gsr_on

        print(f"bvp_on: {bvp_on}, gsr_on: {gsr_on}, dt: {dt}")

        data = {
            "timestamp": time_now.isoformat() + "Z",
            "deviceId": args.deviceId,
            "bvp": random.random() * bvp_on,
            "gsr": random.random() * gsr_on
        }

        mqttc.publish(args.topic, json.dumps(data))
        time.sleep(1)


if __name__ == "__main__":
    main()
