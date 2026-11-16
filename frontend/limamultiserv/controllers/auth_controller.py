import re
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
import models


class AuthController:
    """Inicio de sesión, registro y cierre de sesión."""
    bp = Blueprint("auth", __name__)

    @staticmethod
    def es_dueno(correo):
        return correo.lower() in models.CORREOS_DUENOS

    @staticmethod
    @bp.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            correo = request.form.get("correo", "").strip().lower()
            clave = request.form.get("clave", "")
            u = models.USUARIOS.get(correo)
            if u and check_password_hash(u["hash"], clave):
                session.clear()
                session.update(correo=correo, nombre=u["nombre"], dueno=AuthController.es_dueno(correo))
                # Dueña -> panel administrativo; cliente -> panel personal
                return redirect(url_for("admin.panel" if session["dueno"] else "cuenta.panel"))
            flash("Correo o contraseña incorrectos. Revisa tus datos e inténtalo de nuevo.")
        return render_template("auth/login.html", correo=request.form.get("correo", ""))

    @staticmethod
    @bp.route("/registro", methods=["GET", "POST"])
    def registro():
        if request.method == "POST":
            nombre = request.form.get("nombre", "").strip()
            correo = request.form.get("correo", "").strip().lower()
            clave = request.form.get("clave", "")
            if not nombre or len(nombre) > 100:
                flash("Ingresa tu nombre completo (máximo 100 caracteres).")
            elif (len(correo) > 254
                  or not re.fullmatch(r"[^@\s]+@[^@\s.]+(?:\.[^@\s.]+)+", correo)):
                flash("Ingresa un correo electrónico válido.")
            elif len(clave) < 6 or len(clave) > 128:
                flash("La contraseña debe tener entre 6 y 128 caracteres.")
            elif correo in models.USUARIOS or correo in models.CORREOS_DUENOS:
                flash("Este correo ya está registrado.")
            else:  # los registros públicos siempre son clientes
                models.USUARIOS[correo] = {"nombre": nombre,
                                           "hash": generate_password_hash(clave)}
                models.CLIENTES.append(dict(nombre=nombre, correo=correo, telefono=""))
                models.guardar_datos()
                flash("Cuenta creada. Ya puedes iniciar sesión.")
                return redirect(url_for("auth.login"))
        return render_template("auth/registro.html", nombre=request.form.get("nombre", ""),
                               correo=request.form.get("correo", ""))

    @staticmethod
    @bp.route("/salir")
    def salir():
        session.clear()
        return redirect(url_for("cliente.inicio"))
