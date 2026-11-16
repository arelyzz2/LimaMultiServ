package pe.unamba.limamultiserv.service.impl;
import pe.unamba.limamultiserv.dto.PedidoRequest;
import pe.unamba.limamultiserv.exception.*;
import pe.unamba.limamultiserv.model.*;
import pe.unamba.limamultiserv.repository.*;
import pe.unamba.limamultiserv.service.PedidoService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.time.LocalDate;
import java.util.List;

@Service
@Transactional
public class PedidoServiceImpl implements PedidoService {
 private final PedidoRepository pedidos;
 private final ClienteRepository clientes;
 private final ProductoRepository productos;

 // Inyección por constructor: dependencias explícitas y fáciles de probar.
 public PedidoServiceImpl(PedidoRepository pedidos, ClienteRepository clientes, ProductoRepository productos){
  this.pedidos=pedidos; this.clientes=clientes; this.productos=productos;
 }
 public Pedido crear(PedidoRequest r){
  if(r.fechaEntrega().isBefore(LocalDate.now())) throw new ReglaNegocioException("La fecha de entrega no puede ser anterior a hoy");
  Cliente cliente=clientes.findById(r.clienteId())
   .orElseThrow(()->new RecursoNoEncontradoException("Cliente no encontrado: "+r.clienteId()));
  Producto producto=null;
  if(r.tipo()==TipoPedido.ESTANDAR){
   if(r.productoId()==null) throw new ReglaNegocioException("Un pedido estándar requiere seleccionar un producto");
   producto=productos.findById(r.productoId())
    .orElseThrow(()->new RecursoNoEncontradoException("Producto no encontrado: "+r.productoId()));
   if(!producto.isActivo()) throw new ReglaNegocioException("El producto seleccionado no está disponible");
  } else if(r.especificaciones()==null || r.especificaciones().isBlank()){
   throw new ReglaNegocioException("El pedido personalizado requiere especificaciones");
  }
  Pedido p=new Pedido(); p.setCliente(cliente); p.setProducto(producto); p.setTipo(r.tipo());
  p.setFechaEntrega(r.fechaEntrega()); p.setCantidad(r.cantidad()); p.setPrecioReferencial(r.precioReferencial());
  p.setEspecificaciones(r.especificaciones()); p.setImagenReferenciaUrl(r.imagenReferenciaUrl());
  p.setEstado(EstadoPedido.REGISTRADO);
  return pedidos.save(p);
 }
 public Pedido cambiarEstado(Long id, EstadoPedido estado){
  Pedido p=obtener(id);
  if(p.getEstado()==EstadoPedido.ENTREGADO || p.getEstado()==EstadoPedido.CANCELADO)
   throw new ReglaNegocioException("No se puede modificar un pedido finalizado");
  p.setEstado(estado); return pedidos.save(p);
 }
 @Transactional(readOnly=true) public Pedido obtener(Long id){
  return pedidos.findById(id).orElseThrow(()->new RecursoNoEncontradoException("Pedido no encontrado: "+id));
 }
 @Transactional(readOnly=true) public List<Pedido> listarPorCliente(Long clienteId){
  if(!clientes.existsById(clienteId)) throw new RecursoNoEncontradoException("Cliente no encontrado: "+clienteId);
  return pedidos.findByClienteIdOrderByFechaEntregaAsc(clienteId);
 }
}
