from flask import Flask, render_template,request, Response
from flask_wtf.csrf import CSRFProtect
from flask import redirect
from flask import g

from config import DevelopmentConfig

from flask import flash
import forms

from models import db
from models import Empleados
from models import detalle

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()

@app.errorhandler(404)
def page_no_found(e):
    return render_template("404.html"),404


@app.route("/index",methods=["GET", "POST"])
def index():
    emp_form=forms.UsersForm(request.form)
    if request.method == 'POST':
        emp = Empleados(
            nombre=emp_form.nombre.data,
            email=emp_form.email.data,
            telefono = emp_form.telefono.data,
            direccion = emp_form.direccion.data,
            sueldo = emp_form.sueldo.data,
        )
        db.session.add(emp)
        db.session.commit();

    return render_template("index.html", form=emp_form)

@app.route("/eliminar", methods=["GET", "POST"])
def eliminar():
    emp_form=forms.UsersForm(request.form)
    if request.method=="GET":
        id=request.args.get("id")
        emp1=db.session.query(Empleados).filter(Empleados.id==id).first()

        emp_form.id.data=request.args.get("id")
        emp_form.nombre.data=emp1.nombre
        emp_form.email.data=emp1.email
        emp_form.telefono.data=emp1.telefono
        emp_form.direccion.data=emp1.direccion
        emp_form.sueldo.data=emp1.sueldo
    
    if request.method=='POST':
        id=emp_form.id.data
        alum=Empleados.query.get(id)
        db.session.delete(alum)
        db.session.commit()
        return redirect('ABC_Completo')
    
    return render_template("eliminar.html", form=emp_form)

@app.route("/modificar", methods=["GET", "POST"])
def modificar():
    emp_form=forms.UsersForm(request.form)
    if request.method=="GET":
        id=request.args.get("id")
        emp1=db.session.query(Empleados).filter(Empleados.id==id).first()

        emp_form.id.data=request.args.get("id")
        emp_form.nombre.data=emp1.nombre
        emp_form.email.data=emp1.email
        emp_form.telefono.data=emp1.telefono
        emp_form.direccion.data=emp1.direccion
        emp_form.sueldo.data=emp1.sueldo
    
    if request.method=='POST':
        id=emp_form.id.data
        emp1=db.session.query(Empleados).filter(Empleados.id==id).first()
        emp1.nombre=emp_form.nombre.data
        emp1.email=emp_form.email.data
        emp1.telefono=emp_form.telefono.data
        emp1.direccion=emp_form.direccion.data
        emp1.sueldo=emp_form.sueldo.data
        db.session.add(emp1)
        db.session.commit()
        return redirect('ABC_Completo')
    
    return render_template("modificar.html", form=emp_form)

@app.route("/ABC_Completo", methods=["GET", "POST"])
def ABC_Completo():
    emp_form=forms.UsersForm(request.form)
    empleado=Empleados.query.all()
    return render_template("ABC_Completo.html", empleado=empleado)

@app.route('/eliminar_registros', methods=['POST'])
def eliminar_registros():
    pizza_form=forms.PizzaForm(request.form)
    deta = detalle.query.filter_by(activo=True).all()

    if request.method == 'POST':
        ids_a_eliminar = request.form.getlist('eliminar')
        
        print(ids_a_eliminar)

    return render_template("pizzas.html", form=pizza_form, detalle=deta);

@app.route("/pizzas", methods=["GET", "POST"])
def pizzas():
    pizza_form=forms.PizzaForm(request.form)
    deta = detalle.query.filter_by(activo=True).all()

    if request.method == 'POST':
        subt = 0
        ingredientes = ''
        check_jamon = pizza_form.checkJamon.data
        check_pina = pizza_form.checkPina.data
        check_champ = pizza_form.checkChamp.data

        if check_jamon:
            subt += 10
            ingredientes = "Jamón-"

        if check_pina:
            subt += 10
            ingredientes += "Piña-"

        if check_champ:
            subt += 10
            ingredientes += 'Champiñones'

        det = detalle(
            tamano=pizza_form.tamano.data,
            ingredientes=ingredientes,
            cantPizzas = pizza_form.numPizzas.data,
            subtotal = (subt * pizza_form.numPizzas.data) + int(pizza_form.tamano.data),
            activo = True
        )
        db.session.add(det)
        db.session.commit();

    return render_template("pizzas.html", form=pizza_form, detalle=deta);

if __name__=="__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()