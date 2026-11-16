from functools import wraps
from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import models


def solo_cliente(vista):
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if "correo" not in session:
            return redirect(url_for("auth.login"))
        if session.get("dueno"):
            return redirect(url_for("admin.panel"))
        return vista(*args, **kwargs)
    return envoltura


def _pedidos_cliente(correo):
    return sorted(
        (p for p in models.PEDIDOS if p.get("correo") == correo),
        key=lambda p: -p["id"])


class CuentaController:
    """Panel personal y perfil de los clientes."""
    bp = Blueprint("cuenta", __name__, url_prefix="/cuenta")

    @staticmethod
    @bp.route("/")
    @solo_cliente
    def panel():
        correo = session["correo"]
        cliente = next((c for c in models.CLIENTES if c["correo"] == correo), None)
        if cliente is None:
            abort(404)
        pedidos = _pedidos_cliente(correo)
        return render_template("cuenta/panel.html", cliente=cliente, pedidos=pedidos[:5],
                               total=len(pedidos),
                               pendientes=sum(p["estado"] == "Pendiente" for p in pedidos))

    @staticmethod
    @bp.route("/pedidos")
    @solo_cliente
    def pedidos():
        return render_template("cuenta/pedidos.html",
                               pedidos=_pedidos_cliente(session["correo"]))

    @staticmethod
    @bp.route("/solicitud")
    @solo_cliente
    def solicitud():
        return render_template("cuenta/solicitud.html")

    @staticmethod
    @bp.route("/perfil", methods=["GET", "POST"])
    @solo_cliente
    def perfil():
        correo = session["correo"]
        cliente = next((c for c in models.CLIENTES if c["correo"] == correo), None)
        usuario = models.USUARIOS.get(correo)
        if cliente is None or usuario is None:
            abort(404)

        nombre = request.form.get("nombre", cliente["nombre"]).strip()
        telefono = request.form.get("telefono", cliente.get("telefono", "")).strip()
        if request.method == "POST":
            clave_actual = request.form.get("clave_actual", "")
            clave_nueva = request.form.get("clave_nueva", "")
            confirmar_clave = request.form.get("confirmar_clave", "")
            if not nombre or len(nombre) > 100:
                flash("Ingresa tu nombre completo (máximo 100 caracteres).")
            elif len(telefono) > 30:
                flash("El teléfono no puede superar los 30 caracteres.")
            elif clave_nueva and not check_password_hash(usuario["hash"], clave_actual):
                flash("La contraseña actual no es correcta.")
            elif clave_nueva and not 6 <= len(clave_nueva) <= 128:
                flash("La nueva contraseña debe tener entre 6 y 128 caracteres.")
            elif clave_nueva != confirmar_clave:
                flash("La nueva contraseña y su confirmación no coinciden.")
            else:
                cliente["nombre"] = nombre
                cliente["telefono"] = telefono
                usuario["nombre"] = nombre
                if clave_nueva:
                    usuario["hash"] = generate_password_hash(clave_nueva)
                for pedido in models.PEDIDOS:
                    if pedido.get("correo") == correo:
                        pedido["cliente"] = nombre
                session["nombre"] = nombre
                models.guardar_datos()
                flash("Tu perfil se actualizó correctamente.")
                return redirect(url_for("cuenta.perfil"))

        return render_template("cuenta/perfil.html", cliente=cliente, nombre=nombre,
                               telefono=telefono)
