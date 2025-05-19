package org.acme.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.enterprise.context.ApplicationScoped;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.eclipse.microprofile.reactive.messaging.Incoming;
import org.eclipse.microprofile.reactive.messaging.Outgoing;
import org.jboss.logging.Logger;

@ApplicationScoped
public class EventMaker {
   
    private static final Logger LOG = Logger.getLogger(SensorDataEnricher.class);
    private final ObjectMapper objectMapper = new ObjectMapper();
    private final List<String> events = new ArrayList<>();

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

            // Can only create events for one sensor at a time to prevent message overriding
            String message = checkSensors("ecg", ecgNode, ecgStopTime, ecgOn, deviceId, currentTimestamp);
            if (message.equals("")){
                message = checkSensors("bvp", bvpNode, bvpStopTime, bvpOn, deviceId, currentTimestamp);
            }
            if (message.equals("")){
                message = checkSensors("gsr", gsrNode, gsrStopTime, gsrOn, deviceId, currentTimestamp);
            }
            if (message.equals("")){
                message = "no event for device " + deviceId;
            } else {
                events.add(message);
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

    private static String checkSensors(String sensorType, JsonNode node, HashMap<Long, LocalDateTime> stopTimeMap, HashMap<Long, Boolean> onOffMap, Long deviceId, LocalDateTime currentTimestamp){
        String message = "";
        if(hasValidData(node)){
            if (stopTimeMap.get(deviceId) != null){
                stopTimeMap.replace(deviceId, null);
            }
            // If offline sensor comes back online, create event
            if (!onOffMap.get(deviceId)){
                onOffMap.replace(deviceId, true);
                message = sensorType + " sensor online for device " + deviceId;
            }
        } else {
            // If sensor stops store current timestamp
            if (stopTimeMap.get(deviceId) == null){
                stopTimeMap.replace(deviceId, currentTimestamp);
            }
            // If sensor remains stopped for 5 seconds create event
            if (onOffMap.get(deviceId) && stopTimeMap.get(deviceId).isBefore(currentTimestamp.minusSeconds(5))){
                onOffMap.replace(deviceId, false);
                message = sensorType + " sensor offline for device " + deviceId;
            }
        }
        return message;
    }

    public String getEvent(){
        if (events.size() > 0){
            return events.remove(0);
        }
        return "no event";
    }
}
