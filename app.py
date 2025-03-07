from flask import Flask, render_template, request, redirect, url_for,g
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from models import Alumno
from models import db
import forms

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.route("/")
@app.route("/index")
def index():
    create_form=forms.UserForm2(request.form)
    alumno=Alumno.query.all() # select * from alumnos
    return render_template("index.html",form=create_form,alumnos=alumno)

@app.route("/detalles",methods=['GET','POST'])
def detalles():
    create_form=forms.UserForm2(request.form)
    if request.method == 'GET':
        id=request.args.get('id')
        alumno=db.session.query(Alumno).filter(Alumno.id==id).first()
        nom=alumno.nombre
        ape=alumno.apaterno
        email=alumno.email
    return render_template("detalles.html",form=create_form,nom=nom,ape=ape,email=email)

@app.route("/eliminar",methods=['GET','POST'])
def eliminar():
    create_form=forms.UserForm2(request.form)
    if request.method == 'GET':
        id=request.args.get('id')
        alumno=db.session.query(Alumno).filter(Alumno.id==id).first()
        create_form.id.data=request.args.get('id')
        create_form.nombre.data = str.rstrip(alumno.nombre)
        create_form.apaterno.data = alumno.apaterno
        create_form.email.data = alumno.email
    if request.method == 'POST':
        id=create_form.id.data
        alumno=db.session.query(Alumno).filter(Alumno.id==id).first()
        db.session.delete(alumno)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("eliminar.html",form=create_form)

@app.route("/nuevoAlumno",methods=['GET','POST'])
def nuevoAlumno():
    create_form=forms.UserForm2(request.form)
    if request.method == 'POST':
        alumno=Alumno(
        nombre=create_form.nombre.data,
        apaterno=create_form.apaterno.data,
        email=create_form.email.data)
        db.session.add(alumno)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("nuevoAlumno.html",form=create_form)

@app.route('/modificar',methods=['GET','POST'])
def modificar():
    create_form=forms.UserForm2(request.form)
    if request.method == 'GET':
        id=request.args.get('id')
        alumno=db.session.query(Alumno).filter(Alumno.id==id).first()
        create_form.id.data=request.args.get('id')
        create_form.nombre.data = str.rstrip(alumno.nombre)
        create_form.apaterno.data = alumno.apaterno
        create_form.email.data = alumno.email
    if request.method == 'POST':
        id=create_form.id.data
        alumno=db.session.query(Alumno).filter(Alumno.id==id).first()
        alumno.id=id
        alumno.nombre=str.rstrip(create_form.nombre.data)
        alumno.apaterno=create_form.apaterno.data
        alumno.email=create_form.email.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("modificar.html",form=create_form)

if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app) 
    with app.app_context():
        db.create_all()
    app.run()