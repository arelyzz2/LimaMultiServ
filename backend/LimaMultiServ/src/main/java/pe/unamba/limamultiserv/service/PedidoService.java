package pe.unamba.limamultiserv.service;
import pe.unamba.limamultiserv.dto.PedidoRequest;
import pe.unamba.limamultiserv.model.*;
import java.util.List;

public interface PedidoService {
 Pedido crear(PedidoRequest request);
 Pedido cambiarEstado(Long id, EstadoPedido estado);
 Pedido obtener(Long id);
 List<Pedido> listarPorCliente(Long clienteId);
}
