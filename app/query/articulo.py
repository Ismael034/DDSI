class articulo:
    def __init__(self, database):
        self.db = database
        self.db.connect()
        self.db.rollback()     

    def delete_table(self):
        try:
            self.db.execute(f"DROP TABLE Articulo")
            return True
        
        except Exception as ex:
            print("Error deleting table Articulo: ", ex)
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
                            "Estadisticas VARCHAR(50),"
                            "Ejecutable VARCHAR(50),"
                            "Especificaciones VARCHAR(500),"
                            )
        
        except Exception as ex:
            print("Error creating table Articulo: ", ex)
            self.db.rollback()

    def subir_articulo(self, titulo, tamano, desc, desl, genero, icono, est, eje, esp):
        try:
            self.db.execute(f"INSERT INTO Articulo(Titulo,Tamaño,Descripcion_corta,Descripcion_larga,Genero,Icono,Estadisticas,Ejecutable,Especificaciones) VALUES ({titulo}, {tamano},{desc}, {desl}, {genero}, {icono}, {est}, {eje}, {esp})")
            self.db.commit()
            return True
        except Exception as ex:
            print("Error inserting Articulo: ", ex)
            self.db.rollback()
            return False

    def consultar_articulo(self,titulo):
        try:
            self.db.execute(f"SELECT * FROM Articulo WHERE Titulo = {titulo}")
            return self.db.fetchall()
        except Exception as ex:
            print("Error getting Articulo: ", ex)

    def create_table_articulo_obtenido(self):
        try:
            self.db.execute("CREATE TABLE Articulo_obtenido("
                            "Nombre_usuario FOREIGN KEY REFERENCES Usuario(Nombre_Usuario),"
                            "Titulo_articulo FOREIGN KEY REFERENCES Articulo(Titulo),"
                            "Ult_vez_jugado DATETIME,"
                            "PRIMARY KEY (Nombre_usuario,Titulo_articulo)"
                            ")")
        except Exception as ex:
            print("Error creating table Articulo_obtenido: ", ex)
            self.db.rollback()

    def consultar_articulos(self,user,n):
        if n<0:
            n=0
        try:
            self.db.execute(f"SELECT Titulo FROM Articulo_obtenido WHERE Nombre_usuario = {user} LIMIT {n} ORDER BY Ult_vez_jugado")
            return self.db.fetchall()
        except Exception as ex:
            print("Error al mostrar los articulos obtenidos: ", ex)

    def ejecuta(self, user, juego):
        try:
            self.db.execute(f"UPDATE Articulo_obtenido WHERE Nombre_usuario = {user} AND Titulo_articulo = {juego} SET Ult_vez_jugado = CURRENT_DATE")
            self.db.commit()
            return True
        except Exception as ex:
            print("Error al ejecutar el artículo: ", ex)
    
    def create_table_valoracion(self):
        try:
            self.db.execute("CREATE TABLE Valoracion ("
                            "Nombre_usuario FOREIGN KEY REFERENCES Usuario(Nombre_Usuario),"
                            "Titulo_articulo FOREIGN KEY REFERENCES Articulo(Titulo),"
                            "Puntuacion INTEGER CHECK (Puntuacion > 0 AND Puntuacion < 6)"
                            "Comentario VARCHAR(500),"
                            "PRIMARY KEY (Nombre_usuario,Titulo_articulo)"
                            )
        except Exception as ex:
            print("Error creating table Valoracion: ", ex)
            self.db.rollback()

    def comentar(self,usr,articulo,punt,com):
        try:
            self.db.execute(f"INSERT INTO Valoracion(Nombre_usuario,Titulo_articulo,Puntuacion,Comentario) VALUES ({usr},{articulo},{punt},{com})")
            self.db.commit()
            return True
        except Exception as ex:
            print("Error inserting Valoracion: ", ex)
            self.db.rollback()
            return False