import logging

class articulo:
    def __init__(self, database):
        self.db = database
        self.db.connect()
        self.db.rollback()     

    def create_tables(self):
        try:
            self.create_table_articulo()
            self.create_table_articulo_obtenido()
            self.create_table_valoracion()
            self.db.commit()
            return True
        except Exception as ex:
            logging.error("Error creating tables: ", ex)
            self.db.rollback()
            return False
  

    def delete_table(self):
        try:
            self.db.execute(f"DROP TABLE Articulo")
            return True
        
        except Exception as ex:
            logging.error("Error deleting table Articulo: ", ex)
            self.db.rollback()
            return False

    def create_table_articulo(self):
        try:
            self.db.execute("CREATE TABLE Articulo ("
                            "Titulo VARCHAR(100) PRIMARY KEY,"
                            "Tamaño VARCHAR(20),"
                            "Descripcion_corta VARCHAR(200),"
                            "Descripcion_larga VARCHAR(1000),"
                            "Genero VARCHAR(20),"
                            "Icono VARCHAR(50),"
                            "Ejecutable VARCHAR(50),"
                            "Especificaciones VARCHAR(500))"
                            )
        
        except Exception as ex:
            logging.error("Error creating table Articulo: ", ex)
            self.db.rollback()

    def subir_articulo(self, titulo, tamano, desc, desl, genero, icono, eje, esp):
        try:
            self.db.execute(f"INSERT INTO Articulo(Titulo,Tamaño,Descripcion_corta,Descripcion_larga,Genero,Icono,Ejecutable,Especificaciones) VALUES ('{titulo}', '{tamano}','{desc}', '{desl}', '{genero}', '{icono}', '{eje}', '{esp}')")
            self.db.commit()
            return True
        except Exception as ex:
            logging.error("Error inserting Articulo: ", ex)
            self.db.rollback()
            return False

    def eliminar_articulo(self,titulo):
        try:
            self.db.execute(f"DELETE FROM Articulo WHERE Titulo = '{titulo}'")
            self.db.commit()
        except Exception as ex:
            logging.error("Error eliminar articulo: ", ex)

    def consultar_articulo(self,titulo):
        try:
            self.db.execute(f"SELECT * FROM Articulo WHERE Titulo = '{titulo}'")
            return self.db.fetchall()
        except Exception as ex:
            logging.error("Error getting Articulo: ", ex)

    def create_table_articulo_obtenido(self):
        try:
            self.db.execute("CREATE TABLE Articulo_obtenido("
                            "Nombre_usuario VARCHAR(20) REFERENCES Usuario(Nombre_Usuario),"
                            "Titulo_articulo VARCHAR(100) REFERENCES Articulo(Titulo),"
                            "Ult_vez_jugado DATETIME,"
                            "Estadisticas VARCHAR(150),"
                            "PRIMARY KEY (Nombre_usuario,Titulo_articulo))")

            self.db.execute("CREATE TRIGGER anadir_articulo_usuario AFTER INSERT ON Articulo_obtenido "
                            "FOR EACH ROW "
                            "BEGIN "
                            "DECLARE new_articulo VARCHAR(200);"
                            "SET new_articulo = NEW.Titulo_articulo;"
                            "UPDATE Usuario "
                            "SET Articulos_adquiridos = CONCAT(Articulos_adquiridos,new_articulo,', ') "
                            "WHERE Nombre_Usuario = NEW.Nombre_usuario;"
                            "END;"
                            )
        except Exception as ex:
            logging.error("Error creating table Articulo_obtenido: ", ex)
            self.db.rollback()
            
    def anadir_articulo_obtenido(self,user,articulo):
        try:
            total = "Tiempo de juego total 0, Tiempo medio de juego por semana 0"
            self.db.execute(f"INSERT INTO Articulo_obtenido(Nombre_usuario,Titulo_articulo,Estadisticas) VALUES ('{user}','{articulo}','{total}')")
            self.db.commit()
            return True
        except Exception as ex:
            logging.error("Error inserting Articulo_obtenido: ", ex)
            self.db.rollback()
            return False

    def eliminar_articulo_obtenido(self,user,articulo):
        try:
            self.db.execute(f"DELETE FROM Articulo_obtenido WHERE Titulo_articulo = '{articulo}' AND Nombre_usuario = '{user}'")
            self.db.commit()
        except Exception as ex:
            logging.error("Error eliminar articulo obtenido: ", ex)

    def consultar_articulos(self,user,nn):
        n = int(nn)
        if n<0:
            n=0
        try:
            self.db.execute(f"SELECT Titulo_articulo, Ult_vez_jugado, Estadisticas FROM Articulo_obtenido WHERE Nombre_usuario = '{user}' ORDER BY Ult_vez_jugado LIMIT {n}")
            return self.db.fetchall()
        except Exception as ex:
            logging.error("Error al mostrar los articulos obtenidos: ", ex)

    def consultar_articulo_obtenido(self,user,titulo):
        try:
            self.db.execute(f"SELECT Titulo_articulo, Ult_vez_jugado, Estadisticas FROM Articulo_obtenido WHERE Nombre_usuario = '{user}' AND Titulo_articulo = '{titulo}'")
            return self.db.fetchall()
        except Exception as ex:
            logging.error("Error al mostrar articulo obtenido: ", ex)

    def ejecuta(self, user, juego):
        try:
            #data = est.json.loads(est.data)
            #total = "Tiempo de juego total "+data.record['ttotal']+", Tiempo medio de juego por semana "+data.record['tmedio']
            total = "EJECUTADO"
            self.db.execute(f"UPDATE Articulo_obtenido SET Ult_vez_jugado = NOW(), Estadisticas = '{total}' WHERE Nombre_usuario = '{user}' AND Titulo_articulo = '{juego}'")
            self.db.commit()
            return True
        except Exception as ex:
            logging.error("Error al ejecutar el artículo: ", ex)
            return False
    
    def create_table_valoracion(self):
        try:
            self.db.execute("CREATE TABLE Valoracion ("
                            "Nombre_usuario VARCHAR(20) REFERENCES Usuario(Nombre_Usuario),"
                            "Titulo_articulo VARCHAR(100) REFERENCES Articulo(Titulo),"
                            "Puntuacion INTEGER CHECK (Puntuacion > 0 AND Puntuacion < 6),"
                            "Comentario VARCHAR(500),"
                            "PRIMARY KEY (Nombre_usuario,Titulo_articulo))")
        except Exception as ex:
            logging.error("Error creating table Valoracion: ", ex)
            self.db.rollback()

    def comentar(self,usr,articulo,punt,com):
        try:
            self.db.execute(f"INSERT INTO Valoracion(Nombre_usuario,Titulo_articulo,Puntuacion,Comentario) VALUES ('{usr}','{articulo}','{punt}','{com}')")
            self.db.commit()
            return True
        except Exception as ex:
            logging.error("Error inserting Valoracion: ", ex)
            self.db.rollback()
            return False
    
    def consultar_valoracion(self,user,articulo):
        try:
            self.db.execute(f"SELECT Titulo_articulo, Puntuacion, Comentario FROM Valoracion WHERE Nombre_usuario = '{user}' AND Titulo_articulo = '{articulo}'")
            return self.db.fetchall()
        except Exception as ex:
            logging.error("Error al mostrar valoracion: ", ex)
