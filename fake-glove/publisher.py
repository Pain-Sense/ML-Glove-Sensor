import paho.mqtt.client as mqtt
import argparse
import csv
import json

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

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.connect(args.addr, args.port)

mqttc.loop_start()

file_raw_phys = open('CASE_snippet_360s/data/raw/physiological/sub1_DAQ.txt')
reader = csv.reader(file_raw_phys, csv.excel_tab)

for row in reader:
    content = {
        "daqtime": row[0],
        "ecg": row[1],
        "bvp": row[2],
        "gsr": row[3],
        "rsp": row[4],
        "skt": row[5],
        "emg_zygo": row[6],
        "emg_coru": row[7],
        "emg_trap": row[8]
    }

    stringified = json.dumps(content)

    mqttc.publish("case/raw/phys", stringified)
