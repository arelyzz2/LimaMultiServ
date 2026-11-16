"""Datos y persistencia local del negocio."""
import os
import json
import sqlite3
from contextlib import contextmanager
from werkzeug.security import generate_password_hash

CORREOS_DUENOS = {"admin@limamultiserv.pe"}
USUARIOS = {"admin@limamultiserv.pe": {"nombre": "Administradora", "hash": generate_password_hash("admin123")}}

ESTADOS = ["Pendiente", "En proceso", "Terminado"]
CATEGORIAS = [("Capas patronales", "capas.jpg"), ("Bandas de honor", "bandas.jpg"),
              ("Banderas", "banderas.jpg"), ("Banderolas", "banderolas.jpg")]

CATALOGO = [
    dict(id=1, nombre="Capa patronal bordada", categoria="Capas patronales", precio=450.0, imagen="capa1.jpg", destacado=True,
         descripcion="Terciopelo con hilo dorado y detalles artesanales."),
    dict(id=2, nombre="Banda de honor clásica", categoria="Bandas de honor", precio=120.0, imagen="banda1.jpg", destacado=True,
         descripcion="Satén con flecos y bordado de nombre."),
    dict(id=3, nombre="Bandera institucional", categoria="Banderas", precio=120.0, imagen="bandera1.jpg", destacado=True,
         descripcion="Tela resistente, medidas estándar 1.20 × 0.80 m."),
    dict(id=4, nombre="Banderola de ceremonia", categoria="Banderolas", precio=200.0, imagen="banderola1.jpg", destacado=True,
         descripcion="Acabado en bordado, ideal para desfiles."),
]
CLIENTES = [dict(nombre="María Quispe", correo="maria@correo.pe", telefono="900 111 222"),
            dict(nombre="Colegio San Miguel", correo="colegio@correo.pe", telefono="900 333 444"),
            dict(nombre="José Huamán", correo="jose@correo.pe", telefono="900 555 666")]
PEDIDOS = [  # entrega en formato AAAA-MM-DD, None = por coordinar
    dict(id=1, cliente="María Quispe", correo="", tipo="Capa patronal", entrega="2026-11-22", estado="Pendiente", detalle="Capa vino con bordado dorado.", adjuntos=[]),
    dict(id=2, cliente="Colegio San Miguel", correo="", tipo="Banderas", entrega="2026-11-25", estado="En proceso", detalle="Cuatro banderas institucionales.", adjuntos=[]),
    dict(id=3, cliente="Hermandad Virgen del Rosario", correo="", tipo="Bandas de honor", entrega="2026-11-28", estado="En proceso", detalle="Doce bandas con nombre.", adjuntos=[]),
    dict(id=4, cliente="José Huamán", correo="", tipo="Prenda personalizada", entrega="2026-12-02", estado="Pendiente", detalle="Según imagen de referencia.", adjuntos=[]),
    dict(id=5, cliente="Municipalidad Distrital", correo="", tipo="Banderolas", entrega="2026-11-10", estado="Terminado", detalle="Seis banderolas.", adjuntos=[]),
]

_db_path = None


@contextmanager
def _conexion(path):
    conn = sqlite3.connect(path)
    try:
        with conn:
            yield conn
    finally:
        conn.close()


def nuevo_id(lista):
    return max((x["id"] for x in lista), default=0) + 1


def _guardar_en_conexion(conn):
    conn.execute("DELETE FROM usuarios")
    conn.executemany(
        "INSERT INTO usuarios(correo, nombre, hash, dueno) VALUES (?, ?, ?, ?)",
        [(correo, usuario["nombre"], usuario["hash"], int(correo in CORREOS_DUENOS))
         for correo, usuario in USUARIOS.items()])
    conn.execute("DELETE FROM clientes")
    conn.executemany(
        "INSERT INTO clientes(correo, nombre, telefono) VALUES (?, ?, ?)",
        [(c["correo"], c["nombre"], c.get("telefono", "")) for c in CLIENTES])
    conn.execute("DELETE FROM pedidos")
    conn.executemany(
        """INSERT INTO pedidos(id, cliente, correo, tipo, entrega, estado, detalle, adjuntos)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        [(p["id"], p["cliente"], p.get("correo", ""), p["tipo"], p["entrega"], p["estado"], p["detalle"],
          json.dumps(p.get("adjuntos", [])))
         for p in PEDIDOS])
    conn.execute("DELETE FROM catalogo")
    conn.executemany(
        """INSERT INTO catalogo(id, nombre, categoria, precio, imagen, destacado, descripcion)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        [(p["id"], p["nombre"], p["categoria"], p["precio"], p["imagen"],
          int(p["destacado"]), p["descripcion"]) for p in CATALOGO])


def iniciar_base_datos(path):
    """Crea el esquema local y carga los datos guardados, o los datos iniciales."""
    global _db_path
    _db_path = os.path.abspath(path)
    os.makedirs(os.path.dirname(_db_path), exist_ok=True)
    with _conexion(_db_path) as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS usuarios (
                correo TEXT PRIMARY KEY, nombre TEXT NOT NULL, hash TEXT NOT NULL,
                dueno INTEGER NOT NULL DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS clientes (
                correo TEXT PRIMARY KEY, nombre TEXT NOT NULL, telefono TEXT NOT NULL DEFAULT ''
            );
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY, cliente TEXT NOT NULL, correo TEXT NOT NULL DEFAULT '',
                tipo TEXT NOT NULL,
                entrega TEXT, estado TEXT NOT NULL, detalle TEXT NOT NULL,
                adjuntos TEXT NOT NULL DEFAULT '[]'
            );
            CREATE TABLE IF NOT EXISTS catalogo (
                id INTEGER PRIMARY KEY, nombre TEXT NOT NULL, categoria TEXT NOT NULL,
                precio REAL, imagen TEXT NOT NULL, destacado INTEGER NOT NULL,
                descripcion TEXT NOT NULL
            );
        """)
        columnas_pedidos = {row[1] for row in conn.execute("PRAGMA table_info(pedidos)")}
        if "adjuntos" not in columnas_pedidos:
            conn.execute("ALTER TABLE pedidos ADD COLUMN adjuntos TEXT NOT NULL DEFAULT '[]'")
        if "correo" not in columnas_pedidos:
            conn.execute("ALTER TABLE pedidos ADD COLUMN correo TEXT NOT NULL DEFAULT ''")
        existentes = conn.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
        if not existentes:
            _guardar_en_conexion(conn)
            return

        usuarios = conn.execute("SELECT correo, nombre, hash, dueno FROM usuarios").fetchall()
        USUARIOS.clear()
        CORREOS_DUENOS.clear()
        for correo, nombre, password_hash, dueno in usuarios:
            USUARIOS[correo] = {"nombre": nombre, "hash": password_hash}
            if dueno:
                CORREOS_DUENOS.add(correo)

        CLIENTES[:] = [
            {"correo": correo, "nombre": nombre, "telefono": telefono}
            for correo, nombre, telefono in conn.execute(
                "SELECT correo, nombre, telefono FROM clientes ORDER BY rowid")]
        PEDIDOS[:] = [
            {"id": ident, "cliente": cliente, "correo": correo, "tipo": tipo, "entrega": entrega,
             "estado": estado, "detalle": detalle, "adjuntos": json.loads(adjuntos)}
            for ident, cliente, correo, tipo, entrega, estado, detalle, adjuntos in conn.execute(
                """SELECT id, cliente, correo, tipo, entrega, estado, detalle, adjuntos
                   FROM pedidos ORDER BY id""")]
        CATALOGO[:] = [
            {"id": ident, "nombre": nombre, "categoria": categoria, "precio": precio,
             "imagen": imagen, "destacado": bool(destacado), "descripcion": descripcion}
            for ident, nombre, categoria, precio, imagen, destacado, descripcion in conn.execute(
                """SELECT id, nombre, categoria, precio, imagen, destacado, descripcion
                   FROM catalogo ORDER BY id""")]


def guardar_datos():
    """Persiste los cambios en una transacción SQLite."""
    if _db_path is None:
        raise RuntimeError("La base de datos no se ha inicializado.")
    with _conexion(_db_path) as conn:
        _guardar_en_conexion(conn)


def resumen():
    n = lambda e: sum(p["estado"] == e for p in PEDIDOS)
    return [("Total de pedidos", len(PEDIDOS), "pedidos"), ("Pedidos pendientes", n("Pendiente"), "reloj"),
            ("Pedidos en proceso", n("En proceso"), "aguja"), ("Pedidos terminados", n("Terminado"), "check")]


def precio_txt(p):
    return f"S/ {p:,.2f}" if p is not None else "Precio a coordinar"


