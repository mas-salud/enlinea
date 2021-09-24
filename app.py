from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yqwsipgsefzhwf:c8e6c437ed5e21655da9e1b9a8d7be755a70699f960bfc76af3bf05fdfaa0816@ec2-44-193-150-214.compute-1.amazonaws.com:5432/db3t4c0ipt369a'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)


from models.doctores import Doctores

@app.route("/")
def bienvenido():
       return ("Bienvenido a Mas Salud")


@app.route("/login")
def login():
    correoing = "robertoCardenas@ejemplo.com"
    claveing = "789"
    valida_usuario = Doctores.login(correoing,claveing)

    return str(valida_usuario)


