FROM apache/kafka:latest

ARG STREAM_REACTOR_VERSION="8.1.31"

USER root
RUN     mkdir -p /opt/kafka-connect/connectors \
    &&  mkdir -p /opt/kafka-connect/config \
    &&  wget https://github.com/lensesio/stream-reactor/releases/download/8.1.31/kafka-connect-mqtt-8.1.31.zip -P /tmp \
    &&  unzip /tmp/kafka-connect-mqtt-8.1.31.zip -d /tmp \
    &&  mv /tmp/kafka-connect-mqtt-8.1.31/kafka-connect-mqtt-assembly-8.1.31.jar /opt/kafka-connect/connectors/ \
    &&  rm -f /tmp/kafka-connect-mqtt-8.1.31.zip \
    &&  rm -rf /tmp/kafka-connect-mqtt-8.1.31

COPY start.sh /start.sh
RUN chmod +x /start.sh

ENTRYPOINT ["/start.sh"]

# ENTRYPOINT ["/opt/kafka/bin/connect-standalone.sh"]
# CMD ["/opt/kafka-connect/config/connect-standalone.properties", "/opt/kafka-connect/config/mqtt-source.config"]
