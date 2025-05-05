package org.acme.service;

import org.acme.dto.ExperimentDTO;
import org.acme.entity.Device;
import org.acme.entity.Experiment;
import org.acme.entity.Patient;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.persistence.EntityManager;
import jakarta.transaction.Transactional;

import java.util.List;

@ApplicationScoped
public class ExperimentService {

    @Inject
    EntityManager em;

    @Inject
    DeviceAssignmentRegistry assignmentRegistry;

    public List<Experiment> listAll() {
        return em.createQuery("FROM Experiment", Experiment.class).getResultList();
    }

    public Experiment findById(Long id) {
        return em.find(Experiment.class, id);
    }

    @Transactional
    public Experiment create(ExperimentDTO dto) {
        Patient patient = em.find(Patient.class, dto.patientId);
        if (patient == null) {
            throw new IllegalArgumentException("Patient not found");
        }

        Device device = em.find(Device.class, dto.deviceId);
        if (device == null) {
            throw new IllegalArgumentException("Device not found");
        }

        if (!"available".equalsIgnoreCase(device.status)) {
            throw new IllegalStateException("Device is not available (current status: " + device.status + ")");
        }

        device.status = "in_use";
        em.merge(device);

        Experiment experiment = new Experiment();
        experiment.id = dto.id;
        experiment.name = dto.name;
        experiment.notes = dto.notes;
        experiment.patient = patient;
        experiment.device = device;

        em.persist(experiment);
        assignmentRegistry.assign(device.id, experiment.id);
        return experiment;
    }
}
