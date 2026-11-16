package pe.unamba.limamultiserv.dto;
import jakarta.validation.constraints.NotNull;
import pe.unamba.limamultiserv.model.EstadoPedido;

public record EstadoPedidoRequest(@NotNull EstadoPedido estado) {}
