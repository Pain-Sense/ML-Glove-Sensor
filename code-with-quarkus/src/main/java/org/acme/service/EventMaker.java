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
public class EventMaker {
   
    private static final Logger LOG = Logger.getLogger(SensorDataEnricher.class);
    private final ObjectMapper objectMapper = new ObjectMapper();


    @Incoming("SensorData")
    @Outgoing("Events")
    public String enrich(String rawMessage) {
        try {
            JsonNode root = objectMapper.readTree(rawMessage);

            long deviceId = root.get("deviceId").asLong();

            JsonNode ecgNode = root.get("ecg");
            JsonNode bvpNode = root.get("bvp");
            JsonNode gsrNode = root.get("gsr");
            String message = "something wron on device" + deviceId;
            if (bvpNode != null && gsrNode != null && bvpNode.isNumber() && gsrNode.isNumber()) {
                double bvp = bvpNode.asDouble();
                double gsr = gsrNode.asDouble();
                double ecg = ecgNode.asDouble();
                message = "something wron on device testing " + deviceId;
            }
    
            return objectMapper.writeValueAsString(message);
        } catch (Exception e) {
            LOG.error("Failed to enrich message: " + rawMessage, e);
            return rawMessage; // Return the original message in case of error
        }
    }
}
