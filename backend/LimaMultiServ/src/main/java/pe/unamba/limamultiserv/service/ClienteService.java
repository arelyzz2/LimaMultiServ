package pe.unamba.limamultiserv.service;
import pe.unamba.limamultiserv.dto.ClienteRequest;
import pe.unamba.limamultiserv.model.Cliente;
import java.util.List;

public interface ClienteService {
 Cliente crear(ClienteRequest request);
 List<Cliente> listar();
 Cliente obtener(Long id);
}
