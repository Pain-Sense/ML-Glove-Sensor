package org.acme.service;

import org.acme.dto.DeviceDTO;
import org.acme.entity.Device;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.persistence.EntityManager;
import jakarta.transaction.Transactional;

import java.util.List;

@ApplicationScoped
public class DeviceService {

    @Inject
    EntityManager em;

    public List<Device> listAll() {
        return em.createQuery("FROM Device", Device.class).getResultList();
    }

    public Device findById(Long id) {
        return em.find(Device.class, id);
    }

    @Transactional
    public Device create(DeviceDTO dto) {
        Device device = new Device();
        device.id = dto.id;
        device.name = dto.name;
        device.type = dto.type;
        device.status = dto.status;
        em.persist(device);
        return device;
    }
}
