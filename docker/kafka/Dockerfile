FROM apache/kafka:4.0.0

USER root

RUN wget https://github.com/lensesio/stream-reactor/releases/download/8.1.31/kafka-connect-mqtt-8.1.31.zip -P ~

RUN unzip ~/kafka-connect-mqtt-8.1.31.zip -d ~/

RUN mkdir /opt/connectors
RUN mv ~/kafka-connect-mqtt-8.1.31/kafka-connect-mqtt-assembly-8.1.31.jar /opt/connectors

RUN echo plugin.path=/opt/opt/connectors, >> /opt/kafka/config/connect-standalone.properties

EXPOSE 9092
