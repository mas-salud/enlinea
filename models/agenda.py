from app import database
#from app import bcrypt

class Agenda(database.Model):
    
    __tablename__ = 'agenda'
    
    id = database.Column(database.Integer, primary_key=True)
    fecha_cita = database.Column(database.Date, nullable=False)
    id_doc = database.Column(database.Integer,database.ForeignKey ("doctores.id"),nullable=False)
    id_paciente = database.Column(database.Integer,database.ForeignKey ("pacientes.id"),nullable=False)
    id_franja = database.Column(database.Integer, database.ForeignKey ("franjas.id"),nullable=False)
    codigo_cita = database.Column(database.String(8), nullable=False)
    status_cita = database.Column(database.String(1), nullable=False)
    
    
    def __init__(self,fecha_cita,id_doc,id_paciente,id_franja,codigo_cita,status_cita):
        self.fecha_cita = fecha_cita
        self.id_doc = id_doc
        self.id_paciente = id_paciente
        self.id_franja= id_franja
        self.codigo_cita = codigo_cita
        self.status_cita = status_cita
                
    
    def __str__(self):
        return f"<Agenda {self.id} {self.fecha_cita} {self.id_doc} {self.id_paciente}{self.id_franja}{self.codigo_cita}{self.status_cita}>"
    
    def create(self):
        database.session.add(self)
        database.session.commit()
    
    @staticmethod
    def get_all():
        return Agenda.query.all()

    @staticmethod
    def get_algunos():
        return Agenda.query.filter_by(id_doc=1)   
        
    #def get_citas_doctor():
    #    return Agenda.query.filter_by(Agenda.id_doc=1).filter(month(Agenda.fecha_cita)=9).all()
    
    
    