package org.acme.service;

import jakarta.enterprise.context.ApplicationScoped;

import java.time.Duration;
import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

@ApplicationScoped
public class DeviceStatusService {

    private final Map<String, Instant> lastSeenMap = new ConcurrentHashMap<>();
    private final Duration threshold = Duration.ofSeconds(5); // offline threshold

    public void updateLastSeen(String deviceId) {
        lastSeenMap.put(deviceId, Instant.now());
    }

    public List<String> getOfflineDevices() {
        Instant now = Instant.now();
        return lastSeenMap.entrySet().stream()
            .filter(entry -> Duration.between(entry.getValue(), now).compareTo(threshold) > 0)
            .map(Map.Entry::getKey)
            .collect(Collectors.toList());
    }

    public Map<String, Instant> getLastSeenMap() {
        return lastSeenMap;
    }
}
