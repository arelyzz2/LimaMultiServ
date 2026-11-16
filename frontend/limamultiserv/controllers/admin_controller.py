import calendar
import math
import os
import uuid
from datetime import date
from functools import wraps
from flask import (Blueprint, render_template, session, redirect, url_for, abort, request, flash,
                   current_app, send_from_directory)
from werkzeug.utils import secure_filename
import models

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]
EXTENSIONES_IMAGEN = {"jpg", "jpeg", "png", "webp"}


def solo_dueno(vista):
    @wraps(vista)
    def envoltura(*a, **k):
        if "correo" not in session:
            return redirect(url_for("auth.login"))
        if not session.get("dueno"):
            abort(403)
        return vista(*a, **k)
    return envoltura


def _buscar(lista, ident):
    for x in lista:
        if x["id"] == ident:
            return x
    abort(404)


def _orden(p):
    return p["entrega"] or "9999"


class AdminController:
    """Panel de gestión, solo para los correos del negocio."""
    bp = Blueprint("admin", __name__, url_prefix="/admin")

    # ---------- Panel principal ----------
    @staticmethod
    @bp.route("/")
    @solo_dueno
    def panel():
        h = date.today()
        recientes = sorted(models.PEDIDOS, key=lambda p: -p["id"])[:5]
        proximas = sorted((p for p in models.PEDIDOS if p["estado"] != "Terminado"), key=_orden)[:5]
        return render_template("admin/panel.html", resumen=models.resumen(), recientes=recientes,
                               proximas=proximas, fecha=f"{h.day} de {MESES[h.month-1]} de {h.year}")

    # ---------- Pedidos ----------
    @staticmethod
    @bp.route("/pedidos")
    @solo_dueno
    def pedidos():
        est = request.args.get("estado", "")
        lista = [p for p in models.PEDIDOS if not est or p["estado"] == est]
        return render_template("admin/pedidos.html", pedidos=sorted(lista, key=lambda p: -p["id"]), estado=est)

    @staticmethod
    @bp.route("/pedidos/nuevo", methods=["GET", "POST"])
    @solo_dueno
    def pedido_nuevo():
        if request.method == "POST":
            f = request.form
            cliente = f.get("cliente", "").strip()
            tipo = f.get("tipo", "")
            entrega = f.get("entrega", "")
            if not cliente:
                flash("Ingresa el nombre del cliente.")
                return render_template("admin/pedido_nuevo.html", clientes=models.CLIENTES,
                                       tipos=[c[0] for c in models.CATEGORIAS] + ["Prenda personalizada"])
            if tipo not in [c[0] for c in models.CATEGORIAS] + ["Prenda personalizada"]:
                flash("Selecciona un tipo de trabajo válido.")
                return render_template("admin/pedido_nuevo.html", clientes=models.CLIENTES,
                                       tipos=[c[0] for c in models.CATEGORIAS] + ["Prenda personalizada"])
            try:
                if entrega:
                    date.fromisoformat(entrega)
            except ValueError:
                flash("La fecha de entrega no es válida.")
                return render_template("admin/pedido_nuevo.html", clientes=models.CLIENTES,
                                       tipos=[c[0] for c in models.CATEGORIAS] + ["Prenda personalizada"])
            models.PEDIDOS.append(dict(id=models.nuevo_id(models.PEDIDOS), cliente=cliente, tipo=tipo,
                                       correo=next((c["correo"] for c in models.CLIENTES
                                                    if c["nombre"].casefold() == cliente.casefold()), ""),
                                       entrega=entrega or None, estado="Pendiente",
                                       detalle=f.get("detalle", "").strip(), adjuntos=[]))
            models.guardar_datos()
            flash("Pedido registrado.")
            return redirect(url_for("admin.pedidos"))
        return render_template("admin/pedido_nuevo.html", clientes=models.CLIENTES,
                               tipos=[c[0] for c in models.CATEGORIAS] + ["Prenda personalizada"])

    @staticmethod
    @bp.route("/pedido/<int:pid>", methods=["GET", "POST"])
    @solo_dueno
    def detalle(pid):
        p = _buscar(models.PEDIDOS, pid)
        if request.method == "POST":
            estado = request.form.get("estado", "")
            entrega = request.form.get("entrega", "")
            if estado not in models.ESTADOS:
                flash("Selecciona un estado válido.")
                return render_template("admin/detalle.html", p=p, estados=models.ESTADOS)
            try:
                if entrega:
                    date.fromisoformat(entrega)
            except ValueError:
                flash("La fecha de entrega no es válida.")
                return render_template("admin/detalle.html", p=p, estados=models.ESTADOS)
            p["estado"] = estado
            p["entrega"] = entrega or None
            p["detalle"] = request.form.get("detalle", "").strip()
            models.guardar_datos()
            flash("Pedido actualizado.")
            return redirect(url_for("admin.detalle", pid=pid))
        return render_template("admin/detalle.html", p=p, estados=models.ESTADOS)

    @staticmethod
    @bp.route("/pedido/<int:pid>/archivo/<filename>")
    @solo_dueno
    def pedido_archivo(pid, filename):
        pedido = _buscar(models.PEDIDOS, pid)
        if not any(a.get("filename") == filename for a in pedido.get("adjuntos", [])):
            abort(404)
        return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename,
                                   as_attachment=False)

    # ---------- Clientes ----------
    @staticmethod
    @bp.route("/clientes")
    @solo_dueno
    def clientes():
        q = request.args.get("q", "").strip().lower()
        filas = []
        for c in models.CLIENTES:
            if q and q not in c["nombre"].lower() and q not in c["correo"].lower():
                continue
            cantidad = sum(
                p.get("correo") == c["correo"] if p.get("correo")
                else p["cliente"] == c["nombre"] for p in models.PEDIDOS)
            filas.append((c, cantidad))
        return render_template("admin/clientes.html", filas=filas, q=q)

    # ---------- Catálogo ----------
    @staticmethod
    @bp.route("/catalogo")
    @solo_dueno
    def catalogo():
        return render_template("admin/catalogo.html", productos=models.CATALOGO, precio=models.precio_txt)

    @staticmethod
    @bp.route("/catalogo/nuevo", methods=["GET", "POST"])
    @bp.route("/catalogo/<int:pid>/editar", methods=["GET", "POST"])
    @solo_dueno
    def producto(pid=None):
        p = _buscar(models.CATALOGO, pid) if pid else None
        if request.method == "POST":
            f = request.form
            nombre = f.get("nombre", "").strip()
            categoria = f.get("categoria", "")
            precio_txt = f.get("precio", "").strip()
            if not nombre:
                flash("El nombre del producto es obligatorio.")
                return render_template("admin/producto.html", p=p,
                                       categorias=[c[0] for c in models.CATEGORIAS])
            if categoria not in [c[0] for c in models.CATEGORIAS]:
                flash("Selecciona una categoría válida.")
                return render_template("admin/producto.html", p=p,
                                       categorias=[c[0] for c in models.CATEGORIAS])
            try:
                precio = float(precio_txt) if precio_txt else None
            except ValueError:
                precio = -1
            if precio is not None and (not math.isfinite(precio) or precio < 0):
                flash("El precio debe ser un número igual o mayor que cero.")
                return render_template("admin/producto.html", p=p,
                                       categorias=[c[0] for c in models.CATEGORIAS])
            destacados_actuales = sum(x["destacado"] and x is not p for x in models.CATALOGO)
            destacado = "destacado" in f
            if destacado and destacados_actuales >= 4:
                flash("El catálogo admite hasta cuatro productos destacados.")
                return render_template("admin/producto.html", p=p,
                                       categorias=[c[0] for c in models.CATEGORIAS])
            datos = dict(nombre=nombre, categoria=categoria, descripcion=f.get("descripcion", "").strip(),
                         precio=precio, destacado=destacado)
            foto = request.files.get("imagen")
            if foto and foto.filename:
                extension = secure_filename(foto.filename).rsplit(".", 1)
                if len(extension) != 2 or extension[1].lower() not in EXTENSIONES_IMAGEN:
                    flash("La imagen debe ser JPG, PNG o WEBP.")
                    return render_template("admin/producto.html", p=p,
                                           categorias=[c[0] for c in models.CATEGORIAS])
                nombre_archivo = f"{uuid.uuid4().hex}.{extension[1].lower()}"
                foto.save(os.path.join(current_app.static_folder, "img", nombre_archivo))
                datos["imagen"] = nombre_archivo
            if p:
                p.update(datos)
            else:
                datos.setdefault("imagen", "capas.jpg")
                models.CATALOGO.append(dict(id=models.nuevo_id(models.CATALOGO), **datos))
            models.guardar_datos()
            flash("Producto guardado.")
            return redirect(url_for("admin.catalogo"))
        return render_template("admin/producto.html", p=p, categorias=[c[0] for c in models.CATEGORIAS])

    @staticmethod
    @bp.route("/catalogo/<int:pid>/eliminar", methods=["POST"])
    @solo_dueno
    def producto_eliminar(pid):
        models.CATALOGO.remove(_buscar(models.CATALOGO, pid))
        models.guardar_datos()
        flash("Producto eliminado.")
        return redirect(url_for("admin.catalogo"))

    # ---------- Calendario de entregas ----------
    @staticmethod
    @bp.route("/calendario")
    @solo_dueno
    def calendario():
        h = date.today()
        try:
            a, m = map(int, request.args.get("m", f"{h.year}-{h.month}").split("-"))
            date(a, m, 1)
        except ValueError:
            a, m = h.year, h.month
        dias = {}
        for p in models.PEDIDOS:
            if p["entrega"] and p["entrega"][:7] == f"{a}-{m:02d}":
                dias.setdefault(int(p["entrega"][8:]), []).append(p)
        ant = (a - 1, 12) if m == 1 else (a, m - 1)
        sig = (a + 1, 1) if m == 12 else (a, m + 1)
        return render_template("admin/calendario.html", semanas=calendar.Calendar(0).monthdayscalendar(a, m), dias=dias,
                               titulo=f"{MESES[m-1].capitalize()} {a}", ant=f"{ant[0]}-{ant[1]}", sig=f"{sig[0]}-{sig[1]}",
                               hoy=h.day if (h.year, h.month) == (a, m) else 0,
                               sin_fecha=[p for p in models.PEDIDOS if not p["entrega"]])
