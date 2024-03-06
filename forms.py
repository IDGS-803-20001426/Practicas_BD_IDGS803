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

class PizzaForm(Form):
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
    tamano=RadioField('tamaño',
                          choices=[('Chica', 'Chica $40'),('Mediana', 'Mediana $80'),('Grande', 'Grande $120')])
    
    checkJamon=BooleanField('Jamón $10')
    checkPina=BooleanField('Piña $10')
    checkChamp=BooleanField('Champiñones $10')

    numPizzas=IntegerField('Cantidad Pizzas',[
        validators.DataRequired(message='El campo es requerido')
    ])

