package org.acme.resource;

import org.acme.dto.ExperimentDTO;
import org.acme.entity.Device;
import org.acme.entity.Experiment;
import org.acme.entity.Patient;

import jakarta.inject.Inject;
import jakarta.persistence.EntityManager;
import jakarta.transaction.Transactional;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;

import java.util.List;
import java.util.stream.Collectors;

@Path("/experiments")
@Consumes(MediaType.APPLICATION_JSON)
@Produces(MediaType.APPLICATION_JSON)
public class ExperimentResource {

    @Inject
    EntityManager em;

    @GET
    public List<ExperimentDTO> getAll() {
        List<Experiment> experiments = em.createQuery("FROM Experiment", Experiment.class).getResultList();
        return experiments.stream().map(this::toDTO).collect(Collectors.toList());
    }

    @GET
    @Path("/{id}")
    public Response getById(@PathParam("id") String id) {
        Experiment experiment = em.find(Experiment.class, id);
        if (experiment == null) {
            return Response.status(Response.Status.NOT_FOUND).build();
        }
        return Response.ok(toDTO(experiment)).build();
    }

    @POST
    @Transactional
    public Response create(ExperimentDTO dto) {
        if (dto.id == null || dto.id.isBlank()) {
            return Response.status(Response.Status.BAD_REQUEST).entity("Experiment ID is required").build();
        }

        Patient patient = em.find(Patient.class, dto.patientId);
        if (patient == null) {
            return Response.status(Response.Status.NOT_FOUND).entity("Patient not found").build();
        }

        Device device = em.find(Device.class, dto.deviceId);
        if (device == null) {
            return Response.status(Response.Status.NOT_FOUND).entity("Device not found").build();
        }

        Experiment experiment = new Experiment();
        experiment.id = dto.id;
        experiment.name = dto.name;
        experiment.notes = dto.notes;
        experiment.patient = patient;
        experiment.device = device;

        em.persist(experiment);
        return Response.status(Response.Status.CREATED).entity(toDTO(experiment)).build();
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
}
