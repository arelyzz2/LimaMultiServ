package pe.unamba.limamultiserv.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.*;
import java.math.BigDecimal;

@Entity
@Table(name = "productos")
public class Producto {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @NotBlank @Size(max = 120)
    private String nombre;
    @Column(length = 1000)
    private String descripcion;
    @NotBlank @Size(max = 60)
    private String categoria;
    @NotNull @DecimalMin("0.00") @Digits(integer=8, fraction=2)
    private BigDecimal precioBase;
    private boolean activo = true;
    private String imagenUrl;

    public Producto() {}
    public Producto(String nombre, String descripcion, String categoria, BigDecimal precioBase) {
        this.nombre=nombre; this.descripcion=descripcion; this.categoria=categoria; this.precioBase=precioBase; this.activo=true;
    }
    public Long getId(){return id;} public void setId(Long id){this.id=id;}
    public String getNombre(){return nombre;} public void setNombre(String v){this.nombre=v;}
    public String getDescripcion(){return descripcion;} public void setDescripcion(String v){this.descripcion=v;}
    public String getCategoria(){return categoria;} public void setCategoria(String v){this.categoria=v;}
    public BigDecimal getPrecioBase(){return precioBase;} public void setPrecioBase(BigDecimal v){this.precioBase=v;}
    public boolean isActivo(){return activo;} public void setActivo(boolean v){this.activo=v;}
    public String getImagenUrl(){return imagenUrl;} public void setImagenUrl(String v){this.imagenUrl=v;}
}
