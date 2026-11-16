package pe.unamba.limamultiserv.controller;
import pe.unamba.limamultiserv.dto.*;
import pe.unamba.limamultiserv.model.*;
import pe.unamba.limamultiserv.service.PedidoService;
import jakarta.validation.Valid;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController @RequestMapping("/api/pedidos")
public class PedidoController {
 private final PedidoService service;
 public PedidoController(PedidoService service){this.service=service;}
 @PostMapping public ResponseEntity<Pedido> crear(@Valid @RequestBody PedidoRequest r){return ResponseEntity.status(HttpStatus.CREATED).body(service.crear(r));}
 @GetMapping("/{id}") public Pedido obtener(@PathVariable Long id){return service.obtener(id);}
 @GetMapping("/cliente/{clienteId}") public List<Pedido> listarPorCliente(@PathVariable Long clienteId){return service.listarPorCliente(clienteId);}
 @PatchMapping("/{id}/estado") public Pedido cambiarEstado(@PathVariable Long id,@Valid @RequestBody EstadoPedidoRequest r){return service.cambiarEstado(id,r.estado());}
}
