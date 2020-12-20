from flask import Flask, render_template, url_for, flash, redirect, session
from systemdb import init_db
from forms import formulario_login
from werkzeug import security
from usuarios_service import usuario_by_username

app = Flask(__name__)
init_db()
app.config.update(SECRET_KEY="GRUPO3-R")

rutas_admin = [["/", "Inicio"], ["/logout", "Salir"]]
rutas_no_user = [["/login", "Login"]]


@app.route("/")
def index():
    if "rol" in session:
        session["rutas"] = rutas_admin
    else:
        session["rutas"] = rutas_no_user
    return render_template("index.html")


@app.route("/login", methods=("GET", "POST"))
def login():
    if "rol" in session:
        return redirect(url_for("index"))

    form = formulario_login()

    if form.validate_on_submit():
        username = form.usuario.data
        password = form.password.data
        usuariodb = usuario_by_username(username)
        if (usuariodb is not None) and (security.check_password_hash(usuariodb[1], password)):
            session["rol"] = usuariodb[3]
            session["rutas"] = rutas_admin
            return redirect(url_for("index"))
        else:
            session["rutas"] = rutas_no_user
            flash("Usuario o contraseña incorrectos")

    return render_template("login.html", form=form)


@app.route("/logout", methods=("GET", "POST"))
def logout():
    if "rol" in session:
        session.pop("rol", None)
        session["rutas"] = rutas_no_user
        return redirect(url_for("index"))
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)
