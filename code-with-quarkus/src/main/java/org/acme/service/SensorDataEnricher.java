package org.acme.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import org.eclipse.microprofile.reactive.messaging.Incoming;
import org.eclipse.microprofile.reactive.messaging.Outgoing;
import org.jboss.logging.Logger;

@ApplicationScoped
public class SensorDataEnricher {

    private static final Logger LOG = Logger.getLogger(SensorDataEnricher.class);
    private final ObjectMapper objectMapper = new ObjectMapper();

    @Inject
    DeviceAssignmentRegistry assignmentRegistry;

    @Incoming("SensorData")
    @Outgoing("ProcessedSensorData")
    public String enrich(String rawMessage) {
        try {
            JsonNode root = objectMapper.readTree(rawMessage);

            if (!root.has("deviceId") || !root.get("deviceId").isNumber()) {
                LOG.warn("Invalid or missing deviceId in message: " + rawMessage);
                return rawMessage;
            }

            long deviceId = root.get("deviceId").asLong();
            Long experimentId = assignmentRegistry.getExperimentId(deviceId);

            ObjectNode enriched = (ObjectNode) root;

            if (experimentId != null) {
                enriched.put("experimentId", experimentId);
                LOG.debugf("Enriched message from device %d with experiment %d", deviceId, experimentId);
            } else {
                LOG.debugf("No active experiment for device %d. Skipping enrichment.", deviceId);
            }

            return objectMapper.writeValueAsString(enriched);
        } catch (Exception e) {
            LOG.error("Failed to enrich message: " + rawMessage, e);
            return rawMessage; // Return the original message in case of error
        }
    }

    @Incoming("hrData")
    @Outgoing("EnrichedHrData")
    public String enrichHrData(String rawMessage) {
        try {
            JsonNode root = objectMapper.readTree(rawMessage);

            if (!root.has("deviceId") || !root.get("deviceId").isNumber()) {
                LOG.warn("Invalid or missing deviceId in hrData message: " + rawMessage);
                return rawMessage;
            }

            long deviceId = root.get("deviceId").asLong();
            Long experimentId = assignmentRegistry.getExperimentId(deviceId);

            ObjectNode enriched = (ObjectNode) root;

            if (experimentId != null) {
                enriched.put("experimentId", experimentId);
                LOG.debugf("Enriched HR data from device %d with experiment %d", deviceId, experimentId);
            } else {
                LOG.debugf("No active experiment for device %d in hrData enrichment.", deviceId);
            }

            return objectMapper.writeValueAsString(enriched);

        } catch (Exception e) {
            LOG.error("Failed to enrich hrData message: " + rawMessage, e);
            return rawMessage;
        }
    }
}
