package org.acme.resource;

import org.acme.dto.ExperimentDTO;
import org.acme.entity.Device;
import org.acme.entity.Experiment;
import org.acme.entity.Patient;
import org.acme.service.DeviceAssignmentRegistry;
import org.acme.service.InfluxService;

import jakarta.inject.Inject;
import jakarta.persistence.EntityManager;
import jakarta.transaction.Transactional;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Path("/experiments")
@Consumes(MediaType.APPLICATION_JSON)
@Produces(MediaType.APPLICATION_JSON)
public class ExperimentResource {

    @Inject
    EntityManager em;

    @Inject
    DeviceAssignmentRegistry assignmentRegistry;

    @Inject
    InfluxService influxService;

    @GET
    public List<ExperimentDTO> getAll() {
        List<Experiment> experiments = em.createQuery("FROM Experiment", Experiment.class).getResultList();
        return experiments.stream().map(this::toDTO).collect(Collectors.toList());
    }

    @GET
    @Path("/{id}")
    public Response getById(@PathParam("id") Long id) {
        Experiment experiment = em.find(Experiment.class, id);
        if (experiment == null) {
            return Response.status(Response.Status.NOT_FOUND).build();
        }
        return Response.ok(toDTO(experiment)).build();
    }

    @POST
    @Transactional
    public Response create(ExperimentDTO dto) {
        Patient patient = em.find(Patient.class, dto.patientId);
        if (patient == null) {
            return Response.status(Response.Status.NOT_FOUND).entity("Patient not found").build();
        }

        Device device = em.find(Device.class, dto.deviceId);
        if (device == null) {
            return Response.status(Response.Status.NOT_FOUND).entity("Device not found").build();
        }

        Experiment experiment = new Experiment();
        experiment.name = dto.name;
        experiment.notes = dto.notes;
        experiment.patient = patient;
        experiment.device = device;

        em.persist(experiment);
        return Response.status(Response.Status.CREATED).entity(toDTO(experiment)).build();
    }

    @POST
    @Path("/{id}/stop")
    @Transactional
    public Response stopExperiment(@PathParam("id") Long id) {
        Experiment experiment = em.find(Experiment.class, id);
        
        if (experiment == null) return Response.status(404).build();

        Device device = experiment.device;
        if (device != null) {
            device.status = "available";
            em.merge(device);
            assignmentRegistry.unassign(device.id);
        }

        return Response.ok().build();
    }

    private ExperimentDTO toDTO(Experiment e) {
        ExperimentDTO dto = new ExperimentDTO();
        dto.id = e.id;
        dto.name = e.name;
        dto.notes = e.notes;
        dto.patientId = e.patient != null ? e.patient.id : null;
        dto.deviceId = e.device != null ? e.device.id : null;
        return dto;
    }

    @GET
    @Path("/{id}/metrics")
    @Produces(MediaType.APPLICATION_JSON)
    public Response getMetrics(
        @PathParam("id") Long experimentId,
        @QueryParam("start") @DefaultValue("-30s") String start,
        @QueryParam("stop") @DefaultValue("now()") String stop
    ) {
        List<Map<String, Object>> results = influxService.queryMetricsInRange(
            experimentId, start, stop
        );
        return Response.ok(results).build();
    }

    @GET
    @Path("/{id}/metrics/aggregate")
    @Produces(MediaType.APPLICATION_JSON)
    public Response getAggregatedMetrics(
        @PathParam("id") Long experimentId,
        @QueryParam("start") @DefaultValue("-5m") String start,
        @QueryParam("stop") @DefaultValue("now()") String stop,
        @QueryParam("window") @DefaultValue("5s") String window,
        @QueryParam("aggregateFn") @DefaultValue("mean") String aggregateFn,
        @QueryParam("field") @DefaultValue("bvp") String field
    ) {
        List<Map<String, Object>> result = influxService.queryAggregatedMetrics(
            experimentId, field, start, stop, window, aggregateFn
        );
        return Response.ok(result).build();
    }
}
