package pe.unamba.limamultiserv.service.impl;
import pe.unamba.limamultiserv.dto.ProductoRequest;
import pe.unamba.limamultiserv.exception.RecursoNoEncontradoException;
import pe.unamba.limamultiserv.model.Producto;
import pe.unamba.limamultiserv.repository.ProductoRepository;
import pe.unamba.limamultiserv.service.ProductoService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;

@Service
@Transactional
public class ProductoServiceImpl implements ProductoService {
 private final ProductoRepository repository;
 public ProductoServiceImpl(ProductoRepository repository){this.repository=repository;}
 public Producto crear(ProductoRequest r){
  Producto p=new Producto(r.nombre(),r.descripcion(),r.categoria(),r.precioBase());
  p.setImagenUrl(r.imagenUrl()); return repository.save(p);
 }
 @Transactional(readOnly=true) public List<Producto> listarActivos(){return repository.findByActivoTrue();}
 @Transactional(readOnly=true) public Producto obtener(Long id){
  return repository.findById(id).orElseThrow(()->new RecursoNoEncontradoException("Producto no encontrado: "+id));
 }
}
