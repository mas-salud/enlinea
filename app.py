from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import redirect,url_for,request
from flask.helpers import flash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yqwsipgsefzhwf:c8e6c437ed5e21655da9e1b9a8d7be755a70699f960bfc76af3bf05fdfaa0816@ec2-44-193-150-214.compute-1.amazonaws.com:5432/db3t4c0ipt369a'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)

app.secret_key='12345'



from models.doctores import Doctores
from models.franjas import Franjas
from models.pacientes import Pacientes
from models.agenda import Agenda


@app.route("/")
def home():
    return render_template('index.html')





@app.route("/crea_cita",methods=["GET", "POST"])

def get_crea_cita():   
    if (request.method == "GET"):
        date_cita=request.args.get("date",default="", type=str)
        id_doc=request.args.get("id_doc",default=1, type=int)
        if date_cita=="":
            all_franjas=[]
        else:
            id_franjas_ocupadas=list(Agenda.query.with_entities(Agenda.id_franja).filter_by(fecha_cita=date_cita,id_doc=id_doc).all())
            id_franjas_desocupadas=list(set(range(1,17)).difference(set([agd[0] for agd in id_franjas_ocupadas])))
            all_franjas=Franjas.get_for_ids(id_franjas_desocupadas)
        all_doctores=Doctores.get_all()
        #all_franjas=Franjas.get_all()
        #envio lista con fechas deshabilitadas No. uno
        fechas_deshabilitadas = ['12/25/2021', '12/08/2021'];
        #ag = Agenda.query.all()
        #all_diasferiados =[]
        #for dias in ag:
        #    all_diasferiados.append(dias.fecha_cita.strftime("%m/%d/%Y"))

        #return render_template('crea_cita.html',muestra_doctores=all_doctores,muestra_franjas=all_franjas,disabledDate=str(all_diasferiados),date=date_cita,id_doc=id_doc)
        return render_template('crea_cita.html',muestra_doctores=all_doctores,muestra_franjas=all_franjas,disabledDate=fechas_deshabilitadas,date=date_cita,id_doc=id_doc)
    else:
        request_data=request.form
        doctor_seleccionado = request_data["doctor_seleccionado_formulario"]
        franja_seleccionada = request_data["franja_seleccionada_formulario"]
        fecha_seleccionada=request.form["fecha_formulario"]
        numero_documento_seleccionado=request.form["numero_documento_formulario"]
        codigo_cita=112233
        status_cita="P"
        paciente=Pacientes.query.filter_by(numero_documento=numero_documento_seleccionado).first()
        
        busca = Pacientes.query.filter_by(numero_documento= numero_documento_seleccionado)
        
        if (len(busca.all())==0):
            print("no esta creado")
        # el paciente no esta creado se debe enviar a crear paciente
            return redirect(url_for("get_crea_pacientes"))
        else:
            doctor=Doctores.query.get(doctor_seleccionado).nombre_completo
            franja=Franjas.query.get(franja_seleccionada).hora_inicio
            cita = Agenda(fecha_seleccionada,doctor_seleccionado,paciente.id,franja_seleccionada,codigo_cita,status_cita)
            cita.create()
            return render_template("confirmar_cita.html",paciente=paciente, fecha=fecha_seleccionada, doctor=doctor, franja=franja)

@app.route("/crea_pacientes",methods=["GET", "POST"])

def get_crea_pacientes():   
    if (request.method == "GET"): 
       return render_template('crea_paciente.html')
    else:
        request_data=request.form
        # el numero de documento y el tipo vienen de la consulta anterior
        tipodoc_seleccionado = request_data["tipodoc_formulario"]
        numero_documento_seleccionado=request_data["numero_documento_formulario"]
        apellidos_seleccionado = request_data["apellidos_seleccionado_formulario"]
        nombres_seleccionado = request_data["nombres_seleccionado_formulario"]
        apellidos_seleccionado = request_data["apellidos_seleccionado_formulario"]
        fecha_nacimiento_seleccionado = request_data["fecha_nacimiento_seleccionado_formulario"]
        telefono_seleccionado = request_data["telefono_seleccionado_formulario"]
        celular_seleccionado = request_data["celular_seleccionado_formulario"]
        correo_electronico_seleccionado = request_data["correo_electronico_seleccionado_formulario"]
        paciente_nuevo = Pacientes( nombres_seleccionado,apellidos_seleccionado,tipodoc_seleccionado, numero_documento_seleccionado, fecha_nacimiento_seleccionado, telefono_seleccionado,celular_seleccionado,correo_electronico_seleccionado)
        paciente_nuevo.create()
        return redirect(url_for("get_crea_cita"))



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
        busca = Pacientes.query.filter_by(numero_documento= documento_paciente)
        if (len(busca.all())==0):
        # el paciente no esta creado se debe enviar a crear paciente
            return redirect(url_for("get_crea_pacientes"))
        else:
            return redirect(url_for("get_pacientes_citas"))
    else:    
        return render_template('consulta_pacientes.html')







@app.route("/pacientes_citas",methods=["GET", "POST"])
def get_pacientes_citas():
    if request.method =="POST":
        request_data=request.form    
        documento_paciente=request_data.get("busca_documento")
    elif request.method == "GET":
        documento_paciente=request.args.get("doc",default=1,type=int)
    print(documento_paciente)
    busca = (Pacientes.query.filter_by(numero_documento= documento_paciente).first())
    if busca==None:
        return render_template('paciente_no_registrado.html',documento_consultado=documento_paciente)
        #return "NO creado"
    else:
        id_capturado_paciente=busca.id
        all_data=Agenda.query.filter_by(id_paciente=id_capturado_paciente).all()
        buscan = (Pacientes.query.filter_by(id= id_capturado_paciente).first())
        nombre_busca=buscan.nombres
        apellido_busca=buscan.apellidos
        print(nombre_busca)
        all_doctores=Doctores.todict()
        all_franjas=Franjas.todict()
        return render_template('consulta_agenda_pacientes.html',nombre=nombre_busca,apellido=apellido_busca,muestra_agenda=all_data,muestra_doctores=all_doctores,muestra_franjas=all_franjas)





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


@app.route("/doctores")

def get_doctores():
    all_data=Doctores.get_all()
    return render_template('consulta_doctores.html',muestra_doctores=all_data)

""" @app.route("/fechas_deshabilitadas")
def get_fechas_deshabilitadas():
    filtrodoctorfecha = (Agenda.query.filter((Agenda.id_doc == 2) & (Agenda.fecha_cita =="10/19/2021" )))
    cuantos=len(filtrodoctorfecha.all())
    print(cuantos)
    return render_template('fechasdoctor.html',fecha=filtrodoctorfecha)
     """
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


""" if __name__ == '__main__':
    app.debug=True
    app.run() """
## realizo andrea    
@app.route("/login_doctores", methods=['GET','POST'])
def login_de_doctores():
     if request.method == 'POST':
         correo = request.form['correodoct']
         clave= request.form['clavedoct']
         fechac=request.form['fecha']
         doctor = Doctores.match_login(correo,clave)
         if doctor != None:
            id=doctor.id
            nombre=doctor.nombre_completo
            print(nombre)
            all_data=Agenda.query.filter_by(id_doc=id).all()
            all_pacientes=Pacientes.todict()
            all_doctores=Doctores.todict()
            all_franjas=Franjas.todict()
            return render_template('consulta_agenda_doctores.html',nombred=nombre,muestra_paciente=all_pacientes,muestra_agenda=all_data,muestra_franjas=all_franjas,muestra_doctores=all_doctores) 
         else:
            return render_template('login_doctores.html')    
         print(doctor)
     return render_template('login_doctores.html')




    

    
if __name__ == '__main__' :    
    app.run(debug=False)