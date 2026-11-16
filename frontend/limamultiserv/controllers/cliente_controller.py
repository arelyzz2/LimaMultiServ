import os
import uuid
from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from flask import current_app
from werkzeug.utils import secure_filename
import models

EXTENSIONES_IMAGEN = {"jpg", "jpeg", "png", "webp"}


class ClienteController:
    """Página pública: se puede ver sin iniciar sesión."""
    bp = Blueprint("cliente", __name__)

    @staticmethod
    @bp.route("/")
    def inicio():
        categoria = request.args.get("categoria", "").strip()
        busqueda = request.args.get("q", "").strip()
        categorias = [c[0] for c in models.CATEGORIAS]
        if categoria not in categorias:
            categoria = ""
        productos = list(models.CATALOGO)
        if categoria:
            productos = [p for p in productos if p["categoria"] == categoria]
        if busqueda:
            termino = busqueda.casefold()
            productos = [
                p for p in productos
                if termino in " ".join(
                    (p["nombre"], p["categoria"], p["descripcion"])).casefold()
            ]
        elif not categoria:
            productos = [p for p in models.CATALOGO if p["destacado"]][:4]
        return render_template("cliente/inicio.html", categorias=models.CATEGORIAS,
                               productos=productos, categoria=categoria,
                               busqueda=busqueda, precio=models.precio_txt)

    @staticmethod
    @bp.route("/pedido-personalizado", methods=["POST"])
    def pedido_personalizado():
        if "correo" not in session:  # solo clientes registrados pueden pedir
            flash("Para solicitar un pedido primero inicia sesión o regístrate.")
            return redirect(url_for("auth.login"))
        f = request.form
        tipos = {"Capa patronal", "Banda de honor", "Bandera", "Banderola", "Otra prenda"}
        tipo = f.get("tipo", "")
        if tipo not in tipos:
            flash("Selecciona un tipo de confección válido.")
            return redirect(url_for("cuenta.solicitud"))
        adjuntos_pendientes = []
        for campo, etiqueta in (("logo", "Logo o diseño"), ("referencia", "Imagen de referencia")):
            archivo = request.files.get(campo)
            if archivo and archivo.filename:
                extension = secure_filename(archivo.filename).rsplit(".", 1)
                if len(extension) != 2 or extension[1].lower() not in EXTENSIONES_IMAGEN:
                    flash("Las imágenes deben estar en formato JPG, PNG o WEBP.")
                    return redirect(url_for("cuenta.solicitud"))
                adjuntos_pendientes.append((etiqueta, extension[1].lower(), archivo))

        carpeta = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(carpeta, exist_ok=True)
        adjuntos = []
        for etiqueta, extension, archivo in adjuntos_pendientes:
            nombre_archivo = f"{uuid.uuid4().hex}.{extension}"
            archivo.save(os.path.join(carpeta, nombre_archivo))
            adjuntos.append({"etiqueta": etiqueta, "filename": nombre_archivo})

        det = (f"Tela: {f.get('tela', '').strip()}. Medidas: {f.get('medidas', '').strip()}. "
               f"Colores: {f.get('colores', '').strip()}. Acabado: {f.get('acabado', '').strip()}. "
               f"{f.get('descripcion', '').strip()}")
        models.PEDIDOS.append(dict(id=models.nuevo_id(models.PEDIDOS), cliente=session["nombre"],
                                   correo=session["correo"], tipo=tipo,
                                   entrega=None, estado="Pendiente", detalle=det, adjuntos=adjuntos))
        models.guardar_datos()
        # Sin cálculo de precios: el precio se coordina con el negocio.
        flash("Recibimos tu solicitud. Nos pondremos en contacto contigo para coordinar el precio.")
        return redirect(url_for("cuenta.pedidos"))
