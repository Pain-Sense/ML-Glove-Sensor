package org.acme.entity;
import jakarta.persistence.*;

@Entity
@Table(name = "experiments")
public class Experiment {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    public Long id;

    public String name;
    public String notes;

    @ManyToOne
    @JoinColumn(name = "patient_id", nullable = false)
    public Patient patient;

    @ManyToOne
    @JoinColumn(name = "device_id")
    public Device device;
}
