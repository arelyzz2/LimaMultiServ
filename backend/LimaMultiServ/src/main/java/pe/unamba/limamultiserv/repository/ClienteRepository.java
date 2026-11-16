package pe.unamba.limamultiserv.repository;

import pe.unamba.limamultiserv.model.Cliente;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.*;

public interface ClienteRepository extends JpaRepository<Cliente, Long> {
    Optional<Cliente> findByTelefono(String telefono);
}
