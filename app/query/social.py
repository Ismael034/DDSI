class social:
    def __init__(self, database):
        self.db = database
        self.db.connect()
        self.db.rollback()     

    def delete_tables(self):
        try:
            self.db.execute("DROP TABLE Usuario")
            self.db.execute("DROP TABLE Perfil")
            self.db.execute("DROP TABLE Amistad")
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



    def create_table_usuario(self):
        try:
            self.db.execute("CREATE TABLE Usuario ("
                            "Nombre_Usuario VARCHAR(20) PRIMARY KEY,"
                            "Saldo INTEGER,"
                            "Nombre VARCHAR(20),"
                            "Password VARCHAR(100),"
                            "Artículos_adquiridos VARCHAR(20))")
        
        except Exception as ex:
            print("Error creating usuario table:", ex)

    def create_table_perfil(self):
        try:
            self.db.execute("CREATE TABLE Perfil ("
                            "Nombre_Usuario VARCHAR(20),"
                            "Email VARCHAR(20),"
                            "Fotografía BLOB,"
                            "Biografía VARCHAR(300),"
                            "Logros VARCHAR(300),"
                            "Artículos_adquiridos VARCHAR(20)",
                            "FOREIGN KEY (Nombre_Usuario) REFERENCES Usuario(Nombre_Usuario)",
                            "FOREIGN KEY (Artículos_adquiridos) REFERENCES Usuario(Artículos_adquiridos)",
                            "PRIMARY KEY (Nombre_Usuario, Email)")
        
        except Exception as ex:
            print("Error creating stock perfil: ", ex)
            self.db.rollback()

    def create_table_amistad(self):
        try:
            self.db.execute("CREATE TABLE Amistad ("
                            "Nombre_Usuario VARCHAR(20) PRIMARY KEY,"
                            "Amigo VARCHAR(20),"
                            "Aceptada BOOLEAN,"
                            "FOREIGN KEY (Nombre_Usuario) REFERENCES Usuario(Nombre_Usuario),"
                            "FOREIGN KEY (Amigo) REFERENCES Usuario(Nombre_Usuario))")
        except Exception as ex:
            print("Error creating articulo table: ", ex)

    def create_tables(self):
        try:
            self.create_table_usuario()
            self.create_table_perfil()
            self.create_table_amistad()
            self.db.commit()
            return True
        except Exception as ex:
            print("Error creating tables: ", ex)
            self.db.rollback()
            return False



    def get_usuario_by_id(self, nombre_usuario):
        try:
            self.db.execute(f"SELECT * FROM Usuario WHERE Nombre_Usuario = '{nombre_usuario}'")
            return self.db.fetchone()
        except Exception as ex:
            print("Error getting usuario: ", ex)

    def insert_usuario(self, nombre_usuario, nombre, password):
        try:
            self.db.execute(f"INSERT INTO Usuario VALUES ('{nombre_usuario}', 0,"
                            "'{nombre}', '{password}', '')")
            return True
        except Exception as ex:
            print("Error inserting stock: ", ex)
            self.db.rollback()
            return False
    
    def update_usuario(self, nombre_usuario, nombre, password, articulos_adquiridos):
        try:
            self.db.execute(f"UPDATE Usuario SET nombre = '{nombre}', password = '{password}',"
                            "articulos_adquiridos = '{articulos_adquiridos}' WHERE nombre_usuario = '{nombre_usuario}'")
            self.db.commit()
            return True
        except Exception as ex:
            print("Error updating usuario: ", ex)
            self.db.rollback()
            return False

    def update_saldo(self, nombre_usuario, saldo):
        try:
            self.db.execute(f"UPDATE Usuario SET saldo = {saldo} WHERE nombre_usuario = '{nombre_usuario}'")
            self.db.commit()
            return True
        except Exception as ex:
            print("Error updating saldo: ", ex)
            self.db.rollback()
            return False
            
    def delete_usuario(self, nombre_usuario):
        try:
            self.db.execute(f"DELETE FROM Usuario WHERE nombre_usuario = '{nombre_usuario}'")
            self.db.commit()
            return True
        except Exception as ex:
            print("Error deleting usuario: ", ex)
            self.db.rollback()
            return False



    def get_perfil_by_id(self, nombre_usuario, email):
        try:
            self.db.execute(f"SELECT * FROM Perfil WHERE Nombre_Usuario = '{nombre_usuario}' AND Email = '{email}'")
            return self.db.fetchone()
        except Exception as ex:
            print("Error getting perfil: ", ex)

    def insert_perfil(self, nombre_usuario, email, fotografia, biografia, logros, articulos_adquiridos):
        try:
            self.db.execute(f"INSERT INTO Perfil VALUES ('{nombre_usuario}', '{email}', '{fotografia}',"
                            "'{biografia}', '{logros}', '{articulos_adquiridos}')")
            return True
        except Exception as ex:
            print("Error inserting perfil: ", ex)
            self.db.rollback()
            return False

    def update_perfil(self, nombre_usuario, email, fotografia, biografia, logros, articulos_adquiridos):
        try:
            self.db.execute(f"UPDATE Perfil SET fotografia = '{fotografia}', biografia = '{biografia}',"
                            "logros = '{logros}', articulos_adquiridos = '{articulos_adquiridos}'"
                            "WHERE nombre_usuario = '{nombre_usuario}' AND email = '{email}'")
            self.db.commit()
            return True
        except Exception as ex:
            print("Error updating perfil: ", ex)
            self.db.rollback()
            return False

    def delete_perfil(self, nombre_usuario, email):
        try:
            self.db.execute(f"DELETE FROM Perfil WHERE nombre_usuario = '{nombre_usuario}' AND email = '{email}'")
            self.db.commit()
            return True
        except Exception as ex:
            print("Error deleting perfil: ", ex)
            self.db.rollback()
            return False


    def get_amistad_by_id(self, nombre_usuario):
        try:
            self.db.execute(f"SELECT * FROM Amistad WHERE Nombre_Usuario = '{nombre_usuario}'")
            return self.db.fetchone()
        except Exception as ex:
            print("Error getting amistad: ", ex)

    def insert_amistad(self, nombre_usuario, amigo):
        try:
            self.db.execute(f"INSERT INTO Amistad VALUES ('{nombre_usuario}', '{amigo}', {false})")
            return True
        except Exception as ex:
            print("Error inserting amistad: ", ex)
            self.db.rollback()
            return False

    def accept_amistad(self, nombre_usuario, amigo):
        try:
            self.db.execute(f"UPDATE Amistad SET aceptada = {true} WHERE nombre_usuario = '{nombre_usuario}' AND amigo = '{amigo}'")
            self.db.commit()
            return True
        except Exception as ex:
            print("Error accepting amistad: ", ex)
            self.db.rollback()
            return False

    def delete_amistad(self, nombre_usuario, amigo):
        try:
            self.db.execute(f"DELETE FROM Amistad WHERE nombre_usuario = '{nombre_usuario}' AND amigo = '{amigo}'")
            self.db.commit()
            return True
        except Exception as ex:
            print("Error deleting amistad: ", ex)
            self.db.rollback()
            return False
    
     
