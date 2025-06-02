package org.acme.resource;

import org.acme.dto.ExperimentDTO;
import org.acme.entity.Experiment;
import org.acme.service.ExperimentService;
import org.acme.service.InfluxService;

import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import jakarta.transaction.Transactional;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Path("/experiments")
@Consumes(MediaType.APPLICATION_JSON)
@Produces(MediaType.APPLICATION_JSON)
public class ExperimentResource {

    @Inject
    ExperimentService experimentService;

    @Inject
    InfluxService influxService;

    @GET
    public List<ExperimentDTO> getAll() {
        return experimentService.listAll().stream().map(this::toDTO).collect(Collectors.toList());
    }

    @GET
    @Path("/notstopped")
    public List<ExperimentDTO> getAllNotStopped() {
        return experimentService.listNotStopped().stream().map(this::toDTO).collect(Collectors.toList());
    }

    @GET
    @Path("/stopped")
    public List<ExperimentDTO> getAllStopped() {
        return experimentService.listStopped().stream().map(this::toDTO).collect(Collectors.toList());
    }

    @GET
    @Path("/{id}")
    public Response getById(@PathParam("id") Long id) {
        Experiment experiment = experimentService.findById(id);
        if (experiment == null) {
            return Response.status(Response.Status.NOT_FOUND).build();
        }
        return Response.ok(toDTO(experiment)).build();
    }

    @POST
    @Transactional
    public Response create(ExperimentDTO dto) {
        try {
            Experiment experiment = experimentService.create(dto);
            return Response.status(Response.Status.CREATED).entity(toDTO(experiment)).build();
        } catch (IllegalArgumentException e) {
            return Response.status(Response.Status.NOT_FOUND).entity(e.getMessage()).build();
        } catch (IllegalStateException e) {
            return Response.status(Response.Status.CONFLICT).entity(e.getMessage()).build();
        }
    }

    @POST
    @Path("/{id}/stop")
    @Transactional
    public Response stopExperiment(@PathParam("id") Long id) {
        Experiment experiment = experimentService.findById(id);
        if (experiment == null) return Response.status(404).build();

        experimentService.stopExperiment(experiment.id);
        return Response.ok().build();
    }

    @GET
    @Path("/{id}/metrics/fields")
    @Produces(MediaType.APPLICATION_JSON)
    public Response getFieldKeys(
        @PathParam("id") Long experimentId
    ) {
        List<String> fieldKeys = influxService.getFieldsForLiveExperiment(experimentId);
        return Response.ok(fieldKeys).build();
    }

    @GET
    @Path("/{id}/metrics/fields/grouped")
    @Produces(MediaType.APPLICATION_JSON)
    public Response getGroupedFieldKeys(
        @PathParam("id") Long experimentId
    ) {
        List<String> grouped = influxService.getFieldsForHistoricalData(experimentId);
        return Response.ok(grouped).build();
    }

    private ExperimentDTO toDTO(Experiment e) {
        ExperimentDTO dto = new ExperimentDTO();
        dto.id = e.id;
        dto.name = e.name;
        dto.notes = e.notes;
        dto.patientId = e.patient != null ? e.patient.id : null;
        dto.deviceId = e.device != null ? e.device.id : null;
        dto.stopped = e.stopped;
        return dto;
    }
}
