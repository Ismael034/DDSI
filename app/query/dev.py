
import app.query.articulo as articulo
import app.query.social as social
import logging

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
            logging.error("Error deleting table: ", ex)
            self.db.rollback()

    def delete_table(self, name):
        try:
            self.db.execute(f"DROP TABLE {name}")
            return True
        
        except Exception as ex:
            logging.error("Error deleting table: ", ex)
            self.db.rollback()
            return False

    def create_table_creacion(self):
        try:
            self.db.execute("CREATE TABLE Creacion ("
                            "Titulo_Creacion VARCHAR(100),"
                            "Tipo VARCHAR(16),"
                            "Nombre_Usuario VARCHAR(20),"
                            "NumDescargas INTEGER,"
                            "Fecha_Subida DATETIME,"
                            "Modificacion_activada BOOLEAN,"
                            "FOREIGN KEY (Titulo_Creacion) REFERENCES Articulo(Titulo),"
                            "FOREIGN KEY (Nombre_Usuario) REFERENCES Usuario(Nombre_Usuario),"
                            "PRIMARY KEY (Titulo_Creacion))")
                            
            self.db.execute("CREATE TRIGGER tipo_creacion_valido Before INSERT ON Creacion "
                            "FOR EACH ROW "
                            "BEGIN "
                            "IF NEW.Tipo != 'MOD_JUGABLE' and NEW.Tipo != 'MOD_GRAFICO' and NEW.Tipo != 'TEXTURE_PACK' and NEW.Tipo != 'BETA' and NEW.Tipo != 'DEMO' and NEW.Tipo != 'FANGAME' and NEW.Tipo != 'JUEGO_COMPLETO' THEN "
                            "   SIGNAL SQLSTATE '45000' "
                            "   SET MESSAGE_TEXT = 'Error: La creacion subida no tiene un tipo valido'; "
                            "END IF; "
                            "END;"
                        )	
        
        except Exception as ex:
            logging.error("Error creating creacion table: ", ex)
            self.db.rollback()
 
    def create_table_creacion_consulta(self):
        try:
            self.db.execute("CREATE TABLE Consultar_Creacion ("
                            "Titulo_Creacion VARCHAR(100),"
                            "Nombre_Usuario VARCHAR(20),"
                            "FOREIGN KEY (Titulo_Creacion) REFERENCES Articulo(Titulo),"
                            "FOREIGN KEY (Nombre_Usuario) REFERENCES Usuario(Nombre_Usuario),"
                            "PRIMARY KEY (Titulo_Creacion, Nombre_Usuario)")
        
        except Exception as ex:
            logging.error("Error creating creacion_consulta table:", ex)

    def create_table_creacion_lista(self):
        try:
            self.db.execute("CREATE TABLE Listar_Creacion ("
            		    "Titulo_Creacion VARCHAR(100) REFERENCES Articulo(Titulo),"
                            "Nombre_Usuario VARCHAR(20) REFERENCES Usuario(Nombre_Usuario),"
                            "Tipo_a_listar VARCHAR(16),"
                            "PRIMARY KEY (Titulo_Creacion, Nombre_Usuario, Tipo_a_listar)")
        except Exception as ex:
            logging.error("Error creating creacion_lista table: ", ex)


    def create_tables(self):
        try:
            self.create_table_creacion()
            #self.create_table_creacion_lista()
            #self.create_table_creacion_consulta()
            self.db.commit()
            return True
        except Exception as ex:
            logging.error("Error creating tables: ", ex)
            self.db.rollback()
            return False
  
        
    def subir_creacion(self, titulo, tipo, usu):
        try:
        
            self.db.execute(f"INSERT INTO Creacion(Titulo_Creacion,Tipo,Nombre_Usuario,NumDescargas,Fecha_Subida,Modificacion_activada) VALUES ('{titulo}', '{tipo}', '{usu}', '0', NOW(), '0')")
            self.db.commit()
            return True
        except Exception as ex:
            logging.error("Error subiendo creacion: ", ex)
            self.db.rollback()
            return False

    def consulta_creacion(self, nomb):
        try:
            self.db.execute(f"SELECT * FROM Creacion WHERE Titulo_Creacion = '{nomb}'")
            return self.db.fetchall()
        except Exception as ex:
            logging.error("Error consulta creacion: ", ex)

    def listar_creaciones(self, t):
        try:
            self.db.execute(f"SELECT Titulo_Creacion FROM Creacion WHERE Tipo = '{t}'")
            return self.db.fetchone()
        except Exception as ex:
            logging.error("Error listar creaciones: ", ex)

    def borrar_creacion(self, nomb, usr):
        try:
            self.db.execute(f"DELETE FROM Creacion WHERE Titulo_Creacion = '{nomb}' AND Nombre_Usuario = '{usr}'")
            self.db.commit()
        except Exception as ex:
            logging.error("Error deleting creacion: ", ex)
            self.db.rollback()

    def activar_mod(self, nomb):
        self.db.execute(f"SELECT Tipo FROM Creacion WHERE Titulo_Creacion = '{nomb}'")
        a = self.db.fetchone()[0]
        if a == "MOD_JUGABLE" or a == "MOD_GRAFICO" or a == "TEXTURE_PACK":
            try:
                self.db.execute(f"UPDATE Creacion SET Modificacion_activada = 1 WHERE Titulo_Creacion = '{nomb}'")
            except Exception as ex:
                logging.error("Error al activar modificación",ex)
                self.db.rollback()
        else:
            logging.error("Esta creacion no es una modificacion\n")
