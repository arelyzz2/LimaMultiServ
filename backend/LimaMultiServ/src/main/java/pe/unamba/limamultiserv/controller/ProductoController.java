package pe.unamba.limamultiserv.controller;
import pe.unamba.limamultiserv.dto.ProductoRequest;
import pe.unamba.limamultiserv.model.Producto;
import pe.unamba.limamultiserv.service.ProductoService;
import jakarta.validation.Valid;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController @RequestMapping("/api/productos")
public class ProductoController {
 private final ProductoService service;
 public ProductoController(ProductoService service){this.service=service;}
 @PostMapping public ResponseEntity<Producto> crear(@Valid @RequestBody ProductoRequest r){return ResponseEntity.status(HttpStatus.CREATED).body(service.crear(r));}
 @GetMapping public List<Producto> listar(){return service.listarActivos();}
 @GetMapping("/{id}") public Producto obtener(@PathVariable Long id){return service.obtener(id);}
}
