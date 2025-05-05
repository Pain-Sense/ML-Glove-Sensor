package org.acme.resource;

import jakarta.inject.Inject;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import org.acme.service.DeviceAssignmentRegistry;
import org.acme.service.SensorDataEnricher;
import org.acme.service.DeviceStreamTracker;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Path("/debug")
public class DebugResource {

    @Inject
    DeviceAssignmentRegistry assignmentRegistry;

    @Inject
    SensorDataEnricher enricher;

    @Inject
    DeviceStreamTracker streamTracker;

    public static class AssignmentDTO {
        public Long deviceId;
        public Long experimentId;

        public AssignmentDTO(Long deviceId, Long experimentId) {
            this.deviceId = deviceId;
            this.experimentId = experimentId;
        }
    }

    @GET
    @Path("/device-assignments")
    @Produces(MediaType.APPLICATION_JSON)
    public Response getAssignments() {
        Map<Long, Long> assignments = assignmentRegistry.getAllAssignments();

        List<AssignmentDTO> response = assignments.entrySet().stream()
            .map(e -> new AssignmentDTO(e.getKey(), e.getValue()))
            .collect(Collectors.toList());

        return Response.ok(response).build();
    }

    @GET
    @Path("/devices/active")
    @Produces(MediaType.APPLICATION_JSON)
    public Response getActiveDeviceStatuses() {
        List<Long> activeDeviceIds = streamTracker.getActiveDevices();

        List<Map<String, Object>> response = activeDeviceIds.stream()
            .map(id -> Map.<String, Object>of("id", id, "status", "active"))
            .collect(Collectors.toList());

        return Response.ok(response).build();
    }

    @POST
    @Path("/enrichment")
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    public Response enrichMessage(String rawMessage) {
        try {
            String enriched = enricher.enrich(rawMessage);
            return Response.ok(enriched).build();
        } catch (Exception e) {
            return Response.status(Response.Status.BAD_REQUEST)
                .entity("Failed to enrich: " + e.getMessage())
                .build();
        }
    }
}
