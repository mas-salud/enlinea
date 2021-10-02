from app import database


class Pacientes(database.Model):
    
    __tablename__ = 'pacientes'
    #table model
    id = database.Column(database.Integer, primary_key=True)
    nombres= database.Column(database.String(50),nullable=False)
    apellidos= database.Column(database.String(50),nullable=False)
    tipo_documento= database.Column(database.Integer, nullable=False)
    numero_documento= database.Column(database.Integer, nullable=False)
    fecha_nacimiento= database.Column(database.Date, nullable=False)
    telefono =database.Column(database.String(13))
    celular =database.Column(database.String(13), nullable=False)
    correo_electronico = database.Column(database.String(50), nullable=False)
   

    #constructor
    def __init__(self,nombres,apellidos,tipo_documento, numero_documento,fecha_nacimiento,telefono,celular,correo_electronico):
        self.nombres=nombres
        self.apellidos=apellidos
        self.tipo_documento=tipo_documento
        self.numero_documento=numero_documento
        self.fecha_nacimiento=fecha_nacimiento
        self.telefono=telefono
        self.celular=celular
        self.correo_electronico = correo_electronico
        
        
    
    def __str__(self):
        return f"<Paciente {self.id} {self.nombres} {self.apellidos} {self.tipo_documento} {self.numero_documento} {self.fecha_nacimiento} {self.telefono} {self.celular} {self.correo_electronico}>"
    
    def create(self):
        database.session.add(self)
        database.session.commit()
    
    @staticmethod
    def todict():
        dic={}
        for paciente in Pacientes.get_all():
            dic[paciente.id]=paciente
        return dic    
                        
    
    @staticmethod
    def get_all():
        return Pacientes.query.all()
        
        
        
    
   