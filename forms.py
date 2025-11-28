from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional, Regexp, NumberRange

class LoginForm(FlaskForm):

    email = StringField('Email', 
                        validators=[DataRequired(message='El email es obligatorio.'), 
                                    Email(message='Formato de email inválido.')])
    

    password = PasswordField('Contraseña', 
                             validators=[DataRequired(message='La contraseña es obligatoria.')])
    

    submit = SubmitField('Iniciar Sesión')
from wtforms.validators import Length

class MarcaForm(FlaskForm):

    nombre = StringField('Nombre de la Marca',
                         validators=[DataRequired(message='El nombre es obligatorio.'),
                                     Length(min=2, max=50, message='El nombre debe tener entre 2 y 50 caracteres.')])
    

    submit = SubmitField('Guardar Marca')


class TipoEquipoForm(FlaskForm):

    nombre = StringField('Nombre del Tipo de Equipo',
                         validators=[DataRequired(message='El nombre es obligatorio.'),
                                     Length(min=2, max=50, message='El nombre debe tener entre 2 y 50 caracteres.')])
    

    submit = SubmitField('Guardar Tipo')


class ClienteForm(FlaskForm):

    nombre = StringField('Nombre Completo',
                         validators=[DataRequired(message='El nombre es obligatorio.'),
                                     Length(min=3, max=150)])
    

    telefono = StringField('Teléfono / Celular',
                           validators=[DataRequired(message='El teléfono es obligatorio.'),
                                       Length(min=6, max=20),
                                       Regexp('^[0-9]+$', message='El teléfono debe contener solo números.')])
    

    email = StringField('Email',
                        validators=[Optional(),
                                    Length(max=120)])

    submit = SubmitField('Guardar Cliente')


class EquipoForm(FlaskForm):

    modelo = StringField('Modelo',
                         validators=[DataRequired(message='El modelo es obligatorio.'),
                                     Length(min=2, max=100)])
    

    serial = StringField('Número de Serie (Serial)',
                         validators=[DataRequired(message='El serial es obligatorio.'),
                                     Length(min=4, max=100)])


    


    
    cliente = SelectField('Cliente Propietario', coerce=int,
                           validators=[DataRequired(message='Debe seleccionar un cliente.')])
    
    marca = SelectField('Marca del Equipo', coerce=int,
                         validators=[DataRequired(message='Debe seleccionar una marca.')])
    
    tipo = SelectField('Tipo de Equipo', coerce=int,
                        validators=[DataRequired(message='Debe seleccionar un tipo.')])


    submit = SubmitField('Guardar Equipo')


class RepuestoForm(FlaskForm):

    nombre = StringField('Nombre del Repuesto',
                         validators=[DataRequired(message='El nombre es obligatorio.'),
                                     Length(min=2, max=100)])
    

    stock = IntegerField('Cantidad en Stock',
                         validators=[DataRequired(message='El stock es obligatorio.'),
                                     NumberRange(min=0, message='El stock no puede ser negativo.')])
    

    precio = FloatField('Precio de Venta',
                        validators=[DataRequired(message='El precio es obligatorio.'),
                                    NumberRange(min=0, message='El precio no puede ser negativo.')])


    submit = SubmitField('Guardar Repuesto')


class OrdenForm(FlaskForm):

    equipo = SelectField('Equipo a Reparar', coerce=int,
                         validators=[DataRequired(message='Debe seleccionar un equipo.')])
    

    problema = TextAreaField('Problema Reportado',
                             validators=[DataRequired(message='Describa el problema.'),
                                         Length(min=5)])
    

    submit = SubmitField('Crear Orden de Trabajo')


class UsuarioForm(FlaskForm):
    nombre = StringField('Nombre Completo', 
                         validators=[DataRequired(), Length(min=3, max=100)])
    
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    
    password = PasswordField('Contraseña',
                             validators=[Optional(), Length(min=6)]) 

    
    rol = SelectField('Rol del Usuario', coerce=int,
                      validators=[DataRequired()])
    
    submit = SubmitField('Guardar Usuario')