package org.acme.service;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import io.smallrye.reactive.messaging.annotations.Blocking;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import org.eclipse.microprofile.reactive.messaging.Incoming;

@ApplicationScoped
public class SensorDataConsumer {

    @Inject
    DeviceStatusService statusService;

    @Incoming("SensorData")
    @Blocking
    public void consume(String rawJson) {
        try {
            JsonObject data = JsonParser.parseString(rawJson).getAsJsonObject();

            if (data.has("deviceId")) {
                String deviceId = data.get("deviceId").getAsString();
                statusService.updateLastSeen(deviceId);
            } else {
                System.err.println("Missing deviceId in message: " + rawJson);
            }

        } catch (Exception e) {
            System.err.println("Failed to process message: " + rawJson);
            e.printStackTrace();
        }
    }
}