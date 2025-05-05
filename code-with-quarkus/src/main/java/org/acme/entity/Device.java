package org.acme.entity;

import jakarta.persistence.*;
import java.util.List;

@Entity
@Table(name = "devices")
public class Device {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    public Long id;

    public String name;
    public String type;
    public String status; // "available", "in_use", "maintenance"

    @OneToMany(mappedBy = "device")
    public List<org.acme.entity.Experiment> experiments;
}
