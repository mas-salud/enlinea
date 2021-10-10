from app import database

class No_laborales(database.Model):
    
    __tablename__ = 'no_laborales'
    
    id = database.Column(database.Integer, primary_key=True)
    fecha= database.Column(database.Time,nullable=False)
    descripcion= database.Column(database.String,nullable=False)

    
    def __init__(self,fecha,descripcion):
        self.fecha = fecha
        self.descripcion = descripcion
        
    
    def __str__(self):
        return f"<no_laborales {self.id} {self.fecha} {self.descripcion}>"
    
    def create(self):
        database.session.add(self)
        database.session.commit()
    
    @staticmethod
    def get_all():
        return No_laborales.query.all()
        
        
    