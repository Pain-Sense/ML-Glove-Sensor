package org.acme.kafka;

import jakarta.inject.Inject;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import java.util.HashMap;
import java.util.Map;

@Path("/kafka")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class KafkaResource {

    @Inject
    KafkaProducerService producer;

    @POST
    @Path("/send")
    public Response sendSensorData() {
        producer.sendSensorData();
        return Response.accepted().build();
    }

    @GET
    @Path("/status")
    public Response getStatus() {
        Map<String, String> status = new HashMap<>();
        status.put("status", "Kafka Producer running");
        status.put("broker", "kafka:9092");
        return Response.ok(status).build();
    }

    @POST
    @Path("/test")
    public Response Testing() {
        producer.Testing();
        return Response.accepted().build();
    }
}
