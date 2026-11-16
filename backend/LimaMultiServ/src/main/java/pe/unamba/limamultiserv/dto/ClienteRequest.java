package pe.unamba.limamultiserv.dto;
import jakarta.validation.constraints.*;

public record ClienteRequest(
 @NotBlank @Size(max=120) String nombres,
 @NotBlank @Size(max=20) String telefono,
 @Email @Size(max=120) String correo,
 @Size(max=180) String direccion
) {}
