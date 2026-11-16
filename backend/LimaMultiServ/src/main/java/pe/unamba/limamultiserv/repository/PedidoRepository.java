package pe.unamba.limamultiserv.repository;

import pe.unamba.limamultiserv.model.Pedido;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.*;
import java.util.List;

public interface PedidoRepository extends JpaRepository<Pedido, Long> {
    List<Pedido> findByClienteIdOrderByFechaEntregaAsc(Long clienteId);
}
