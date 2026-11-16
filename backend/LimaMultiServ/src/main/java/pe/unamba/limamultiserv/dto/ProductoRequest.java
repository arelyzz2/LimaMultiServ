package pe.unamba.limamultiserv.dto;
import jakarta.validation.constraints.*;
import java.math.BigDecimal;

public record ProductoRequest(
 @NotBlank @Size(max=120) String nombre,
 @Size(max=1000) String descripcion,
 @NotBlank @Size(max=60) String categoria,
 @NotNull @DecimalMin("0.00") BigDecimal precioBase,
 String imagenUrl
) {}
