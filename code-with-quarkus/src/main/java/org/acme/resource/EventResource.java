package org.acme.resource;

import java.util.Map;

import org.acme.service.EventMaker;

import jakarta.inject.Inject;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.PathParam;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;

@Path("/events")
public class EventResource {

    @Inject
    EventMaker eventMaker;

    @GET
    @Produces(MediaType.TEXT_PLAIN)
    public String getEvent(){
        return eventMaker.getEvent();
    }

    @GET
    @Path("/{id}")
    @Produces(MediaType.APPLICATION_JSON)
    public Response getSensorStatus(@PathParam("id") Long id){
        Map<String, Boolean> sensorStatus = eventMaker.getSensorStatus(id);
        if (sensorStatus == null){
            return Response.status(Response.Status.NOT_FOUND).build();
        }
        return Response.ok(sensorStatus).build();
    }
}
