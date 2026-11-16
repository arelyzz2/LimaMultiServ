package pe.unamba.limamultiserv.service.impl;
import pe.unamba.limamultiserv.dto.ClienteRequest;
import pe.unamba.limamultiserv.exception.*;
import pe.unamba.limamultiserv.model.Cliente;
import pe.unamba.limamultiserv.repository.ClienteRepository;
import pe.unamba.limamultiserv.service.ClienteService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;

@Service
@Transactional
public class ClienteServiceImpl implements ClienteService {
 private final ClienteRepository repository;
 public ClienteServiceImpl(ClienteRepository repository){this.repository=repository;}
 public Cliente crear(ClienteRequest r){
  if(repository.findByTelefono(r.telefono()).isPresent()) throw new ReglaNegocioException("El teléfono ya está registrado");
  return repository.save(new Cliente(r.nombres(),r.telefono(),r.correo(),r.direccion()));
 }
 @Transactional(readOnly=true) public List<Cliente> listar(){return repository.findAll();}
 @Transactional(readOnly=true) public Cliente obtener(Long id){
  return repository.findById(id).orElseThrow(()->new RecursoNoEncontradoException("Cliente no encontrado: "+id));
 }
}
