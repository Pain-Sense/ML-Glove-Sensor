package org.acme.kafka;

import io.smallrye.reactive.messaging.kafka.Record;
import jakarta.enterprise.context.ApplicationScoped;
import org.eclipse.microprofile.reactive.messaging.Channel;
import org.eclipse.microprofile.reactive.messaging.Emitter;
import org.eclipse.microprofile.reactive.messaging.Incoming;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

import java.io.IOException;
import java.util.Random;
import java.util.UUID;

@ApplicationScoped
public class SensorDataProcessor {

    private final ObjectMapper objectMapper = new ObjectMapper();
    private final Random random = new Random();

    @Channel("ProcessedSensorData")
    Emitter<Record<String, String>> emitter;

    @Incoming("SensorData")
    public void process(String message) {
        try {
            JsonNode jsonNode = objectMapper.readTree(message);
            double bvp = jsonNode.get("bvp").asDouble();
            double gsr = jsonNode.get("gsr").asDouble();

            // Generate a random ECG value
            double ecg = (0.5 + random.nextDouble()) * (bvp + gsr);

            // Add ECG to the message
            ((ObjectNode) jsonNode).put("ecg", ecg);

            // Send the modified message to the new topic
            String modifiedMessage = objectMapper.writeValueAsString(jsonNode);

            // Sleep for 1 second
            Thread.sleep(1000);

            emitter.send(Record.of(UUID.randomUUID().toString(), modifiedMessage));
        } catch (IOException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            // Handle the interrupted exception
            Thread.currentThread().interrupt();
        }
    }
}
