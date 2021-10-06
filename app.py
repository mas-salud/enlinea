from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import redirect,url_for,request


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yqwsipgsefzhwf:c8e6c437ed5e21655da9e1b9a8d7be755a70699f960bfc76af3bf05fdfaa0816@ec2-44-193-150-214.compute-1.amazonaws.com:5432/db3t4c0ipt369a'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
#app.secretkey = "secret key"

from models.doctores import Doctores
from models.franjas import Franjas
from models.pacientes import Pacientes
from models.agenda import Agenda


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/doctores")

def get_doctores():
    all_data=Doctores.get_all()
    return render_template('consulta_doctores.html',muestra_doctores=all_data)



@app.route("/franjas")

def get_franjas():
    all_data=Franjas.get_all()
    return render_template('consulta_franjas.html',muestra_franjas=all_data)


@app.route("/calendario")

def get_calendario():
    
    fechas_deshabilitadas= ["12/08/2021", "12/25/2021"]
   # franjas_ocupadas= Agenda.get_franjas_dia_doctor
   # print(franjas_ocupadas)
    return render_template('calendario.html',lista_fechas=fechas_deshabilitadas)


@app.route("/crea_cita",methods=["GET", "POST"])

def get_crea_cita():   
    if (request.method == "GET"): 
        all_doctores=Doctores.get_all()
        all_franjas=Franjas.get_all()
        return render_template('crea_cita.html',muestra_doctores=all_doctores,muestra_franjas=all_franjas)
    else:
        request_data=request.form
        doctor_seleccionado = request_data["doctor_seleccionado_formulario"]
        franja_seleccionada = request_data["franja_seleccionada_formulario"]
        fecha_seleccionada=request.form["fecha_formulario"]
        numero_documento_seleccionado=request.form["numero_documento_formulario"]
        codigo_cita=112233
        status_cita="P"
        print("franja seleccionada",franja_seleccionada)
        print("doctor seleccionado",doctor_seleccionado)
        print("fecha seleccionada",fecha_seleccionada)
        print("documento paciente",numero_documento_seleccionado)
        paciente=Pacientes.query.filter_by(numero_documento=numero_documento_seleccionado).first()
        print(paciente.id)
        cita = Agenda(fecha_seleccionada,doctor_seleccionado,paciente.id,franja_seleccionada,codigo_cita,status_cita)
        cita.create()
        return redirect(url_for("home"))

@app.route("/agenda")


def get_agenda():
    all_data=Agenda.get_all()
    #print(Pacientes.query.filter(Pacientes.id==all_data[0].id_paciente).first())
    print(Franjas.todict())
    all_pacientes=Pacientes.todict()
    all_doctores=Doctores.todict()
    all_franjas=Franjas.todict()
    return render_template('consulta_agenda.html',muestra_paciente=all_pacientes,muestra_agenda=all_data,muestra_doctores=all_doctores,muestra_franjas=all_franjas)

@app.route("/pacientes", methods=["GET", "POST"])
def get_pacientes():
    if request.method =="POST":
        documento_paciente=request.form.get("busca_documento")
        print(documento_paciente)
        print("hola1")
        busca = Pacientes.query.filter_by(numero_documento= documento_paciente).first()
        #busca=Pacientes.query.filter_by(Pacientes.numero_documento==documento_paciente).one()
        print(busca.nombres)
        print(busca.id)
        print("hola2")
        return redirect(url_for("get_pacientes_citas"))
    else:    
        return render_template('consulta_pacientes.html')


@app.route("/pacientes_citas",methods=["GET", "POST"])
def get_pacientes_citas():
    if request.method =="POST":    
        documento_paciente=request.form.get("busca_documento")
        busca = (Pacientes.query.filter_by(numero_documento= documento_paciente).first())
        id_capturado_paciente=busca.id
        all_data=Agenda.query.filter_by(id_paciente=id_capturado_paciente).all()
        buscan = (Pacientes.query.filter_by(id= id_capturado_paciente).first())
        nombre_busca=buscan.nombres
        print(nombre_busca)
        all_doctores=Doctores.todict()
        all_franjas=Franjas.todict()
        return render_template('consulta_agenda_pacientes.html',nombre=nombre_busca,muestra_agenda=all_data,muestra_doctores=all_doctores,muestra_franjas=all_franjas)





@app.route("/agenda_doctores")

def get_agenda_doctores():
    all_data=Agenda.get_all()
    #print(Pacientes.query.filter(Pacientes.id==all_data[0].id_paciente).first())
    print(Franjas.todict())
    all_pacientes=Pacientes.todict()
    all_franjas=Franjas.todict()
    all_doctores=Doctores.todict()
    return render_template('consulta_agenda_doctores.html',muestra_paciente=all_pacientes,muestra_agenda=all_data,muestra_franjas=all_franjas,muestra_doctores=all_doctores)


@app.route("/franjas_doctor")

def get_franjas_doctor():
    print(Franjas.todict())
    all_data=Agenda.get_all()
    all_pacientes=Pacientes.todict()
    all_franjas=Franjas.todict()
    all_doctores=Doctores.todict()
    franjas_doctor=Agenda.get_franjas_dia_doctor()
    print(franjas_doctor.todict())
    return render_template('consulta_agenda_doctores.html',muestra_paciente=all_pacientes,muestra_agenda=all_data,muestra_franjas=all_franjas,muestra_doctores=all_doctores)


if __name__ == '__main__':
    app.debug=True
    app.run()