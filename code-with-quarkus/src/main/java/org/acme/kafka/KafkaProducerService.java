package org.acme.kafka;

import io.smallrye.reactive.messaging.kafka.Record;
import jakarta.enterprise.context.ApplicationScoped;
import org.eclipse.microprofile.reactive.messaging.Channel;
import org.eclipse.microprofile.reactive.messaging.Emitter;

import java.util.Random;
import java.util.UUID;

@ApplicationScoped
public class KafkaProducerService {

    @Channel("messages-out")
    Emitter<Record<String, SensorData>> emitter;
    
    private final Random random = new Random();

    private double randomTemp() {
        return Math.round((-10 + random.nextDouble() * 60) * 10.0) / 10.0;
    }

    private double randomHumidity() {
        return Math.round((random.nextDouble() * 100) * 10.0) / 10.0;
    }

    private double randomWind() {
        return Math.round((random.nextDouble() * 10) * 10.0) / 10.0;
    }

    private double randomSoil() {
        return Math.round((random.nextDouble() * 100) * 10.0) / 10.0;
    }

    public void sendSensorData() {
        for (int i = 0; i < 5; i++) {
        SensorData data = new SensorData(randomTemp(), randomHumidity(), randomWind(), randomSoil());
        emitter.send(Record.of(UUID.randomUUID().toString(), data));
        
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    }

}

class SensorData {
    private double temperature;
    private double humidity;
    private double wind;
    private double soil;

    public SensorData(double temperature, double humidity, double wind, double soil) {
        this.temperature = temperature;
        this.humidity = humidity;
        this.wind = wind;
        this.soil = soil;   
    }

    public double getTemperature() { return temperature; }
    public double getHumidity() { return humidity; }
    public double getWind() { return wind; }
    public double getSoil() { return soil; }

    @Override
    public String toString() {
        return "SensorData{" +
                "temperature=" + temperature +
                ", humidity=" + humidity +
                ", wind=" + wind +
                ", soil=" + soil +
                '}';
    }
}
