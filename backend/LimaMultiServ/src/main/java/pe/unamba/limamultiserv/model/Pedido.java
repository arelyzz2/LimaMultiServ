package pe.unamba.limamultiserv.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Entity
@Table(name = "pedidos")
public class Pedido {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @ManyToOne(optional=false, fetch=FetchType.LAZY)
    @JoinColumn(name="cliente_id", nullable=false)
    private Cliente cliente;
    @ManyToOne(fetch=FetchType.LAZY)
    @JoinColumn(name="producto_id")
    private Producto producto;
    @Enumerated(EnumType.STRING)
    @Column(nullable=false, length=30)
    private TipoPedido tipo = TipoPedido.ESTANDAR;
    @Enumerated(EnumType.STRING)
    @Column(nullable=false, length=30)
    private EstadoPedido estado = EstadoPedido.REGISTRADO;
    @NotNull
    private LocalDate fechaEntrega;
    @Column(length=1500)
    private String especificaciones;
    private String imagenReferenciaUrl;
    @Column(nullable=false, precision=10, scale=2)
    private BigDecimal cantidad = BigDecimal.ONE;
    @Column(nullable=false, precision=10, scale=2)
    private BigDecimal precioReferencial = BigDecimal.ZERO;
    private LocalDateTime fechaRegistro = LocalDateTime.now();

    public Pedido() {}
    public Long getId(){return id;} public void setId(Long id){this.id=id;}
    public Cliente getCliente(){return cliente;} public void setCliente(Cliente v){this.cliente=v;}
    public Producto getProducto(){return producto;} public void setProducto(Producto v){this.producto=v;}
    public TipoPedido getTipo(){return tipo;} public void setTipo(TipoPedido v){this.tipo=v;}
    public EstadoPedido getEstado(){return estado;} public void setEstado(EstadoPedido v){this.estado=v;}
    public LocalDate getFechaEntrega(){return fechaEntrega;} public void setFechaEntrega(LocalDate v){this.fechaEntrega=v;}
    public String getEspecificaciones(){return especificaciones;} public void setEspecificaciones(String v){this.especificaciones=v;}
    public String getImagenReferenciaUrl(){return imagenReferenciaUrl;} public void setImagenReferenciaUrl(String v){this.imagenReferenciaUrl=v;}
    public BigDecimal getCantidad(){return cantidad;} public void setCantidad(BigDecimal v){this.cantidad=v;}
    public BigDecimal getPrecioReferencial(){return precioReferencial;} public void setPrecioReferencial(BigDecimal v){this.precioReferencial=v;}
    public LocalDateTime getFechaRegistro(){return fechaRegistro;} public void setFechaRegistro(LocalDateTime v){this.fechaRegistro=v;}
}
