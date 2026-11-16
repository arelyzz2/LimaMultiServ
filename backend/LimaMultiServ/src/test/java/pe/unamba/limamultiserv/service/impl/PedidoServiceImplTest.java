package pe.unamba.limamultiserv.service.impl;

import pe.unamba.limamultiserv.dto.PedidoRequest;
import pe.unamba.limamultiserv.exception.ReglaNegocioException;
import pe.unamba.limamultiserv.model.*;
import pe.unamba.limamultiserv.repository.*;
import org.junit.jupiter.api.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.*;
import org.mockito.junit.jupiter.MockitoExtension;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Optional;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class PedidoServiceImplTest {
 @Mock PedidoRepository pedidos;
 @Mock ClienteRepository clientes;
 @Mock ProductoRepository productos;
 @InjectMocks PedidoServiceImpl service;

 @Test void pedidoEstandarValidoDebeGuardarse(){
  Cliente c=new Cliente("Ana Pérez","987654321","ana@mail.com","Abancay");
  Producto p=new Producto("Banda de honor","Bordada","Bandas",new BigDecimal("45.00"));
  when(clientes.findById(1L)).thenReturn(Optional.of(c));
  when(productos.findById(2L)).thenReturn(Optional.of(p));
  when(pedidos.save(any(Pedido.class))).thenAnswer(i->i.getArgument(0));
  PedidoRequest req=new PedidoRequest(1L,2L,TipoPedido.ESTANDAR,LocalDate.now().plusDays(7),
    BigDecimal.ONE,new BigDecimal("45.00"),null,null);
  Pedido result=service.crear(req);
  assertEquals(EstadoPedido.REGISTRADO,result.getEstado());
  assertEquals(TipoPedido.ESTANDAR,result.getTipo());
  verify(pedidos).save(any(Pedido.class));
 }

 @Test void estandarSinProductoDebeLanzarError(){
  when(clientes.findById(1L)).thenReturn(Optional.of(new Cliente("Ana","999","a@mail.com","Abancay")));
  PedidoRequest req=new PedidoRequest(1L,null,TipoPedido.ESTANDAR,LocalDate.now().plusDays(2),
    BigDecimal.ONE,BigDecimal.ZERO,null,null);
  assertThrows(ReglaNegocioException.class,()->service.crear(req));
  verify(pedidos,never()).save(any());
 }

 @Test void personalizadoSinEspecificacionesDebeLanzarError(){
  when(clientes.findById(1L)).thenReturn(Optional.of(new Cliente("Ana","999","a@mail.com","Abancay")));
  PedidoRequest req=new PedidoRequest(1L,null,TipoPedido.PERSONALIZADO,LocalDate.now().plusDays(2),
    BigDecimal.ONE,BigDecimal.ZERO,"  ",null);
  assertThrows(ReglaNegocioException.class,()->service.crear(req));
 }

 @Test void fechaPasadaDebeLanzarErrorAntesDeConsultarCliente(){
  PedidoRequest req=new PedidoRequest(1L,2L,TipoPedido.ESTANDAR,LocalDate.now().minusDays(1),
    BigDecimal.ONE,BigDecimal.ZERO,null,null);
  assertThrows(ReglaNegocioException.class,()->service.crear(req));
  verifyNoInteractions(clientes,productos,pedidos);
 }
}
