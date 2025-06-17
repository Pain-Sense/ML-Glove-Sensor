# analyze_latency.py
from influxdb_client import InfluxDBClient
from datetime import datetime
import csv
import sys
import os

# InfluxDB configuration
bucket = "bucket1"
org = "UA"
token = "abc"
url = "http://localhost:8086"
measurement = "sensor_data"

# Default device range: 45–65
DEVICE_START = int(sys.argv[1]) if len(sys.argv) > 1 else 45
DEVICE_END = int(sys.argv[2]) if len(sys.argv) > 2 else 65

client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()

# Overall metrics
total_sent = 0
total_received = 0
total_lost = 0
all_latencies = []

def analyze_device(device_id):
    global total_sent, total_received, total_lost, all_latencies

    print(f"\n📡 Querying InfluxDB for deviceId = {device_id}")

    query = f'''
    from(bucket: "{bucket}")
    |> range(start: -2h)
    |> filter(fn: (r) => r["_measurement"] == "{measurement}")
    |> filter(fn: (r) => r["deviceId"] == "{device_id}")
    |> filter(fn: (r) => r["_field"] == "seq")
    |> keep(columns: ["_time", "_value"])
    '''

    tables = query_api.query(query)
    received = {}
    for table in tables:
        for row in table.records:
            seq = int(row.get_value())
            received_time = row.get_time().isoformat()
            received[seq] = received_time

    print(f"📥 Received {len(received)} messages from InfluxDB for device {device_id}")

    csv_file = f"sent_messages_device_{device_id}.csv"
    if not os.path.exists(csv_file):
        print(f"⚠️ CSV file {csv_file} not found. Skipping device {device_id}.")
        return

    sent = {}
    with open(csv_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            sent[int(row["seq"])] = row["sent_timestamp"]

    latencies = []
    lost = []

    for seq in sent:
        if seq in received:
            t_sent = datetime.fromisoformat(sent[seq].replace("Z", "+00:00"))
            t_recv = datetime.fromisoformat(received[seq].replace("Z", "+00:00"))
            latency_sec = (t_recv - t_sent).total_seconds()
            latencies.append(latency_sec)
        else:
            lost.append(seq)

    all_latencies.extend(latencies)
    total_sent += len(sent)
    total_received += len(received)
    total_lost += len(lost)

    if latencies:
        avg_latency = sum(latencies) / len(latencies)
        print(f"✅ Device {device_id} - Avg Latency: {avg_latency:.6f} s")
    else:
        print(f"⚠️ Device {device_id} - No latency data")

    print(f"📦 Sent: {len(sent)} | 📥 Received: {len(received)} | ❌ Lost: {len(lost)}")
    if lost:
        print(f"🔍 First 10 lost seqs: {lost[:10]}")

# Analyze all devices in the range
for device_id in range(DEVICE_START, DEVICE_END + 1):
    analyze_device(str(device_id))

# Print overall stats
print("\n📊 OVERALL STATISTICS ACROSS DEVICES:")
if all_latencies:
    overall_avg_latency = sum(all_latencies) / len(all_latencies)
    print(f"✅ Average Latency: {overall_avg_latency:.6f} s")
else:
    print("⚠️ No latency data to calculate average.")

print(f"📦 Total Sent: {total_sent}")
print(f"📥 Total Received: {total_received}")
print(f"❌ Total Lost: {total_lost}")
print(f"📉 Packet Loss Rate: {100 * total_lost / total_sent:.2f}%")

print("\n✅ Done analyzing all devices.")
