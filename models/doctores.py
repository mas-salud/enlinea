from app import database
#from app import bcrypt

class Doctores(database.Model):
    
    __tablename__ = 'doctores'
    
    id = database.Column(database.Integer, primary_key=True)
    correo_electronico = database.Column(database.String, nullable=False)
    clave = database.Column(database.String, nullable=False)
   
    
    def __init__(self,correo_electronico,clave):
        self.email = correo_electronico
        self.clave = clave
        
    
    def __str__(self):
        return f"<Doctor {self.id} {self.email} {self.clave} >"
    
    def create(self):
        database.session.add(self)
        database.session.commit()
    
    @staticmethod
    def get_all():
        return Doctores.query.all()
    
    #@staticmethod
    #def get_id():
    #    return Usuario.query.filter_by(id=7).first()
    
    @staticmethod
    def get_email(email_find):
        return Doctores.query.filter_by(correo_electronico=email_find).first()
    
    @staticmethod
    def login(email, password):
        success = False
        user = Doctores.get_email(email)
                
        if(user):
            
            if (user.clave==password):
                print("clave validada")
            return ("Clave validada")
        return success
        