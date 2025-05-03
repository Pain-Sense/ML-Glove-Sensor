#!/bin/bash
# Start Kafka in the background
/etc/kafka/docker/run &

# Start Kafka Connect
/opt/kafka/bin/connect-standalone.sh /opt/kafka-connect/config/connect-standalone.properties /opt/kafka-connect/config/mqtt-source.config
