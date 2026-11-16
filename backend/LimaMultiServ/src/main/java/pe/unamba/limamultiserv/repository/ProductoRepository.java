package pe.unamba.limamultiserv.repository;

import pe.unamba.limamultiserv.model.Producto;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.*;
import java.util.List;

public interface ProductoRepository extends JpaRepository<Producto, Long> {
    List<Producto> findByActivoTrue();
}
