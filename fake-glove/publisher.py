import paho.mqtt.client as mqtt
import argparse
import csv
import json

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
    '-i', '--subject', type=int, default=1, choices=range(1, 6),
    help='Número do participante.'
)

args = parser.parse_args()

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.connect(args.addr, args.port)
mqttc.loop_start()

f = open(
    f'../Data/sub_{args.subject}.csv'
)
reader = csv.reader(f)

for row in reader:
    content = {
        "daqtime": row[0],
        # "ecg": row[1],
        "bvp": row[2],
        "gsr": row[3],
        # "rsp": row[4],
        # "skt": row[5],
        # "emg_zygo": row[6],
        # "emg_coru": row[7],
        # "emg_trap": row[8]
    }

    stringified = json.dumps(content)
    mqttc.publish("sensors", stringified)
