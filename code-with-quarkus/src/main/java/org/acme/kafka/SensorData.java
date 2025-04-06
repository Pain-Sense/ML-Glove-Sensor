package org.acme.kafka;


public class SensorData {
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
