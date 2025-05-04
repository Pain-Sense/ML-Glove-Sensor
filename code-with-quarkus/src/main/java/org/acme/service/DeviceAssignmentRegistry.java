package org.acme.service;

import jakarta.enterprise.context.ApplicationScoped;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@ApplicationScoped
public class DeviceAssignmentRegistry {

    private final Map<Long, Long> activeAssignments = new ConcurrentHashMap<>();

    public void assign(Long deviceId, Long experimentId) {
        activeAssignments.put(deviceId, experimentId);
    }

    public void unassign(Long deviceId) {
        activeAssignments.remove(deviceId);
    }

    public Long getExperimentId(Long deviceId) {
        return activeAssignments.get(deviceId);
    }

    public boolean isAssigned(Long deviceId) {
        return activeAssignments.containsKey(deviceId);
    }
}
