package pe.unamba.limamultiserv.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import java.time.LocalDateTime;

@Entity
@Table(name = "clientes")
public class Cliente {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @NotBlank @Size(max = 120)
    private String nombres;
    @NotBlank @Size(max = 20)
    @Column(unique = true)
    private String telefono;
    @Email @Size(max = 120)
    @Column(unique = true)
    private String correo;
    @Size(max = 180)
    private String direccion;
    private LocalDateTime fechaRegistro = LocalDateTime.now();

    public Cliente() {}
    public Cliente(String nombres, String telefono, String correo, String direccion) {
        this.nombres=nombres; this.telefono=telefono; this.correo=correo; this.direccion=direccion;
    }
    public Long getId(){return id;} public void setId(Long id){this.id=id;}
    public String getNombres(){return nombres;} public void setNombres(String v){this.nombres=v;}
    public String getTelefono(){return telefono;} public void setTelefono(String v){this.telefono=v;}
    public String getCorreo(){return correo;} public void setCorreo(String v){this.correo=v;}
    public String getDireccion(){return direccion;} public void setDireccion(String v){this.direccion=v;}
    public LocalDateTime getFechaRegistro(){return fechaRegistro;} public void setFechaRegistro(LocalDateTime v){this.fechaRegistro=v;}
}
