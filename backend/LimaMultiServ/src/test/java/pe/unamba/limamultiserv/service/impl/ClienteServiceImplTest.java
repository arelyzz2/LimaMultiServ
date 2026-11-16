package pe.unamba.limamultiserv.service.impl;
import pe.unamba.limamultiserv.dto.ClienteRequest;
import pe.unamba.limamultiserv.exception.ReglaNegocioException;
import pe.unamba.limamultiserv.model.Cliente;
import pe.unamba.limamultiserv.repository.ClienteRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.*;
import org.mockito.junit.jupiter.MockitoExtension;
import java.util.Optional;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class ClienteServiceImplTest {
 @Mock ClienteRepository repository;
 @InjectMocks ClienteServiceImpl service;

 @Test void telefonoDuplicadoNoDebeRegistrar(){
  when(repository.findByTelefono("987654321")).thenReturn(Optional.of(new Cliente()));
  ClienteRequest req=new ClienteRequest("María","987654321","maria@mail.com","Abancay");
  assertThrows(ReglaNegocioException.class,()->service.crear(req));
  verify(repository,never()).save(any());
 }
}
