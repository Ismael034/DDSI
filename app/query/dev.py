
import app.query.articulo as articulo
import app.query.social as social

class dev:
    def __init__(self, database):
        self.db = database
        self.db.connect()
        self.db.rollback()     

    def delete_tables(self):
        try:
            self.db.execute("DROP TABLE Creacion")
            self.db.execute("DROP TABLE Consultar_Creacion")
            self.db.execute("DROP TABLE Listar_Creacion")
            self.db.commit()
        
        except Exception as ex:
            print("Error deleting table: ", ex)
            self.db.rollback()

    def delete_table(self, name):
        try:
            self.db.execute(f"DROP TABLE {name}")
            return True
        
        except Exception as ex:
            print("Error deleting table: ", ex)
            self.db.rollback()
            return False

    def create_table_creacion(self):
        try:
            self.db.execute("CREATE TABLE Creacion ("
                            "Titulo_Creacion VARCHAR(100),"
                            "Tipo VARCHAR(16),"
                            "Videojuego_Asociado VARCHAR(100),"
                            "#Nombre_Usuario VARCHAR(20),"
                            "NumDescargas INTEGER,"
                            "Fecha_Subida DATE,"
                            "PRIMARY KEY (Titulo_Creacion) REFERENCES Articulo(#Titulo),"
                            "FOREIGN KEY (Videojuego_Asociado) REFERENCES Articulo(#Titulo)),"
                            "UNIQUE KEY (#Nombre_Usuario) REFERENCES Usuario(#Nombre_Usuario))")
        
        except Exception as ex:
            print("Error creating creacion table: ", ex)
            self.db.rollback()
 
    def create_table_creacion_consulta(self):
        try:
            self.db.execute("CREATE TABLE Consultar_Creacion ("
                            "Titulo_Creacion VARCHAR(100) REFERENCES Articulo(#Titulo),"
                            "#Nombre_Usuario VARCHAR(20) REFERENCES Usuario(#Nombre_Usuario)",
                            "PRIMARY KEY (Titulo_Creacion, #Nombre_Usuario)")
        
        except Exception as ex:
            print("Error creating creacion_consulta table:", ex)

    def create_table_creacion_lista(self):
        try:
            self.db.execute("CREATE TABLE Listar_Creacion ("
            		    "Titulo_Creacion VARCHAR(100) REFERENCES Articulo(#Titulo),"
                            "#Nombre_Usuario VARCHAR(20) REFERENCES Usuario(#Nombre_Usuario)",
                            "Tipo_a_listar VARCHAR(16)",
                            "PRIMARY KEY (Titulo_Creacion, #Nombre_Usuario, Tipo_a_listar))
        except Exception as ex:
            print("Error creating creacion_lista table: ", ex)


    def create_tables(self):
        try:
            self.create_table_creacion()
            self.create_table_creacion_lista()
            self.create_table_creacion_consulta()
            self.db.commit()
            return True
        except Exception as ex:
            print("Error creating tables: ", ex)
            self.db.rollback()
            return False
  
        
    def subir_creacion(self, titulo, tipo, vid, usu, fecha):
        try:
            self.db.execute(f"INSERT INTO Creacion(Titulo_Creacion) VALUES ({titulo})")
            self.db.execute(f"INSERT INTO Creacion(Tipo) VALUES ({tipo})")
            self.db.execute(f"INSERT INTO Creacion(Videojuego_Asociado) VALUES ({vid})")
            self.db.execute(f"INSERT INTO Creacion(#Nombre_Usuario) VALUES ({usu})")
            self.db.execute(f"INSERT INTO Creacion(NumDescargas) VALUES ({0})")
            self.db.execute(f"INSERT INTO Creacion(Fecha_Subida) VALUES ({fecha})")
            self.db.commit()
            return True
        except Exception as ex:
            print("Error subiendo creacion: ", ex)
            self.db.rollback()
            return False

    def consulta_creacion(self, nomb):
        try:
            self.db.execute("SELECT * FROM Creacion WHERE Titulo_Creacion = {nomb}")
            return self.db.fetchall()
        except Exception as ex:
            print("Error consulta creacion: ", ex)

    def listar_creaciones(self, t):
        try:
            self.db.execute(f"SELECT Titulo_Creacion FROM Creacion WHERE Tipo = {t}")
            return self.db.fetchone()
        except Exception as ex:
            print("Error listar creaciones: ", ex)

    def borrar_creacion(self, nomb):
        try:
            self.db.execute(f"DELETE FROM Creacion WHERE Titulo_Creacion = {nomb}")
            self.db.commit()
        except Exception as ex:
            print("Error deleting creacion: ", ex)
            self.db.rollback()

     
