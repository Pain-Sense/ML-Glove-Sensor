FROM bitnami/kafka:4.0.0

ARG REACTOR_VERSION="8.1.31"

USER root

RUN apt-get update && apt-get install -y wget unzip && rm -rf /var/lib/apt/lists/*

RUN     mkdir -p /opt/kafka-connect/connectors \
    &&  mkdir -p /opt/kafka-connect/config \
    &&  wget https://github.com/lensesio/stream-reactor/releases/download/$REACTOR_VERSION/kafka-connect-mqtt-$REACTOR_VERSION.zip -P /tmp \
    &&  unzip /tmp/kafka-connect-mqtt-$REACTOR_VERSION.zip -d /tmp \
    &&  mv /tmp/kafka-connect-mqtt-$REACTOR_VERSION/kafka-connect-mqtt-assembly-$REACTOR_VERSION.jar /opt/kafka-connect/connectors/ \
    &&  rm -f /tmp/kafka-connect-mqtt-$REACTOR_VERSION.zip \
    &&  rm -rf /tmp/kafka-connect-mqtt-$REACTOR_VERSION

ENTRYPOINT ["/opt/bitnami/kafka/bin/connect-standalone.sh"]
CMD ["/opt/kafka-connect/config/connect-standalone.properties", "/opt/kafka-connect/config/mqtt-source.config"]
