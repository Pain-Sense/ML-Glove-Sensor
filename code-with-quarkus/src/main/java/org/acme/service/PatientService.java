package org.acme.service;

import org.acme.dto.PatientDTO;
import org.acme.entity.Patient;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.persistence.EntityManager;
import jakarta.transaction.Transactional;

import java.util.List;

@ApplicationScoped
public class PatientService {

    @Inject
    EntityManager em;

    public List<Patient> listAll() {
        return em.createQuery("FROM Patient", Patient.class).getResultList();
    }

    public Patient findById(Long id) {
        return em.find(Patient.class, id);
    }

    @Transactional
    public Patient createOrUpdate(PatientDTO dto) {
        Patient patient = em.find(Patient.class, dto.id);
        if (patient == null) {
            patient = new Patient();
            patient.id = dto.id;
        }
        patient.name = dto.name;
        patient.age = dto.age;
        patient.gender = dto.gender;
        patient.health_condition = dto.health_condition;
        return em.merge(patient);
    }
}
