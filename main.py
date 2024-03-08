from flask import Flask, render_template,request, Response, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from flask import redirect
from flask import g
from sqlalchemy import func
from datetime import datetime

from config import DevelopmentConfig

from flask import flash
import forms

from models import db
from models import Empleados
from models import detalle
from models import venta

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

@app.route("/pizzas", methods=["GET", "POST"])
def pizzas():
    datos_form=forms.DatosForm(request.form)
    pizza_form=forms.PizzaForm(request.form)
    ventas_form=forms.VentaForm(request.form)
    
    if request.method == 'POST' and pizza_form.validate():
        subt = 0
        ingredientes = ''
        precioBase = 0
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

        if pizza_form.tamano.data == 'chica':
            precioBase = 40

        if pizza_form.tamano.data == 'mediana':
            precioBase = 80

        if pizza_form.tamano.data == 'grande':
            precioBase = 120

        det = detalle(
            tamano=pizza_form.tamano.data,
            ingredientes=ingredientes,
            cantPizzas = pizza_form.numPizzas.data,
            subtotal = (subt + precioBase) * pizza_form.numPizzas.data,
            activo = True
        )
        db.session.add(det)
        db.session.commit();

    deta = detalle.query.filter_by(activo=True).all()

    # Obtener la fecha actual
    hoy = datetime.now().date()



    return render_template("pizzas.html", form=pizza_form, form_datos=datos_form, detalle=deta,form_ventas=ventas_form);

@app.route('/eliminar_registros', methods=['POST'])
def eliminar_registros():
    pizza_form=forms.PizzaForm(request.form)
    deta = detalle.query.filter_by(activo=True).all()

    if request.method == 'POST':
        ids_a_eliminar = request.form.getlist('eliminar')
        
        for id in ids_a_eliminar:
            det=detalle.query.get(id)
            db.session.delete(det)
            db.session.commit()

    return redirect(url_for('pizzas'))

@app.route("/modificarPizza", methods=["GET", "POST"])
def modificarPizza():
    pizza_form=forms.PizzaForm(request.form)
    if request.method=="GET":
        id=request.args.get("id")
        pizza1=db.session.query(detalle).filter(detalle.id==id).first()

        pizza_form.id.data=request.args.get("id")
        pizza_form.tamano.data=pizza1.tamano
        pizza_form.numPizzas.data=pizza1.cantPizzas

        pizza_form.checkJamon.data = True if "Jamón" in pizza1.ingredientes else False
        pizza_form.checkPina.data = True if "Piña" in pizza1.ingredientes else False
        pizza_form.checkChamp.data = True if "Champiñones" in pizza1.ingredientes else False

    if request.method=='POST':
        subt = 0
        ingredientes = ''
        precionBase = 0
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

        if pizza_form.tamano.data == 'chica':
            precioBase = 40

        if pizza_form.tamano.data == 'mediana':
            precioBase = 80

        if pizza_form.tamano.data == 'grande':
            precioBase = 120

        id=pizza_form.id.data
        pizza1=db.session.query(detalle).filter(detalle.id==id).first()

        pizza1.tamano=pizza_form.tamano.data
        pizza1.cantPizzas=pizza_form.numPizzas.data
        pizza1.ingredientes=ingredientes
        pizza1.subtotal=(subt + precioBase) * pizza_form.numPizzas.data

        db.session.add(pizza1)
        db.session.commit()
        return redirect('pizzas')
    
    return render_template("modificarPizza.html", form=pizza_form)

@app.route("/finalizarCompra", methods=["GET", "POST"])
def finalizarCompra():
    datos_form=forms.DatosForm(request.form)
    pizza_form=forms.PizzaForm(request.form)
    ventas_form=forms.VentaForm(request.form)

    if request.method == "POST" and datos_form.validate():
        ven = venta(
            nombre=datos_form.nombre.data,  
            direccion=datos_form.direccion.data,  
            fechaCompra=datos_form.fechaCompra.data,    
            telefono=datos_form.telefono.data,    
        )
        db.session.add(ven)
        db.session.commit();

        nuevo_id = ven.id
        detalles = detalle.query.filter_by(activo=True).all()
        for det in detalles:
            det.activo = False
            det.idVenta = nuevo_id
            db.session.add(ven)
        db.session.commit();
    
    deta = detalle.query.filter_by(activo=True).all()

    # Obtener la fecha actual
    hoy = datetime.now().date()

    return redirect(url_for('pizzas'))


@app.route("/filtrar-venta", methods=["GET", "POST"])
def filtrar():
    ventas_form=forms.VentaForm(request.form)
    datos_form=forms.DatosForm(request.form)
    pizza_form=forms.PizzaForm(request.form)
    deta = detalle.query.filter_by(activo=True).all()
    resultados = None
    if request.method == 'POST' and ventas_form.validate():
        filtro_seleccionado = ventas_form.selectVenta.data

        print(filtro_seleccionado)

              # Inicializar la consulta base
        base_query = db.session.query(
            venta.id,
            venta.nombre,
            func.sum(detalle.subtotal).label('total'),
            func.DATE_FORMAT(venta.fechaCompra, '%W, %d de %M').label('fechaCompra')
        ).join(detalle, venta.id == detalle.idVenta)

        if filtro_seleccionado == 'dia':
            # Obtener el valor del día del formulario
            dia_seleccionado = ventas_form.dia_semana.data
            # Agregar filtro por día a la consulta
            base_query = base_query.filter(func.DAYNAME(venta.fechaCompra) == dia_seleccionado.capitalize())
        
        elif filtro_seleccionado == 'mes':
            # Obtener el valor del mes del formulario
            mes_seleccionado = ventas_form.mes.data
            # Agregar filtro por mes a la consulta
            base_query = base_query.filter(func.MONTH(venta.fechaCompra) == mes_seleccionado)
        
        elif filtro_seleccionado == 'anio':
            # Obtener el valor del año del formulario
            anio_seleccionado = ventas_form.anio.data
            # Agregar filtro por año a la consulta
            base_query = base_query.filter(func.YEAR(venta.fechaCompra) == int(anio_seleccionado))
        
        
        
        # Ejecutar la consulta final
        resultados = base_query.group_by(venta.id, venta.nombre, venta.fechaCompra).all()

        suma_totales = sum(item[2] for item in resultados)

    return render_template("pizzas.html", form=pizza_form, form_datos=datos_form, ventas=resultados, detalle=deta, form_ventas=ventas_form, total=suma_totales)



if __name__=="__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()