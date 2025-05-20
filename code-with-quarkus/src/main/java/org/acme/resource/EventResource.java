package org.acme.resource;

import org.acme.service.EventMaker;
import org.jboss.resteasy.reactive.RestStreamElementType;

import jakarta.inject.Inject;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.core.MediaType;

@Path("/events")
public class EventResource {

    @Inject
    EventMaker eventMaker;

    @GET
    @RestStreamElementType(MediaType.TEXT_PLAIN)
    public EventMaker.SensorEvent getEvent(){
        return eventMaker.getEvent();
    }
}
