FROM apache/kafka:latest

ARG STREAM_REACTOR_VERSION="8.1.31"

USER root
RUN     mkdir -p /opt/connectors/config \
    &&  wget https://github.com/lensesio/stream-reactor/releases/download/8.1.31/kafka-connect-mqtt-8.1.31.zip -P /tmp \
    &&  unzip /tmp/kafka-connect-mqtt-8.1.31.zip -d /tmp \
    &&  mv /tmp/kafka-connect-mqtt-8.1.31/kafka-connect-mqtt-assembly-8.1.31.jar /opt/connectors \
    &&  echo plugin.path=/opt/connectors, >> /opt/kafka/config/connect-standalone.properties \
    && rm -f /tmp/kafka-connect-mqtt-8.1.31.zip \
    && rm -rf /tmp/kafka-connect-mqtt-8.1.31
