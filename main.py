from flask import Flask, render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from tkinter import *
from tkinter import messagebox as MessageBox
#from flask_migrate import Migrate
import os, datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.abspath(os.getcwd()) +"/database.db"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = SQLAlchemy(app)
#migrate = Migrate(app, db)

#Models

from datetime import datetime

class TypeUser(db.Model):
    __tablename__ = "TypeUser"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        return f"{self.name}"

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    identification = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    cash = db.Column(db.Float, nullable=False)
    state = db.Column(db.Boolean, default=False)
    typeUser = db.Column(db.Integer, db.ForeignKey('TypeUser.id'))
    pubDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"{self.name}"

import jwt
def encryptPassword(password):
    encrypt = jwt.encode(
        {"password": f"{password}"}, 
        "Nació una flor a orillas de una fuente mas pura que la flor de la ilusión", 
        algorithm="HS256"
    )
    return encrypt

def comparePassword(username, password):
    try:
        user = User.query.filter_by(username=username).first()
        encrypt = jwt.encode(
            {"password": f"{password}"}, 
            "Nació una flor a orillas de una fuente mas pura que la flor de la ilusión", 
            algorithm="HS256"
        )
        if user.password == encrypt:
            return True
        else:
            return False
    except:
        return False


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/editar", methods=["POST", "GET"])
def editar():
    # hacer función que reciba en session user y devuelva true o false
    if not session.get("username"):
        return redirect("/index")
    else:
        user = User.query.filter_by(username=session.get("username")).first()

    if request.method == "POST":
        user = User.query.filter_by(username=session.get("username")).first()
        user.name = request.form.get("Name")
        user.username = request.form.get("Username")
        user.phone = request.form.get("Phone")
        user.email = request.form.get("Email")
        db.session.commit()
        return redirect("/")

    return render_template('editar.html', user_object=user)
  
  
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if comparePassword(request.form.get("username"), request.form.get("password")):
            # busque el objeto user por email y username, volverlo clav y guardarloen la sesion
            session["username"] = request.form.get("username")
            user = User.query.filter_by(username=request.form.get("username")).first()
            session["typeUser"] = user.typeUser
        else:
            MessageBox.showwarning("Advertencia","Contraseña Incorrecta")
    return render_template("/index.html")
  
@app.route("/logout")
def logout():
    session["username"] = None
    return redirect("/")

@app.route('/contacto')
def contacto_func():
    return render_template("public/contacto.html")

@app.route('/mision_vision')
def mision_vision_func():
    return render_template("public/mision_vision.html")

@app.route('/servicio')
def servicio_func():
    return render_template("public/servicio.html")

@app.route('/perfil_cliente', methods=["GET"])
def perfil_cliente_func():
    if not session.get("username"):
        return redirect("/login")
    else:
        user = User.query.filter_by(username=session.get("username")).first()
    return render_template("client/perfil_cliente.html", user_object=user)

@app.route('/gestionar_reserva', methods=["POST", "GET"])
def gestionar_reserva_func():
    return render_template("client/gestionar_reserva.html")

@app.route('/crear_reserva', methods=["POST", "GET"])
def crear_reserva_func():
    return render_template("client/crear_reserva.html")


@app.route('/perfil_administrador', methods=["GET"])
def perfil_administrador_func():
    if not session.get("username"):
        return redirect("/login")
    else:
        user = User.query.filter_by(username=session.get("username")).first()
    return render_template("admin/perfil_administrador.html", user_object=user)



if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)