package org.acme.service;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import org.eclipse.microprofile.config.inject.ConfigProperty;
import org.eclipse.microprofile.reactive.messaging.Channel;
import org.eclipse.microprofile.reactive.messaging.Emitter;
import org.acme.service.DeviceStatusService;
import io.quarkus.scheduler.Scheduled;

import java.util.List;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

@ApplicationScoped
public class DeviceWatchdog {

    @Inject
    DeviceStatusService statusService;

    private final Set<String> reportedDevices = ConcurrentHashMap.newKeySet();

    @Scheduled(every = "5s")
    void checkDevices() {
        List<String> offlineDevices = statusService.getOfflineDevices();

        for (String deviceId : offlineDevices) {
            reportedDevices.add(deviceId);
        }

        reportedDevices.removeIf(deviceId -> !offlineDevices.contains(deviceId));
    }

    public Set<String> getOfflineDeviceList() {
        return Set.copyOf(reportedDevices);
    }
}
