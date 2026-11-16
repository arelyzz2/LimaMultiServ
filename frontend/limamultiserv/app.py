import os
from flask import Flask, render_template
from controllers.auth_controller import AuthController
from controllers.cliente_controller import ClienteController
from controllers.admin_controller import AdminController
from controllers.cuenta_controller import CuentaController
import models


def crear_app(config=None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get("FLASK_SECRET_KEY", "dev-key-change-me"),
        MAX_CONTENT_LENGTH=10 * 1024 * 1024,
        DATABASE_PATH=os.environ.get(
            "DATABASE_PATH", os.path.join(app.instance_path, "limamultiserv.sqlite3")),
        UPLOAD_FOLDER=os.path.join(app.instance_path, "uploads"),
    )
    if config:
        app.config.update(config)
    models.iniciar_base_datos(app.config["DATABASE_PATH"])
    for c in (AuthController, ClienteController, AdminController, CuentaController):
        app.register_blueprint(c.bp)

    @app.template_filter("fecha")
    def fecha(v):
        return f"{v[8:]}/{v[5:7]}/{v[:4]}" if v else "Por coordinar"

    @app.errorhandler(403)
    def prohibido(_):
        return render_template("auth/login.html"), 403
    return app


if __name__ == "__main__":
    crear_app().run(debug=True)
