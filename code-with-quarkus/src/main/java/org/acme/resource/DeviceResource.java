package org.acme.resource;

import org.acme.dto.DeviceDTO;
import org.acme.entity.Device;
import org.acme.service.DeviceStreamTracker;
import jakarta.inject.Inject;
import jakarta.persistence.EntityManager;
import jakarta.transaction.Transactional;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Path("/devices")
@Consumes(MediaType.APPLICATION_JSON)
@Produces(MediaType.APPLICATION_JSON)
public class DeviceResource {

    @Inject
    EntityManager em;

    @Inject
    DeviceStreamTracker deviceStreamTracker;

    @GET
    public List<DeviceDTO> getAll() {
        List<Device> devices = em.createQuery("FROM Device", Device.class).getResultList();
        return devices.stream().map(this::toDTO).collect(Collectors.toList());
    }

    @GET
    @Path("/{id}")
    public Response getById(@PathParam("id") Long id) {
        Device device = em.find(Device.class, id);
        if (device == null) {
            return Response.status(Response.Status.NOT_FOUND).build();
        }
        return Response.ok(toDTO(device)).build();
    }

    @GET
    @Path("/{id}/status")
    public Response checkDeviceStatus(@PathParam("id") Long id) {
        boolean active = deviceStreamTracker.isDeviceActive(id);
        return Response.ok(Map.of("available", active)).build();
    }

    @POST
    @Transactional
    public Response create(DeviceDTO dto) {
        if (dto.id == null) {
            return Response.status(Response.Status.BAD_REQUEST)
                .entity("Device ID must be provided").build();
        }

        Device device = new Device();
        device.id = dto.id;
        device.name = dto.name;
        device.type = dto.type;
        device.status = dto.status;

        em.persist(device);
        return Response.status(Response.Status.CREATED).entity(toDTO(device)).build();
    }

    private DeviceDTO toDTO(Device d) {
        DeviceDTO dto = new DeviceDTO();
        dto.id = d.id;
        dto.name = d.name;
        dto.type = d.type;
        dto.status = d.status;
        return dto;
    }
}
