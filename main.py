from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import jsonify
from flask import session
from flask import g
import functools
from flask import send_file
from werkzeug.security import generate_password_hash, check_password_hash 
import os
from flask import redirect, url_for
from wtforms.validators import NoneOf
from utils import isUsernameValid, isEmailValid, isPasswordValid
import yagmail as yagmail
from forms import Registro_usuario, Login, Registrar_cita, Detalle_cita, Registro_medicos, Borrar, Historial
import sqlite3
from sqlite3 import Error
from db import get_db, close_db

app = Flask(__name__)
app.secret_key = os.urandom(24)
#app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

#funciones 

def sql_connection():
    try:
        conn = sqlite3.connect('dbClinica.db')
        print("¡Conexión OK!")
        return conn
    except Error:
        print(Error)

def select_historial_completo():
    sql = "SELECT * FROM historial"
    conn = sql_connection()
    cursorObj = conn.cursor()
    cursorObj.execute(sql)
    medicos = cursorObj.fetchall()
    return medicos

def delete_historial(id):
    sql = "DELETE FROM historial WHERE  cita = '{}'".format(id)
    print(sql)
    conn = sql_connection()
    cursoObj = conn.cursor()
    cursoObj.execute(sql)
    conn.commit()
    conn.close()

def edit_historial(cita, historial):
    sql = "UPDATE historial SET cita = '{}', historial = '{}' WHERE  cita = '{}'".format(cita, historial, cita)
    conn = sql_connection()
    cursoObj = conn.cursor()
    cursoObj.execute(sql)
    conn.commit()
    conn.close()

def insert_historial(cita, historial):
    sql = "INSERT INTO historial (cita, historial) VALUES ('{}', '{}')".format(cita, historial)
    conn = sql_connection()
    cursoObj = conn.cursor()
    cursoObj.execute(sql)
    conn.commit()
    conn.close()

def sql_citas_id():
    sql = "SELECT id, motivo_cita, descripcion, fecha, hora_cita, horario_salida, estado, id_paciente, idMedico, direccion, ciudad, celular, first_time, comentarios, valoracion FROM Citas "
    print(sql)
    conn = sql_connection()
    cursoObj = conn.cursor()
    cursoObj.execute(sql)
    citas = cursoObj.fetchall()
    lista_productos = [ {"ID": cita[0], "Motivo": cita[1], "Descipcion": cita[2], "Fecha": cita[3], "Hora_Inicial": cita[4], "Hora_Salida": cita[5], "Estado": cita[6], "ID_Paciente": cita[7], "ID_Medico": cita[8], "Direccion": cita[9], "Ciudad": cita[10], "Celular": cita[11], "Primera_Vez": cita[12], "Comentarios": cita[13], "Valoracion": cita[14]} for cita in citas ]
    return lista_productos

def dic_pacientes():
    sql = "SELECT id, tipo_doc, num_doc, email, nombre_ape, tipo_persona FROM pacientes "
    print(sql)
    conn = sql_connection()
    cursoObj = conn.cursor()
    cursoObj.execute(sql)
    pacientes = cursoObj.fetchall()
    lista_pacientes = [ {"ID": paciente[0], "Tipo Documento": paciente[1], "N. ID": paciente[2], "Email": paciente[3], "Nombre": paciente[4], "Regimen": paciente[5]} for paciente in pacientes ]
    return lista_pacientes

def dic_medicos():
    sql = "SELECT id, nombre, tipo_doc, num_doc, email, especialidad FROM medico "
    print(sql)
    conn = sql_connection()
    cursoObj = conn.cursor()
    cursoObj.execute(sql)
    medicos = cursoObj.fetchall()
    lista_medicos = [ {"ID": medico[0], "Nombre": medico[1], "Tipo Documento": medico[2], "N. ID": medico[3], "Email": medico[4], "Especialidad_Medico": medico[5]} for medico in medicos ]
    return lista_medicos

def dic_historial():
    sql = "SELECT id, cita, historial FROM historial "
    print(sql)
    conn = sql_connection()
    cursoObj = conn.cursor()
    cursoObj.execute(sql)
    historias = cursoObj.fetchall()
    lista_historias = [ {"ID": historia[0], "ID_Cita": historia[1], "Historial": historia[2]} for historia in historias ]
    return lista_historias

def sql_delete_citas(id):
    sql = "DELETE FROM Citas WHERE id = '{}' ".format(id)
    print(sql)
    conn = sql_connection()
    cursoObj = conn.cursor()
    cursoObj.execute(sql)
    conn.commit()
    conn.close()

def sql_delete_pacientes(num_doc):
    sql = "DELETE FROM pacientes WHERE num_doc = '{}'".format(num_doc)
    print(sql)
    conn = sql_connection()
    cursoObj = conn.cursor()
    cursoObj.execute(sql)
    conn.commit()
    conn.close()

def sql_delete_medicos(num_doc):
    sql = "DELETE FROM medico WHERE num_doc = '{}'".format(num_doc)
    print(sql)
    conn = sql_connection()
    cursoObj = conn.cursor()
    cursoObj.execute(sql)
    conn.commit()
    conn.close()

def sql_edit_citas(motivo_cita, descripcion, fecha, hora_cita, horario_salida, estado, id_paciente, idMedico, direccion, ciudad, celular, first_time, especialidad_consulta, comentarios, valoracion):
    sql = "SET motivo_cita = '{}', descripcion = '{}', fecha = '{}', hora_cita = '{}', horario_salida = '{}', estado = '{}', id_paciente = '{}', idMedico = '{}', direccion = '{}', ciudad = '{}', celular = '{}', first_time = '{}', especialidad_consulta = '{}', comentarios = '{}', valoracion = '{}' WHERE id_paciente = '{}' AND idMedico = '{}'".format(motivo_cita, descripcion, fecha, hora_cita, horario_salida, estado, id_paciente, idMedico, direccion, ciudad, celular, first_time, especialidad_consulta, comentarios, valoracion, id_paciente, idMedico)
    print(sql)
    conn = sql_connection()
    cursoObj = conn.cursor()
    cursoObj.execute(sql)
    conn.commit()
    conn.close()

def sql_edit_paciente(tipo_doc, num_doc, email, password, nombre_ape, tipo_persona):
    sql = "SET tipo_doc = '{}', num_doc = '{}', email = '{}', password = '{}', nombre_ape = '{}', tipo_persona = '{}' WHERE num_doc = '{}'".format(tipo_doc, num_doc, email, password, nombre_ape, tipo_persona, num_doc)
    print(sql)
    conn = sql_connection()
    cursoObj = conn.cursor()
    cursoObj.execute(sql)
    conn.commit()
    conn.close()

def sql_edit_medico(nombre, tipo_doc, num_doc, email, password, especialidad):
    sql = "UPDATE medico SET nombre = '{}', tipo_doc = '{}', num_doc = '{}', email = '{}', password = '{}', especialidad = '{}' WHERE  num_doc = '{}'".format(nombre, tipo_doc, num_doc, email, password, especialidad, num_doc)
    print(sql)
    conn = sql_connection()
    cursoObj = conn.cursor()
    cursoObj.execute(sql)
    conn.commit()
    conn.close()

def seq_insert_medico(nombre, t_id_login, no_id_login, email, password, especialidad):
    sql = "INSERT INTO medico (nombre,tipo_doc, num_doc, email, password, especialidad) VALUES ('{}', '{}', '{}', '{}', '{}','{}')".format(nombre, t_id_login, no_id_login, email, password, especialidad)
    conn = sql_connection()
    cursoObj = conn.cursor()
    cursoObj.execute(sql)
    conn.commit()
    conn.close()

def insert_registro_usuario(tipo_id, num_doc, email, password, nombre_ape, tipo_persona):
    sql = "INSERT INTO pacientes (tipo_doc, num_doc, email, password, nombre_ape, tipo_persona) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(tipo_id, num_doc, email, password, nombre_ape, tipo_persona)
    conn = sql_connection()
    cursoObj = conn.cursor()
    cursoObj.execute(sql)
    conn.commit()
    conn.close()

def insert_registro_cita(motivo_cita, descripcion, fecha, hora_cita, horario_salida, estado, id_paciente, idMedico, direccion, ciudad, celular, first_time, especialidad_consulta, comentarios, valoracion):
    sql = "INSERT INTO Citas (motivo_cita, descripcion, fecha, hora_cita, horario_salida, estado, id_paciente, idMedico, direccion, ciudad, celular, first_time, especialidad_consulta, comentarios, valoracion) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(motivo_cita, descripcion, fecha, hora_cita, horario_salida, estado, id_paciente, idMedico, direccion, ciudad, celular, first_time, especialidad_consulta, comentarios, valoracion)
    conn = sql_connection()
    cursoObj = conn.cursor()
    cursoObj.execute(sql)
    conn.commit()
    conn.close()

def sql_select_medicos():
    sql = "SELECT nombre, num_doc, email, especialidad FROM medico"
    conn = sql_connection()
    cursorObj = conn.cursor()
    cursorObj.execute(sql)
    medicos = cursorObj.fetchall()
    return medicos

def sql_select_pacientes():
    sql = "SELECT num_doc, email, nombre_ape FROM pacientes"
    conn = sql_connection()
    cursorObj = conn.cursor()
    cursorObj.execute(sql)
    pacientes = cursorObj.fetchall()
    return pacientes

def sql_select_citas():
    sql="SELECT id, motivo_cita, fecha, hora_cita, horario_salida, estado, id_paciente, idMedico, direccion, ciudad, celular, first_time, especialidad_consulta FROM Citas"
    conn = sql_connection()
    cursorObj = conn.cursor()
    cursorObj.execute(sql)
    citas = cursorObj.fetchall()
    return citas

def sql_select_especialidad():
    sql = "SELECT id, nombre FROM especialidad_medico"
    conn = sql_connection()
    cursorObj = conn.cursor()
    cursorObj.execute(sql)
    especialidades = cursorObj.fetchall()
    return especialidades

def select_citas_completo():
    sql = "SELECT id, motivo_cita, descripcion, fecha, hora_cita, horario_salida, estado, id_paciente, idMedico, direccion, ciudad, celular, first_time, especialidad_consulta, comentarios, valoracion FROM Citas"
    conn = sql_connection()
    cursorObj = conn.cursor()
    cursorObj.execute(sql)
    citas_completo = cursorObj.fetchall()
    return citas_completo

def select_pacientes_completo():
    sql = "SELECT id, tipo_doc, num_doc, email, nombre_ape, tipo_persona FROM pacientes"
    conn = sql_connection()
    cursorObj = conn.cursor()
    cursorObj.execute(sql)
    pacientes = cursorObj.fetchall()
    return pacientes

def insert_admn(id, nombre, num_id, email, password, telefono):
    sql = "INSERT INTO admin (id, nombre, num_id, email, password, telefono) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(id, nombre, num_id, email, password, telefono)
    conn = sql_connection()
    cursoObj = conn.cursor()
    cursoObj.execute(sql)
    conn.commit()
    conn.close()



def login_required(view):
    @functools.wraps( view ) # toma una función utilizada en un decorador y añadir la funcionalidad de copiar el nombre de la función.
    def wrapped_view(**kwargs):
        if (g.user_medico is None) and (g.user is None):
            return redirect( url_for( 'login' ) ) # si no tiene datos, lo envío a que se loguee
        return view( **kwargs )
    return wrapped_view

def login_required_admin(view):
    @functools.wraps( view ) # toma una función utilizada en un decorador y añadir la funcionalidad de copiar el nombre de la función.
    def wrapped_viewp(**kwargsp):
        print("hola")
        if g.user_admin is None:
            return redirect( url_for( 'login' ) ) # si no tiene datos, lo envío a que se loguee
        return view( **kwargsp )
    return wrapped_viewp

@app.before_request
def cargar_paciente_registrado():
    print("entro en el before_request Paciente")
    id_usuario = session.get('id_usuario')
    if id_usuario is None:
        g.user = None
    else:
        g.user = get_db().execute(
                'SELECT id, tipo_doc, num_doc, email, password, nombre_ape, tipo_persona FROM pacientes WHERE id = ?'
                ,
                (id_usuario,)
            ).fetchone()


@app.before_request
def cargar_medico_registrado():
    print("entro en el before medico")
    id_medico = session.get('id_medico')
    if id_medico is None:
        g.user_medico = None
    else:
        g.user_medico = get_db().execute(
                'SELECT id, nombre, tipo_doc, num_doc, email, password, especialidad FROM medico WHERE id = ?'
                ,
                (id_medico,)
            ).fetchone()
    print('g.user_medico:', g.user_medico)  


@app.before_request
def cargar_administrador_registrado():
    print("entro en el before_request_administrador")
    id_administrador = session.get('id_administrador')
    if id_administrador is None:
        g.user_admin = None
    else:
        g.user_admin = get_db().execute(
                'SELECT id, nombre, num_id, email, password, telefono FROM admin WHERE id = ?'
                ,
                (id_administrador,)
            ).fetchone()
    print('g.user_admin:', g.user_admin)    

@app.route('/')
@app.route('/index/')
def index():
    form = Registro_usuario( request.form )    
    return render_template('index.html')


@app.route('/detalle-cita/')
@app.route('/detalle-cita/<int:id>/')
@app.route('/login/perfil/detalle-cita/<int:id>/')
#@login_required or login_required_admin
def detalle_cita(id=0):
    form = Detalle_cita( request.form )
    try:
        #idu = request.args.get('id_paciente')
        #ido = form.id_paciente.data
        pacientes = sql_select_pacientes()
        citas = sql_select_citas()
        medicos = sql_select_medicos()
        especialidades = sql_select_especialidad()
        pacientes = [ paciente for paciente in pacientes if paciente[0] == id ]
        citas = [ cita for cita in citas if cita[6] == id or cita[7] == id and cita[5] == "Pendiente"]
        cita_especifica =  citas[0]  
        medicos = [ medico for medico in medicos if medico[1] == cita_especifica[7]]#no esta leyendo el cita_especifica
        perfil_medico = medicos[0]
        especialidades = [ especialidad for especialidad in especialidades if especialidad[0] == perfil_medico[3] ]
        if len(pacientes)>0 and len(citas)>0 and len(medicos)>0 and len(especialidades)>0:
            perfil_paciente = pacientes[0]
            especialidad_medico = especialidades[0]
            #cita_especifica = citas[0]
            #perfil_medico = medicos[0]
            return render_template('detalle_cita.html', form=form, perfil_paciente=perfil_paciente, cita_especifica=cita_especifica, perfil_medico=perfil_medico, especialidad_medico=especialidad_medico)
        return render_template('detalle_cita.html', form=form, perfil_paciente=None, cita_especifica=None, perfil_medico=None, especialidad_medico=None)
    except:
        flash("No Encontrado")
        return render_template('detalle_cita.html')


@app.route('/login/perfil/<int:id>/')
@app.route('/perfil/<int:id>/')
#@login_required
def perfil(id=0):
    medicos = sql_select_medicos()
    pacientes = sql_select_pacientes()


    medicos = [ medico for medico in medicos if medico[1] == id ]
    pacientes = [ paciente for paciente in pacientes if paciente[0] == id ]


    if len(medicos)>0:
        perfil_medico = medicos[0] 
        return render_template('perfil.html', perfil_medico=perfil_medico, perfil_paciente=None, id=id)
    if len(pacientes)>0:
        perfil_paciente = pacientes[0]
        return render_template('perfil.html', perfil_paciente=perfil_paciente, perfil_medico=None, id=id )
    else:
        return render_template('perfil.html', medicos=medicos, pacientes=pacientes, id=id)


@app.route('/registrar-cita/', methods=['GET','POST'])
@app.route('/registrar-cita/<int:id>/', methods=['GET', 'POST'])
def registrar_cita(id=0):
    form = Registrar_cita( request.form )
    if request.method == 'POST':
        motivo = request.form['motivo']
        descripcion = request.form['descripcion']
        date = request.form['date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        estado = request.form['estado']
        id_paciente = request.form['id_paciente']
        id_medico = request.form['id_medico']
        direccion = request.form['direccion']
        ciudad = request.form['ciudad']
        celular = request.form['celular']
        vez = request.form['vez']
        especialidad = request.form['especialidad']
        comentarios = request.form['comentarios']
        valoracion = request.form['valoracion']

        insert_registro_cita(motivo, descripcion, date, start_time, end_time, estado, id_paciente, id_medico, direccion, ciudad, celular, vez, especialidad, comentarios, valoracion)
    return render_template('registrar_citas.html', form=form)



@app.route('/login/', methods=['GET','POST'])
def login():
    
    form = Login( request.form )

    #try:
    if request.method == 'POST':
        t_usuario_login = request.form['t_usuario_login']
        t_id_login = request.form['t_id_login']
        no_id_login = request.form['no_id_login']
        password_login = request.form['password_login']

        error = None
        db = get_db()

        if not no_id_login:
            error = "ID requerido."
            flash( error )
        if not password_login:
            error = "Contraseña requerida."
            flash( error )

        if error is not None:
            # SI HAY ERROR:
            return render_template('login.html', form=form)
        else:
            # No hay error:
            flash('Bienvenido')
            if t_usuario_login == "Administrador":#login_administrador
                user_admin = db.execute('SELECT id, nombre, num_id, email, password, telefono FROM admin WHERE num_id = ?',(no_id_login,)).fetchone()
                if user_admin is None:
                    error= "Usuario y Contraseña no existen"
                    flash( error )
                #else: NECESITO ENCRIPTAR AL ADMINISTRADOR PRIMERO
                #    administrador_valido = check_password_hash(user_admin[4],password_login)
                #    if not administrador_valido:
                #        error = "Usuario y contraseña no son correctos."
                #        flash( error )                
                #        return render_template('login.html', form=form)
                else:
                    session.clear()
                    session['id_administrador'] = user_admin[0] 
                    print(user_admin[0])               
                    return redirect( 'administrador/' ) 
            if t_usuario_login == "Medico":#loginMedico
                user_medico = db.execute('SELECT id, nombre, tipo_doc, num_doc, email, password, especialidad FROM medico WHERE num_doc = ?',(no_id_login,)).fetchone()
                if user_medico is None:
                    error= "Usuario y Contraseña no existen"
                    flash( error )
                else:
                    medico_valido = check_password_hash(user_medico[5],password_login)
                    if not medico_valido:
                        error = "Usuario y contraseña no son correctos."
                        flash( error )                
                        return render_template('login.html', form=form)
                    else:
                        session.clear()
                        session['id_medico'] = user_medico[0]                
                        return redirect('perfil/{}'.format(no_id_login) )
            if t_usuario_login == "Paciente":#loginPaciente
                user = db.execute('SELECT id, tipo_doc, num_doc, email, password, nombre_ape, tipo_persona FROM pacientes WHERE num_doc = ?',(no_id_login,)).fetchone()
                if user is None:
                    error= "Usuario y Contraseña no existen"
                    flash( error ) 
                else:
                    usuario_valido = check_password_hash(user[4],password_login)
                    if not usuario_valido:
                        error = "Usuario y contraseña no son correctos."
                        flash( error )                
                        return render_template('login.html', form=form)
                    else:
                        session.clear()
                        session['id_usuario'] = user[0]                
                        return redirect( 'perfil/{}'.format(no_id_login))
    return render_template('login.html', form=form)


@app.route('/registro_usuario/', methods=['GET','POST'])
def registro_usuario():
    form = Registro_usuario( request.form )
    try:
        if request.method == 'POST':   
            tipo_usuario = request.form['tipo_usuario']
            tipo_id = request.form['tipo_id']
            usuario = request.form['usuario']
            no_id = request.form['no_id']
            email = request.form['email']
            password = request.form['password']

            error = None
            db = get_db()

            if not usuario:
                error = "Usuario requerido."
                flash(error)
            if not password:
                error = "Contraseña requerida."
                flash(error)
            if not isUsernameValid(usuario):
                error = "El usuario debe ser alfanumerico o incluir solo '.','_','-'"
                flash(error)
            if not isEmailValid(email):
                error = "Correo invalido"
                flash(error)
            if not isPasswordValid(password):
                error = "La contraseña debe contener al menos una minúscula, una mayúscula, un número y 8 caracteres"
                flash(error)
            if error is not None:
                return render_template('registro_usuario.html',form=form)

            user = db.execute('SELECT * FROM pacientes WHERE num_doc=? AND email = ?',(no_id,email)).fetchone()            
            if user is not None:
                error = "Paciente Ya Existente."
                flash(error)

            if error is not None:
                # Ocurrió un error
                return render_template('registro_usuario.html',form=form)
            else:
                password_cifrado = generate_password_hash(password)
                insert_registro_usuario(tipo_id, no_id, email, password_cifrado, usuario, tipo_usuario)
                
                yag = yagmail.SMTP('pruebas.programacion.test@gmail.com', 'Femizoo.1234') 
                yag.send(to=email, subject='Activa tu cuenta',
                    contents='Bienvenido ')
                flash('Revisa tu correo para activar tu cuenta')
                form=Registro_usuario()
                return render_template('registro_usuario.html',form=form)
        return render_template('registro_usuario.html',form=form)
    except:
        flash("Ha ocurrido un error, intentalo de nuevo")    
        return render_template('registro_usuario.html')


@app.route('/login/administrador/', methods=['GET','POST'])
@app.route('/administrador/', methods=['GET','POST'])
@login_required_admin
def administrador():
    return render_template('dashboard.html')

@app.route('/lista-citas/')
@login_required_admin
def citas():
    citas = sql_select_citas()
    return render_template('listar_citas.html', citas=citas)    
    

@app.route('/resultado-busqueda/<int:id>/', methods=['GET', 'POST'])
@login_required_admin
def resultado(id=0):
    return render_template('Resultadodebusqueda.html')

@app.route('/listar-citas')
@login_required_admin
def listarCitas():
    citas = select_citas_completo()
    return render_template('Listar_citas.html', citas = citas)

@app.route('/listar-pacientes')
@login_required_admin
def listarPacientes():
    pacientes = select_pacientes_completo()
    return render_template('listar_pacientes.html', pacientes = pacientes)

@app.route('/listar-medicos')
@login_required_admin
def listarMedicos():
    medicos = sql_select_medicos()
    return render_template('Listar_medico.html', medicos = medicos)

@app.route('/listar-historial')
@login_required_admin
def listarhistorial():
    historias = select_historial_completo()
    return render_template('Listar_historial.html', historias = historias)


@app.route('/registro_medico/', methods=['GET','POST'])
#@login_required_admin
def registro_medico():
    form = Registro_medicos( request.form )
    try:
        if request.method == 'POST':   
            nombre = request.form['nombre']
            t_id_login = request.form['t_id_login']
            no_id_login = request.form['no_id_login']
            email = request.form['email']
            password = request.form['password']
            especialidad = request.form['especialidad']

            error = None
            db = get_db()

            if not nombre:
                error = "Usuario requerido."
                flash(error)
            if not password:
                error = "Contraseña requerida."
                flash(error)
            if not isUsernameValid(nombre):
                error = "El usuario debe ser alfanumerico o incluir solo '.','_','-'"
                flash(error)
            if not isEmailValid(email):
                error = "Correo invalido"
                flash(error)
            if not isPasswordValid(password):
                error = "La contraseña debe contener al menos una minúscula, una mayúscula, un número y 8 caracteres"
                flash(error)
            if error is not None:
                return render_template('registrar_medicos.html',form=form)

            user = db.execute('SELECT * FROM medico WHERE num_doc = ? AND email = ?',(no_id_login,email)).fetchone()
            if user is not None:
                error = "Medico Ya Existente"
                flash(error)

            if error is not None:
                # Ocurrió un error
                return render_template('registrar_medicos.html',form=form)
            else:
                password_cifrado = generate_password_hash(password)
                seq_insert_medico(nombre, t_id_login, no_id_login, email, password_cifrado, especialidad)
                yag = yagmail.SMTP('pruebas.programacion.test@gmail.com', 'Femizoo.1234') 
                yag.send(to=email, subject='Activa tu cuenta',contents='Bienvenido ')
                flash('Correo Enviado al Medico, para activar cuenta')
                form = Registro_medicos()
                return render_template('registrar_medicos.html',form=form)
        return render_template('registrar_medicos.html',form=form)
    except:
        flash("Ha ocurrido un error, intentalo de nuevo")    
        return render_template('registrar_medicos.html', form=form)


@app.route('/actualizar-medico/', methods=['GET','POST','PUT'])
@login_required_admin
def actualizar_medico():
    form = Registro_medicos( request.form )
    try:
        if request.method == 'POST':   
            nombre = request.form['nombre']
            tipo_doc = request.form['t_id_login']
            num_doc = request.form['no_id_login']
            email = request.form['email']
            password = request.form['password']
            especialidad = request.form['especialidad']

            flash('Medico Actualizado')
            sql_edit_medico(nombre, tipo_doc, num_doc, email, password, especialidad)
            form = Registro_medicos()
            return render_template('actualizar_medico.html',form=form)

        return render_template('actualizar_medico.html',form=form)
    except:
        flash("Ha ocurrido un error, intentalo de nuevo")    
        return render_template('actualizar_medico.html', form=form)

@app.route('/actualizar-paciente/', methods=['GET','POST','PUT'])
@login_required_admin
def edit_usuario():
    form = Registro_usuario( request.form )
    try:
        if request.method == 'POST':   
            tipo_usuario = request.form['tipo_usuario']
            tipo_id = request.form['tipo_id']
            usuario = request.form['usuario']
            no_id = request.form['no_id']
            email = request.form['email']
            password = request.form['password']

            flash('Paciente Actualizado')
            sql_edit_paciente(tipo_id, no_id, email, password, usuario, tipo_usuario)
            form=Registro_usuario()
            return render_template('actualizar_paciente.html',form=form)

        return render_template('actualizar_paciente.html',form=form)
    except:
        flash("Ha ocurrido un error, intentalo de nuevo")    
        return render_template('actualizar_paciente.html')

@app.route('/actualizar-citas/', methods=['GET','POST'])
@login_required_admin
def actualizar_citas():
    form = Registrar_cita( request.form )
    if request.method == 'POST':
        motivo = request.form['motivo']
        descripcion = request.form['descripcion']
        date = request.form['date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        estado = request.form['estado']
        id_paciente = request.form['id_paciente']
        id_medico = request.form['id_medico']
        direccion = request.form['direccion']
        ciudad = request.form['ciudad']
        celular = request.form['celular']
        vez = request.form['vez']
        especialidad = request.form['especialidad']
        comentarios = request.form['comentarios']
        valoracion = request.form['valoracion']
        sql_edit_citas(motivo, descripcion, date, start_time, end_time, estado, id_paciente, id_medico, direccion, ciudad, celular, vez, especialidad, comentarios, valoracion)
        flash('Cita Actualizada')
    return render_template('registrar_citas.html', form=form)

@app.route('/borrar-medicos/', methods=['GET','POST'])
@login_required_admin
def borrar_medicos():
    form = Borrar( request.form )
    if request.method == 'POST':
        id = request.form['no_id_login']
        sql_delete_medicos(id)
        flash('Medico Borrado')
        return render_template('borrar.html', form=form)
    return render_template('borrar.html', form=form)

@app.route('/borrar-pacientes/', methods=['GET','POST'])
@login_required_admin
def borrar_pacientes():
    form = Borrar( request.form )
    if request.method == 'POST':
        id = request.form['no_id_login']
        sql_delete_pacientes(id)
        flash('Paciente Borrado')
        return render_template('borrar.html', form=form)
    return render_template('borrar.html', form=form)

@app.route('/borrar-citas/', methods=['GET','POST'])
@login_required_admin
def borrar_citas():
    form = Borrar( request.form )
    if request.method == 'POST':
        id = request.form['no_id_login']
        sql_delete_citas(id)
        flash('Cita Borrada')
        return render_template('borrar.html', form=form)
    return render_template('borrar.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect( url_for( 'index' ) )

@app.route('/buscador-citas/<int:id>/', methods=['GET','POST'])
@app.route('/buscador-citas', methods=['GET','POST'])
# @login_required or login_required_admin
def buscador_citas(id=0):
    citas = sql_citas_id()
    lista_citas = [ cita for cita in citas if cita['ID_Medico'] == id ]
    if len(lista_citas)>0:
        return render_template('buscador-citas.html', lista_citas = lista_citas)
    else: 
        lista_citas = [ cita for cita in citas if cita['ID_Paciente'] == id ]
        return render_template('buscador-citas.html', lista_citas = lista_citas)

@app.route('/historial/<int:id>/', methods=['GET','POST'])
@app.route('/historial/', methods=['GET', 'POST'])#no esta probado ---> probar
def method_name(id=0):
    historias = dic_historial()
    citas = sql_citas_id()
    lista_citas = [ cita for cita in citas if cita['ID_Medico'] == id ]
    lista_historias = [ historia for historia in historias if historia['ID_Cita'] == lista_citas[0] ]
    if len(lista_historias)>0:
        return render_template('historial.html', lista_historias = lista_historias, lista_citas = lista_citas)
    else: 
        lista_citas = [ cita for cita in citas if cita['ID_Paciente'] == id ]
        lista_historias = [ historia for historia in historias if historia['ID_Cita'] == lista_citas[0] ]
        return render_template('historial.html', lista_historias = lista_historias, lista_citas = lista_citas)

@app.route('/registro-historial', methods=['GET', 'POST'])
@login_required_admin
def historial():
    form = Historial( request.form )
    try:
        if request.method == 'POST':   
            id_cita = request.form['id_cita']
            comentarios = request.form['comentarios']

            error = None
            db = get_db()

            if not id_cita:
                error = "Id Cita Requerido."
                flash(error)
            if error is not None:
                return render_template('registro-historial.html', form=form)
            else:
                insert_historial(id_cita,comentarios)
                flash('Historial Agregado')
                form=Historial()
                return render_template('registro-historial.html', form=form)
        return render_template('registro-historial.html', form=form)
    except:
        flash("Ha ocurrido un error, intentalo de nuevo")    
        return render_template('registro-historial.html')
    
@app.route('/actualizar-historial', methods=['GET', 'POST'])
@login_required_admin
def edit_historial():
    form = Historial( request.form )
    try:
        if request.method == 'POST':   
            id_cita = request.form['id_cita']
            comentarios = request.form['comentarios']

            error = None

            if not id_cita:
                error = "Id Cita Requerido."
                flash(error)
            if error is not None:
                return render_template('registro-historial.html', form=form)
            else:
                edit_historial(id_cita,comentarios)
                flash('Cambio Realizado')
                form=Historial()
                return render_template('registro-historial.html', form=form)
        return render_template('registro-historial.html', form=form)
    except:
        flash("Ha ocurrido un error, intentalo de nuevo")    
        return render_template('registro-historial.html')

@app.route('/borrar-historial', methods=['GET', 'POST'])
@login_required_admin
def borrar_historial():
    form = Borrar( request.form )
    if request.method == 'POST':
        id = request.form['no_id_login']
        delete_historial(id)
        flash('Historial Borrado')
        return render_template('borrar.html', form=form)
    return render_template('borrar.html', form=form)

@app.route('/download')
def download():
    return send_file( "resources/L_medicos.pdf", as_attachment=True )






#DIEGO ESTA LINEA ES NECESARIA PARA LA CERTIFICACION
if __name__ == "__main__":
    app.run( host='127.0.0.1', port =443, ssl_context=('micertificado.pem', 'llaveprivada.pem') )

