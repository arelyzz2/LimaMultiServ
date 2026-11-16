# LimaMultiServ — Sistema Web de Gestión y Organización de Pedidos

Proyecto académico de Ingeniería de Software I — UNAMBA, semestre 2026-II.

## 1. Propósito
Centralizar el registro de clientes, catálogo y pedidos de confecciones de Lima Multiservicios. Permite registrar pedidos estándar y personalizados, guardar especificaciones y fecha de entrega, y actualizar el estado del pedido.

## 2. Tecnologías
- Java 17
- Spring Boot 3.3.5
- Spring Web, Spring Data JPA, Bean Validation
- MySQL 8+
- Maven
- JUnit 5 y Mockito
- Git / GitHub

## 3. Estructura del proyecto
```text
LimaMultiServ/
├── database/limamultiserv.sql
├── docs/
│   ├── diagramas.md
│   ├── pruebas.md
│   ├── interfaces.md
│   └── plan-github.md
├── src/
│   ├── main/java/pe/unamba/limamultiserv/
│   │   ├── LimaMultiServApplication.java
│   │   ├── controller/
│   │   ├── dto/
│   │   ├── exception/
│   │   ├── model/
│   │   ├── repository/
│   │   └── service/impl/
│   ├── main/resources/application.properties
│   └── test/java/...
└── pom.xml
```

## 4. Requisitos previos
Instalar JDK 17, Maven 3.8+ y MySQL 8+. Crear la base de datos ejecutando `database/limamultiserv.sql` o permitir que MySQL la cree mediante la URL configurada.

## 5. Configuración
Por defecto:
- Base de datos: `limamultiserv`
- Usuario MySQL: `root`
- Contraseña: vacía
- Puerto API: `8080`

Si tu MySQL tiene otra contraseña, define variables de entorno antes de ejecutar:
- Windows PowerShell: `$env:DB_USER="root"; $env:DB_PASSWORD="tu_clave"`
- Opcional: `$env:DB_URL="jdbc:mysql://localhost:3306/limamultiserv?createDatabaseIfNotExist=true&useSSL=false&serverTimezone=America/Lima&allowPublicKeyRetrieval=true"`

## 6. Ejecutar
Desde la carpeta donde está `pom.xml`:
```bash
mvn clean test
mvn spring-boot:run
```
API disponible en `http://localhost:8080`.

## 7. Endpoints principales

### Clientes
- `POST /api/clientes` — registrar
- `GET /api/clientes` — listar
- `GET /api/clientes/{id}` — consultar

Ejemplo POST:
```json
{
  "nombres": "María Quispe",
  "telefono": "987654321",
  "correo": "maria@gmail.com",
  "direccion": "Abancay"
}
```

### Productos
- `POST /api/productos` — registrar producto (uso administrativo)
- `GET /api/productos` — catálogo de productos activos
- `GET /api/productos/{id}` — detalle

Ejemplo POST:
```json
{
  "nombre": "Banda de honor",
  "descripcion": "Banda institucional bordada",
  "categoria": "Bandas",
  "precioBase": 45.00,
  "imagenUrl": ""
}
```

### Pedidos
- `POST /api/pedidos` — registrar pedido
- `GET /api/pedidos/{id}` — detalle
- `GET /api/pedidos/cliente/{clienteId}` — pedidos del cliente por fecha de entrega
- `PATCH /api/pedidos/{id}/estado` — actualizar estado

Pedido estándar:
```json
{
  "clienteId": 1,
  "productoId": 1,
  "tipo": "ESTANDAR",
  "fechaEntrega": "2026-12-10",
  "cantidad": 2,
  "precioReferencial": 90.00,
  "especificaciones": "Color azul y bordado dorado",
  "imagenReferenciaUrl": ""
}
```

Pedido personalizado:
```json
{
  "clienteId": 1,
  "productoId": null,
  "tipo": "PERSONALIZADO",
  "fechaEntrega": "2026-12-12",
  "cantidad": 1,
  "precioReferencial": 150.00,
  "especificaciones": "Capa de terciopelo azul, medidas acordadas, escudo bordado",
  "imagenReferenciaUrl": ""
}
```

Actualizar estado:
```json
{ "estado": "EN_CONFECCION" }
```
Estados: `REGISTRADO`, `EN_REVISION`, `ACEPTADO`, `EN_CONFECCION`, `LISTO`, `ENTREGADO`, `CANCELADO`.

## 8. Aplicación de SOLID
- **S — Responsabilidad única:** controladores reciben peticiones; servicios aplican reglas; repositorios acceden a datos.
- **O — Abierto/cerrado:** las reglas se amplían implementando interfaces de servicio sin introducir lógica de negocio en controladores.
- **L — Sustitución de Liskov:** las implementaciones concretas respetan los contratos definidos por las interfaces de servicio.
- **I — Segregación de interfaces:** servicios separados por dominio (Cliente, Producto y Pedido), sin una interfaz gigante.
- **D — Inversión de dependencias:** controladores dependen de interfaces de servicio; servicios reciben repositorios por constructor.

## 9. Alcance y limitaciones de esta versión
Incluye registro y consulta de clientes, catálogo, registro de pedidos estándar/personalizados y seguimiento de estados. No incluye pagos en línea, delivery, aplicación móvil, cálculo automático de cotización personalizada, IA ni control detallado de producción, de acuerdo con el Entregable 01. La autenticación/roles y la carga real de imágenes quedan como siguiente incremento.

## 10. Git y GitHub
Consultar `docs/plan-github.md`. No subir contraseñas ni datos reales de clientes al repositorio.


## Abrir en Spring Tool Suite (Eclipse)
1. Descomprime este ZIP en una carpeta de tu computadora.
2. Abre Spring Tool Suite.
3. Selecciona **File > Import... > Maven > Existing Maven Projects**.
4. En **Root Directory**, selecciona la carpeta `LimaMultiServ`.
5. Marca el `pom.xml` detectado y pulsa **Finish**.
6. Espera a que Maven descargue las dependencias.
7. Configura MySQL en `src/main/resources/application.properties`.
8. Abre `LimaMultiServApplication.java` y selecciona **Run As > Spring Boot App**.

Requisitos: JDK 17 y Spring Tool Suite con soporte Maven (m2e).
