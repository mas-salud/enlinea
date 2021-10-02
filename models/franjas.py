from app import database
#from app import bcrypt

class Franjas(database.Model):
    
    __tablename__ = 'franjas'
    
    id_franja = database.Column(database.Integer, primary_key=True)
    hora_inicio= database.Column(database.Time,nullable=False)
    

    
    def __init__(self,hora_inicio):
        self.hora_inicio = hora_inicio
        
    
    def __str__(self):
        return f"<Franjas {self.id_franja} {self.hora_inicio} >"
    
    def create(self):
        database.session.add(self)
        database.session.commit()
    
    @staticmethod
    def get_all():
        return Franjas.query.all()
        
    @staticmethod
    def todict():
        dic={}
        for franja in Franjas.get_all():
            dic[franja.id_franja]=franja
        return dic    
        
        
    
   
    
    