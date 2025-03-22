import paho.mqtt.subscribe as subscribe
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '-a', '--addr', type=str, default="test.mosquitto.org",
    help="Endereço do broker MQTT."
)
parser.add_argument(
    '-p', '--port', type=int, default=1883,
    help="Porto do broker MQTT."
)

args = parser.parse_args()


def on_message(client, userdata, message: subscribe.paho.MQTTMessage):
    print(f"topic: {message.topic}\npayload: {message.payload}")

subscribe.callback(
    on_message,
    "case/raw/phys",
    hostname=args.addr, port=args.port
)
