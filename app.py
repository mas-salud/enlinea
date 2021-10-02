from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import request


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yqwsipgsefzhwf:c8e6c437ed5e21655da9e1b9a8d7be755a70699f960bfc76af3bf05fdfaa0816@ec2-44-193-150-214.compute-1.amazonaws.com:5432/db3t4c0ipt369a'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)


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


@app.route("/crea_cita",methods=["GET", "POST"])

def get_crea_cita():
    if (request.method == "POST"):
        print (request.form) 
    all_franjas=Franjas.get_all() 
    all_doctores=Doctores.get_all() 
    return render_template('crea_cita.html',muestra_franjas=all_franjas,muestra_doctores=all_doctores)

@app.route("/agenda")

def get_agenda():
    all_data=Agenda.get_all()
    #print(Pacientes.query.filter(Pacientes.id==all_data[0].id_paciente).first())
    print(Franjas.todict())
    all_pacientes=Pacientes.todict()
    all_doctores=Doctores.todict()
    all_franjas=Franjas.todict()
    return render_template('consulta_agenda.html',muestra_paciente=all_pacientes,muestra_agenda=all_data,muestra_doctores=all_doctores,muestra_franjas=all_franjas)

@app.route("/agenda_doctores")

def get_agenda_doctores():
    #all_data=Agenda.get_all().filter_by(id_doc=1)
    all_data =Agenda.get_algunos()
   

    #print(Pacientes.query.filter(Pacientes.id==all_data[0].id_paciente).first())
    print(Franjas.todict())
    all_pacientes=Pacientes.todict()
    all_franjas=Franjas.todict()
    all_doctores=Doctores.todict()
    return render_template('consulta_agenda_doctores.html',muestra_paciente=all_pacientes,muestra_agenda=all_data,muestra_franjas=all_franjas,muestra_doctores=all_doctores)




if __name__ == '__main__':
    app.debug=True
    app.run()