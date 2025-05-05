package org.acme.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.enterprise.context.ApplicationScoped;
import org.eclipse.microprofile.config.inject.ConfigProperty;
import org.eclipse.microprofile.reactive.messaging.Incoming;
import org.jboss.logging.Logger;

import java.time.Duration;
import java.time.Instant;
import java.util.Map;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;

@ApplicationScoped
public class DeviceStreamTracker {

    private static final Logger LOG = Logger.getLogger(DeviceStreamTracker.class);

    private final Map<Long, Instant> deviceActivity = new ConcurrentHashMap<>();

    private final ObjectMapper objectMapper = new ObjectMapper();

    @ConfigProperty(name = "device.activity.timeout", defaultValue = "5")
    int timeoutInSeconds;

    @Incoming("SensorData")
    public void onSensorData(String message) {
        try {
            JsonNode root = objectMapper.readTree(message);
            JsonNode deviceNode = root.get("deviceId");

            if (deviceNode != null && deviceNode.isNumber()) {
                long deviceId = deviceNode.asLong();
                deviceActivity.put(deviceId, Instant.now());
                LOG.debugf("Device %d activity updated", deviceId);
            } else {
                LOG.warn("Received message without valid deviceId: " + message);
            }

        } catch (Exception e) {
            LOG.error("Failed to parse sensor message: " + message, e);
        }
    }

    public boolean isDeviceActive(Long deviceId) {
        Instant lastSeen = deviceActivity.get(deviceId);
        boolean active = lastSeen != null && Instant.now().minus(Duration.ofSeconds(timeoutInSeconds)).isBefore(lastSeen);
        LOG.warnf("Checked device %d → active=%s", deviceId, active);
        return active;
    }

    public List<Long> getActiveDevices() {
        Instant now = Instant.now();
        return deviceActivity.entrySet().stream()
            .filter(e -> now.minus(Duration.ofSeconds(timeoutInSeconds)).isBefore(e.getValue()))
            .map(Map.Entry::getKey)
            .toList();
    }
}