from app import db

class Docente(db.Model):
    __tablename__ = 'docente'
    
    ID_docente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nombre = db.Column(db.String(50), nullable=False)
    Apellido = db.Column(db.String(50), nullable=False)
    Fecha_de_Nacimiento = db.Column(db.Date, nullable=True)
    Correo = db.Column(db.String(255), nullable=False, unique=True)
    Estado = db.Column(db.SmallInteger, nullable=False)
