package pe.unamba.limamultiserv.controller;
import pe.unamba.limamultiserv.dto.ClienteRequest;
import pe.unamba.limamultiserv.model.Cliente;
import pe.unamba.limamultiserv.service.ClienteService;
import jakarta.validation.Valid;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController @RequestMapping("/api/clientes")
public class ClienteController {
 private final ClienteService service;
 public ClienteController(ClienteService service){this.service=service;}
 @PostMapping public ResponseEntity<Cliente> crear(@Valid @RequestBody ClienteRequest r){return ResponseEntity.status(HttpStatus.CREATED).body(service.crear(r));}
 @GetMapping public List<Cliente> listar(){return service.listar();}
 @GetMapping("/{id}") public Cliente obtener(@PathVariable Long id){return service.obtener(id);}
}
