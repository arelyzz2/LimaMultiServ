package pe.unamba.limamultiserv.dto;
import jakarta.validation.constraints.*;
import pe.unamba.limamultiserv.model.TipoPedido;
import java.math.BigDecimal;
import java.time.LocalDate;

public record PedidoRequest(
 @NotNull Long clienteId,
 Long productoId,
 @NotNull TipoPedido tipo,
 @NotNull LocalDate fechaEntrega,
 @NotNull @DecimalMin("0.01") BigDecimal cantidad,
 @NotNull @DecimalMin("0.00") BigDecimal precioReferencial,
 String especificaciones,
 String imagenReferenciaUrl
) {}
