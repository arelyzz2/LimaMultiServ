package pe.unamba.limamultiserv.service;
import pe.unamba.limamultiserv.dto.ProductoRequest;
import pe.unamba.limamultiserv.model.Producto;
import java.util.List;

public interface ProductoService {
 Producto crear(ProductoRequest request);
 List<Producto> listarActivos();
 Producto obtener(Long id);
}
