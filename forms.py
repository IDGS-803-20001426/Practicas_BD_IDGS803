from wtforms import Form
from wtforms import StringField, SelectField, RadioField, EmailField, IntegerField, FloatField, DateField, BooleanField
from wtforms import validators

class UsersForm(Form):
    id=IntegerField(id)
    nombre=StringField('nombre', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=10, message='Ingresa nombre valido')
    ])
    email=EmailField('correo', [
        validators.Email(message='Ingrese un correo valido')
    ])
    telefono=StringField('telefono', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=10, max=10, message='Ingresa un teléfono valido')
    ])

    direccion=StringField('direccion', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=1, max=200, message='Ingresa una dirección valida')
    ])

    sueldo=FloatField('sueldo', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(max=10, message='Ingresa un sueldo valido')
    ])

class DatosForm(Form):
    id=IntegerField(id)
    nombre=StringField('nombre', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=10, message='Ingresa nombre valido')
    ])
    direccion=StringField('direccion', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=10, message='Ingresa una dirección valido')
    ])
    telefono=StringField('telefono', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=10, max=10, message='Ingresa un teléfono valido')
    ])
    fechaCompra=DateField('Fecha Compra', [
        validators.DataRequired(message='El campo es requerido')
    ])

class VentaForm(Form):
    id=IntegerField(id)
    opciones = [('dia', 'Día'), ('mes', 'Mes'), ('anio', 'Año')]
    selectVenta = SelectField('Selecciona El filtro', choices=opciones, id='select_venta', validators=[
        validators.DataRequired(message='El campo es requerido')
    ])  
    dia_semana = SelectField('Día de la semana', choices=[('lunes', 'Lunes'), ('martes', 'Martes'), ('miercoles', 'Miércoles'), ('jueves', 'Jueves'), ('viernes', 'Viernes'), ('sabado', 'Sábado'), ('domingo', 'Domingo')], validators=[
        validators.DataRequired(message='El campo es requerido')
    ])  
    mes = SelectField('Mes', choices=[('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'), ('4', 'Abril'), ('5', 'Mayo'), ('6', 'Junio'), ('7', 'Julio'), ('8', 'Agosto'), ('9', 'Septiembre'), ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre')], validators=[
        validators.DataRequired(message='El campo es requerido')
    ])  
    anio = StringField('Año', default=2024, validators=[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=4, message='Ingresa año valido')
    ])  


class PizzaForm(Form):
    id=IntegerField(id)
    tamano=RadioField('tamaño',
                          choices=[('chica', 'Chica $40'),('mediana', 'Mediana $80'),('grande', 'Grande $120')])
    
    checkJamon=BooleanField('Jamón $10')
    checkPina=BooleanField('Piña $10')
    checkChamp=BooleanField('Champiñones $10')

    numPizzas=IntegerField('Cantidad Pizzas',[
        validators.DataRequired(message='El campo es requerido')
    ])

    def validate(self):
        # Llamamos al método validate de la clase base
        if not Form.validate(self):
            return False

        # Validamos que al menos uno de los checks esté seleccionado
        if not (self.checkJamon.data or self.checkPina.data or self.checkChamp.data):
            message = 'Selecciona al menos un ingrediente'
            self.checkJamon.errors.append(message)
            self.checkPina.errors.append(message)
            self.checkChamp.errors.append(message)
            return False

        return True

