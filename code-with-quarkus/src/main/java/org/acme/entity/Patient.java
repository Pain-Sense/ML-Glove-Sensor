package org.acme.entity;
import jakarta.persistence.*;
import java.util.List;

@Entity
@Table(name = "patients")
public class Patient {

    @Id
    public String id;

    public String name;
    public String age;
    public String gender;
    public String health_condition;

    @OneToMany(mappedBy = "patient", cascade = CascadeType.ALL, orphanRemoval = true)
    public List<org.acme.entity.Experiment> experiments;
}