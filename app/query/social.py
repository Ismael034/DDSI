import logging

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

    def create_tables(self):
        try:
            self.create_table_usuario()
            self.create_table_perfil()
            self.create_table_amistad()
            self.db.commit()
            return True
        except Exception as ex:
            logging.error("Error creating tables: ", ex)
            self.db.rollback()
            return False
  

    def create_table_usuario(self):
        try:
            self.db.execute("CREATE TABLE Usuario ("
                            "Nombre_Usuario VARCHAR(20) PRIMARY KEY,"
                            "Email VARCHAR(20),"
                            "Saldo INTEGER,"
                            "Nombre VARCHAR(20),"
                            "Password VARCHAR(100),"
                            "Activo BOOLEAN,"
                            "Articulos_adquiridos VARCHAR(200))")

        except Exception as ex:
            logging.error("Error creating usuario table:", ex)

    def create_table_perfil(self):
        try:
            self.db.execute("CREATE TABLE Perfil ("
                            "Nombre_Usuario VARCHAR(20),"
                            "Fotografia VARCHAR(50),"
                            "Biografia VARCHAR(300),"
                            "Logros VARCHAR(300),"
                            "FOREIGN KEY (Nombre_Usuario) REFERENCES Usuario(Nombre_Usuario),"
                            "PRIMARY KEY (Nombre_Usuario))")

            self.db.execute("CREATE TRIGGER crear_perfil AFTER INSERT ON Usuario "
                                "FOR EACH ROW "
                                "BEGIN "
                                "INSERT INTO Perfil VALUES (NEW.Nombre_Usuario, '', '', '');"
                                "END;")
        except Exception as ex:
            logging.error("Error creating perfil: ", ex)
            self.db.rollback()

    def create_table_amistad(self):
        try:
            self.db.execute("CREATE TABLE Amistad ("
                            "Nombre_Usuario VARCHAR(20),"
                            "Amigo VARCHAR(20),"
                            "Aceptada BOOLEAN,"
                            "FOREIGN KEY (Nombre_Usuario) REFERENCES Usuario(Nombre_Usuario),"
                            "FOREIGN KEY (Amigo) REFERENCES Usuario(Nombre_Usuario),"
                            "PRIMARY KEY (Nombre_Usuario, Amigo))")
        except Exception as ex:
            logging.error("Error creating articulo table: ", ex)





    def get_usuario_by_id(self, nombre_usuario):
        try:
            self.db.execute(f"SELECT * FROM Usuario WHERE Nombre_Usuario = '{nombre_usuario}' AND activo = TRUE")
            return self.db.fetchone()
        except Exception as ex:
            logging.error("Error getting usuario: ", ex)

    def get_perfil_by_id(self, nombre_usuario):
        try:
            self.db.execute(f"SELECT * FROM Perfil WHERE Nombre_Usuario = '{nombre_usuario}'")
            return self.db.fetchone()
        except Exception as ex:
            logging.error("Error getting perfil: ", ex)

    def insert_usuario(self, nombre_usuario, nombre, email, password, saldo, articulos_adquiridos):
        try:
            self.db.execute(f"INSERT INTO Usuario VALUES ('{nombre_usuario}', '{email}', '{saldo}', '{nombre}', '{password}', TRUE, '{articulos_adquiridos}')")
            self.db.commit()
            return True
        except Exception as ex:
            logging.error("Error inserting usuario: ", ex)
            self.db.rollback()
            return False


    def update_articulos_adquiridos(self, nombre_usuario, articulos_adquiridos):
        try:
            self.db.execute(f"UPDATE Usuario SET articulos_adquiridos = '{articulos_adquiridos}' WHERE nombre_usuario = '{nombre_usuario}'")
            self.db.commit()
            return True
        except Exception as ex:
            logging.error("Error updating articulos_adquiridos: ", ex)
            self.db.rollback()
            return False

    def get_saldo_by_id(self, nombre_usuario):
        try:
            self.db.execute(f"SELECT saldo FROM Usuario WHERE Nombre_Usuario = '{nombre_usuario}'")
            return self.db.fetchone()[0]
        except Exception as ex:
            logging.error("Error getting saldo: ", ex)

    def update_saldo(self, nombre_usuario, saldo):
        try:
            self.db.execute(f"UPDATE Usuario SET saldo = Saldo + {saldo} WHERE nombre_usuario = '{nombre_usuario}'")
            self.db.commit()
            return True
        except Exception as ex:
            logging.error("Error updating saldo: ", ex)
            self.db.rollback()
            return False
            
    def delete_usuario(self, nombre_usuario):
        try:
            self.db.execute(f"UPDATE Usuario SET activo = FALSE WHERE nombre_usuario = '{nombre_usuario}'")
            self.db.commit()
            return True
        except Exception as ex:
            logging.error("Error deleting usuario: ", ex)
            self.db.rollback()
            return False



    def get_perfil_by_id(self, nombre_usuario):
        try:
            self.db.execute(f"SELECT * FROM Perfil WHERE Nombre_Usuario = '{nombre_usuario}'")
            return self.db.fetchone()
        except Exception as ex:
            logging.error("Error getting perfil: ", ex)

    def insert_perfil(self, nombre_usuario, email, fotografia, biografia, logros):
        try:
            self.db.execute(f"INSERT INTO Perfil VALUES ('{nombre_usuario}', '{fotografia}','{biografia}', '{logros}')")
            self.db.commit()
            return True
        except Exception as ex:
            logging.error("Error inserting perfil: ", ex)
            self.db.rollback()
            return False

    def update_perfil(self, nombre_usuario, fotografia, biografia, logros):
        try:
            self.db.execute(f"UPDATE Perfil SET fotografia = '{fotografia}', biografia = '{biografia}', logros = '{logros}' WHERE nombre_usuario = '{nombre_usuario}'")
            self.db.commit()
            return True
        except Exception as ex:
            logging.error("Error updating perfil: ", ex)
            self.db.rollback()
            return False

    def delete_perfil(self, nombre_usuario):
        try:
            self.db.execute(f"DELETE FROM Perfil WHERE nombre_usuario = '{nombre_usuario}'")
            self.db.commit()
            return True
        except Exception as ex:
            logging.error(f"Error deleting perfil: {ex}")
            self.db.rollback()
            return False


    def get_amistad_by_id(self, nombre_usuario):
        try:
            self.db.execute(f"SELECT * FROM Amistad WHERE Nombre_Usuario = '{nombre_usuario}' OR Amigo = '{nombre_usuario}'")
            return self.db.fetchall()
        except Exception as ex:
            logging.error("Error getting amistad: ", ex)
            

    def insert_amistad(self, nombre_usuario, amigo):
        try:
            self.db.execute(f"INSERT INTO Amistad VALUES ('{nombre_usuario}', '{amigo}', FALSE)")
            self.db.commit()
            return True
        except Exception as ex:
            logging.error("Error inserting amistad: ", ex)
            self.db.rollback()
            return False

    def accept_amistad(self, nombre_usuario, amigo):
        try:
            self.db.execute(f"UPDATE Amistad SET aceptada = TRUE WHERE amigo = '{nombre_usuario}' AND nombre_usuario = '{amigo}'")
            self.db.commit()
            return True
        except Exception as ex:
            logging.error("Error accepting amistad: ", ex)
            self.db.rollback()
            return False

    def delete_amistad(self, nombre_usuario, amigo):
        try:
            self.db.execute(f"DELETE FROM Amistad WHERE (nombre_usuario = '{nombre_usuario}' AND amigo = '{amigo}') OR (nombre_usuario = '{amigo}' AND amigo = '{nombre_usuario}')")
            self.db.commit()
            return True
        except Exception as ex:
            logging.error("Error deleting amistad: ", ex)
            self.db.rollback()
            return False
    
     
