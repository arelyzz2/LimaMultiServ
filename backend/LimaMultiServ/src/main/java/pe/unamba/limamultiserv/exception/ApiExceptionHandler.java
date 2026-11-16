package pe.unamba.limamultiserv.exception;

import org.springframework.http.*;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.*;
import java.time.LocalDateTime;
import java.util.*;

@RestControllerAdvice
public class ApiExceptionHandler {
 @ExceptionHandler(RecursoNoEncontradoException.class)
 public ResponseEntity<Map<String,Object>> noEncontrado(RecursoNoEncontradoException ex){
  return respuesta(HttpStatus.NOT_FOUND, ex.getMessage());
 }
 @ExceptionHandler(ReglaNegocioException.class)
 public ResponseEntity<Map<String,Object>> regla(ReglaNegocioException ex){
  return respuesta(HttpStatus.BAD_REQUEST, ex.getMessage());
 }
 @ExceptionHandler(MethodArgumentNotValidException.class)
 public ResponseEntity<Map<String,Object>> validacion(MethodArgumentNotValidException ex){
  String mensaje=ex.getBindingResult().getFieldErrors().stream()
   .map(e->e.getField()+": "+e.getDefaultMessage()).findFirst().orElse("Datos inválidos");
  return respuesta(HttpStatus.BAD_REQUEST,mensaje);
 }
 private ResponseEntity<Map<String,Object>> respuesta(HttpStatus status,String mensaje){
  Map<String,Object> body=new LinkedHashMap<>();
  body.put("fecha", LocalDateTime.now()); body.put("estado",status.value()); body.put("error",mensaje);
  return ResponseEntity.status(status).body(body);
 }
}
