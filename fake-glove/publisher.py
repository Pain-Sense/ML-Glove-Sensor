import paho.mqtt.client as mqtt
import csv
import json

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.connect("test.mosquitto.org", 1883)

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

if __name__ == "__main__":
    pass
