package org.acme.entity;

import jakarta.persistence.*;
import java.util.List;

@Entity
@Table(name = "devices")
public class Device {

    @Id
    public String id;

    public String name;
    public String type;
    public String status;

    @OneToMany(mappedBy = "device")
    public List<org.acme.entity.Experiment> experiments;
}
