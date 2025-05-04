package org.acme.resource;

import org.acme.dto.PatientDTO;
import org.acme.entity.Patient;
import jakarta.inject.Inject;
import jakarta.persistence.EntityManager;
import jakarta.transaction.Transactional;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;

import java.util.List;
import java.util.stream.Collectors;

@Path("/patients")
@Consumes(MediaType.APPLICATION_JSON)
@Produces(MediaType.APPLICATION_JSON)
public class PatientResource {

    @Inject
    EntityManager em;

    @GET
    public List<PatientDTO> getAll() {
        List<Patient> patients = em.createQuery("FROM Patient", Patient.class).getResultList();
        return patients.stream().map(this::toDTO).collect(Collectors.toList());
    }

    @GET
    @Path("/{id}")
    public Response getById(@PathParam("id") Long id) {
        Patient patient = em.find(Patient.class, id);
        if (patient == null) {
            return Response.status(Response.Status.NOT_FOUND).build();
        }
        return Response.ok(toDTO(patient)).build();
    }

    @POST
    @Transactional
    public Response createOrUpdate(PatientDTO dto) {
        Patient patient = em.find(Patient.class, dto.id);
        if (patient == null) {
            patient = new Patient();
            patient.id = dto.id;
        }
        patient.name = dto.name;
        patient.age = dto.age;
        patient.gender = dto.gender;
        patient.health_condition = dto.health_condition;

        em.merge(patient);
        return Response.ok(toDTO(patient)).build();
    }

    private PatientDTO toDTO(Patient p) {
        PatientDTO dto = new PatientDTO();
        dto.id = p.id;
        dto.name = p.name;
        dto.age = p.age;
        dto.gender = p.gender;
        dto.health_condition = p.health_condition;
        return dto;
    }
}