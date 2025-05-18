package org.acme.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;

import java.time.LocalDateTime;
import java.util.HashMap;

import org.eclipse.microprofile.reactive.messaging.Incoming;
import org.eclipse.microprofile.reactive.messaging.Outgoing;
import org.jboss.logging.Logger;

@ApplicationScoped
public class EventMaker {
   
    private static final Logger LOG = Logger.getLogger(SensorDataEnricher.class);
    private final ObjectMapper objectMapper = new ObjectMapper();

    private HashMap<Long,LocalDateTime> ecgStopTime = new HashMap<>();
    private HashMap<Long,LocalDateTime> bvpStopTime = new HashMap<>();
    private HashMap<Long,LocalDateTime> gsrStopTime = new HashMap<>();

    private HashMap<Long, Boolean> ecgOn = new HashMap<>();
    private HashMap<Long, Boolean> bvpOn = new HashMap<>();
    private HashMap<Long, Boolean> gsrOn = new HashMap<>();

    @Incoming("SensorData")
    @Outgoing("Events")
    public String enrich(String rawMessage) {
        try {
            JsonNode root = objectMapper.readTree(rawMessage);

            long deviceId = root.get("deviceId").asLong();

            JsonNode ecgNode = root.get("ecg");
            JsonNode bvpNode = root.get("bvp");
            JsonNode gsrNode = root.get("gsr");

            // Add device to detector
            if (!ecgStopTime.keySet().contains(deviceId)){
                ecgStopTime.put(deviceId, null);
            }
            if (!bvpStopTime.keySet().contains(deviceId)){
                bvpStopTime.put(deviceId, null);
            }
            if (!gsrStopTime.keySet().contains(deviceId)){
                gsrStopTime.put(deviceId, null);
            }
            if (!ecgOn.keySet().contains(deviceId)){
                ecgOn.put(deviceId, false);
            }
            if (!bvpOn.keySet().contains(deviceId)){
                bvpOn.put(deviceId, false);
            }
            if (!gsrOn.keySet().contains(deviceId)){
                gsrOn.put(deviceId, false);
            }

            LocalDateTime currentTimestamp = LocalDateTime.now();

            // Store the current timestamp if a sensor fails
            if (ecgStopTime.get(deviceId) == null && !hasValidData(ecgNode)){
                    ecgStopTime.replace(deviceId, currentTimestamp);
                }
            if (bvpStopTime.get(deviceId) == null && !hasValidData(bvpNode)){
                    bvpStopTime.replace(deviceId, currentTimestamp);
                }
            if (gsrStopTime.get(deviceId) == null && !hasValidData(gsrNode)){
                    gsrStopTime.replace(deviceId, currentTimestamp);
                }

            // If a sensor activates, create an event
            String message;
            if (!ecgOn.get(deviceId) && hasValidData(ecgNode)){
                ecgOn.replace(deviceId, true);
                message = "ecg sensor online for device " + deviceId;
                return objectMapper.writeValueAsString(message);
            }
            if (!bvpOn.get(deviceId) && hasValidData(bvpNode)){
                bvpOn.replace(deviceId, true);
                message = "bvp sensor online for device " + deviceId;
                return objectMapper.writeValueAsString(message);
            }
            if (!gsrOn.get(deviceId) && hasValidData(gsrNode)){
                gsrOn.replace(deviceId, true);
                message = "gsr sensor online for device " + deviceId;
                return objectMapper.writeValueAsString(message);
            }

            // If a sensor remains inactive for long enough, create an event
            if (ecgOn.get(deviceId) && ecgStopTime.get(deviceId).isBefore(currentTimestamp.minusSeconds(5))){
                ecgOn.replace(deviceId, false);
                message = "ecg sensor offline for device " + deviceId;
                return objectMapper.writeValueAsString(message);
            }
            if (bvpOn.get(deviceId) && bvpStopTime.get(deviceId).isBefore(currentTimestamp.minusSeconds(5))){
                bvpOn.replace(deviceId, false);
                message = "bvp sensor offline for device " + deviceId;
                return objectMapper.writeValueAsString(message);
            }
            if (gsrOn.get(deviceId) && gsrStopTime.get(deviceId).isBefore(currentTimestamp.minusSeconds(5))){
                gsrOn.replace(deviceId, false);
                message = "gsr sensor offline for device " + deviceId;
                return objectMapper.writeValueAsString(message);
            }

            message = "no event for device " + deviceId;
            if (bvpNode != null && gsrNode != null && ecgNode !=null && bvpNode.isNumber() && gsrNode.isNumber() && ecgNode.isNumber()) {
                double bvp = bvpNode.asDouble();
                double gsr = gsrNode.asDouble();
                double ecg = ecgNode.asDouble();
                message = "no event for device " + deviceId;
            }
            return objectMapper.writeValueAsString(message);
        } catch (Exception e) {
            LOG.error("Failed to enrich message: " + rawMessage, e);
            return rawMessage; // Return the original message in case of error
        }
    }

    private static boolean hasValidData(JsonNode node){
        return node != null && node.isNumber() && node.asDouble() != 0;
    }
}
