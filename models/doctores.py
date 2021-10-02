from app import database


class Doctores(database.Model):
    
    __tablename__ = 'doctores'
    #table model
    id = database.Column(database.Integer, primary_key=True)
    nombre_completo= database.Column(database.String,nullable=False)
    correo_electronico = database.Column(database.String, nullable=False)
    clave = database.Column(database.String, nullable=False)

    #constructor
    def __init__(self,nombre_completo, correo_electronico,clave):
        self.nombre_completo=nombre_completo
        self.email = correo_electronico
        self.clave = clave
        
    
    def __str__(self):
        return f"<Doctor {self.id} {self.email}{self.nombre_completo} {self.clave} >"
    
    def create(self):
        database.session.add(self)
        database.session.commit()
        
        
    @staticmethod
    def todict():
        dic={}
        for doctor in Doctores.get_all():
            dic[doctor.id]=doctor
        return dic    
    
    @staticmethod
    def get_all():
        return Doctores.query.order_by(Doctores.nombre_completo).all()
        
    
    
    #@staticmethod
    #def get_id():
    #    return Usuario.query.filter_by(id=7).first()
    
    @staticmethod
    def get_email(email_find):
        return Doctores.query.filter_by(correo_electronico=email_find).first()
    
   