import paho.mqtt.subscribe as subscribe

def on_message(client, userdata, message: subscribe.paho.MQTTMessage):
    print(f"topic: {message.topic}\npayload: {message.payload}")

subscribe.callback(on_message, "case/raw/phys", hostname="test.mosquitto.org", port=1883)
