from wtforms import Form, StringField, PasswordField, BooleanField, SelectField, SubmitField, validators, IntegerField, DateField, TimeField
from wtforms.fields.html5 import EmailField

class Registro_usuario(Form):
    tipo_usuario = SelectField("Tipo de usuario",[validators.Required()],choices=[("Natural","Persona Natural"),("Juridica","Persona Juridica")])
    tipo_id = SelectField("Tipo de identificación del usuario",[validators.Required()],choices=[("c.c","Cedula"),("Nit","Nit"),("Ps","Pasaporte"),("t.i","Tarjeta De Identidad")])
    usuario = StringField('Nombre del usuario: ', 
    [ 
        validators.DataRequired(), 
        validators.Length(min=8,max=25)
    ] )
    password = PasswordField('Contraseña: ',
    [ 
        validators.DataRequired(), 
        validators.Length(min=8,max=25) 
    ])
    no_id = IntegerField('Número de identifiación del usuario: ', 
    [ 
        validators.DataRequired(), 

    ] )
    email = EmailField( 'Email' )
    recordar = BooleanField('Terminos y Condiciones')
    registro = SubmitField('Registrarse')

class Login(Form):
    t_usuario_login = SelectField("Tipo de usuario",[validators.Required()],choices=[("Paciente","Paciente"),("Medico","Medico"),("Administrador","Administrador")])
    t_id_login = SelectField("Tipo de identificación del usuario",[validators.Required()],choices=[("c.c","Cedula"),("Nit","Nit"),("Ps","Pasaporte"),("t.i","Tarjeta De Identidad")])
    no_id_login = IntegerField('Número de identifiación del usuario: ', 
    [ 
        validators.DataRequired(), 

    ] )
    password_login = PasswordField('Contraseña: ',
    [ 
        validators.DataRequired(), 
        validators.Length(min=8,max=25) 
    ])
    ingresar_login = SubmitField('Ingresar')

class Registrar_cita(Form):
    motivo = StringField('Motivo de la cita: ', 
    [ 
        validators.DataRequired(), 
        validators.Length(min=5,max=500)
    ] ) 
    descripcion = StringField('Descripción o Sintomas: ', 
    [ 
        validators.DataRequired(), 
        validators.Length(min=5,max=500)
    ] ) 
    date = DateField('Fecha de la cita: ')
    start_time = TimeField('Hora de la cita: ')
    end_time = TimeField('Hora terminación cita: ')
    estado = SelectField("Estado de la cita: ",[validators.Required()],choices=[("Pendiente","Pendiente"),("Progreso","En Progreso"),("Finalizado","Finalizado")])
    id_paciente = IntegerField('Número de identifiación del paciente: ', 
    [ 
        validators.DataRequired(), 

    ] )
    id_medico = IntegerField('Número de identifiación del medico: ', 
    [ 
        validators.DataRequired(), 

    ] )
    direccion = StringField('Dirección: ', 
    [ 
        validators.DataRequired(), 
    ] ) 
    ciudad = StringField('Ciudad: ', 
    [ 
        validators.DataRequired(), 
    ] ) 
    celular = IntegerField('Número de celular: ', 
    [ 
        validators.DataRequired(), 

    ] )
    vez = SelectField("Es su primera Consulta : ",[validators.Required()],choices=[("si","Si"),("no","No")])
    especialidad = SelectField("Seleccione consulta : ",[validators.Required()],choices=[("General","General"),("Especializada","Especializada")])
    comentarios = StringField('Algo extra para tu consulta: ') 
    valoracion = SelectField("Seleccione satisfacción: ",choices=[("",""),("1","1"),("2","2"),("3","3"),("4","4"),("5","5")])
    registro_cita = SubmitField('Registrar')

class Detalle_cita(Form):
    id_paciente = IntegerField('Número de identifiación del paciente: ', 
    [ 
        validators.DataRequired(), 

    ] )
    buscar = SubmitField('Buscar')

class Registro_medicos(Form):
    nombre = StringField('Nombre del medico: ', 
    [ 
        validators.DataRequired(), 
        validators.Length(min=4,max=25)
    ] )
    t_id_login = SelectField("Tipo de identificación del medico",[validators.Required()],choices=[("c.c","Cedula"),("Nit","Nit"),("Ps","Pasaporte"),("t.i","Tarjeta De Identidad")])
    no_id_login = IntegerField('Número de identifiación del medico: ', 
    [ 
        validators.DataRequired(), 

    ] )
    email = EmailField( 'Email' )
    password = PasswordField('Contraseña: ',
    [ 
        validators.DataRequired(), 
        validators.Length(min=8,max=25) 
    ])
    especialidad = IntegerField('Especialidad *Mirar tabla especialidad: ', 
    [ 
        validators.DataRequired(), 

    ] )
    registro = SubmitField('Registrar')

class Borrar(Form):
    no_id_login = IntegerField('Número de ID: ', 
    [ 
        validators.DataRequired(), 

    ] )
    registro = SubmitField('Borrar')