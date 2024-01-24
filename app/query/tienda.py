import logging

class tienda:
    def __init__(self, database):
        self.db = database
        self.db.connect()
        self.db.rollback()

    def create_tables(self):
        try:
            self.create_table_videojuego()
            self.create_table_compra()
            self.db.commit()
            return True
        except Exception as ex:
            logging.error("Error creating tables: ", ex)
            self.db.rollback()
            return False
  
    def create_table_videojuego(self):
        try:
            self.db.execute("CREATE TABLE Videojuego ("
                            "Titulo_Videojuego VARCHAR(30),"
                            "Nombre_Usuario VARCHAR(20),"
                            "Genero VARCHAR(20),"
                            "Precio INTEGER,"
                            "Version VARCHAR(20),"
                            "FOREIGN KEY (Titulo_Videojuego) REFERENCES Articulo(Titulo),"
                            "FOREIGN KEY (Nombre_Usuario) REFERENCES Usuario(Nombre_Usuario),"
                            "PRIMARY KEY (Titulo_Videojuego))")
        
        except Exception as ex:
            logging.error("Error creating Tienda table: ", ex)
            self.db.rollback()
 
    def create_table_compra(self):
        try:
            self.db.execute("CREATE TABLE Compra ("
                            "Titulo_Videojuego VARCHAR(30),"
                            "Nombre_Usuario VARCHAR(20),"
                            "Fecha_Transaccion DATETIME,"
                            "FOREIGN KEY (Titulo_Videojuego) REFERENCES Articulo(Titulo),"
                            "FOREIGN KEY (Nombre_Usuario) REFERENCES Usuario(Nombre_Usuario),"
                            "PRIMARY KEY (Titulo_Videojuego, Nombre_Usuario))")
            
            self.db.execute("CREATE TRIGGER actualizar_saldo AFTER INSERT ON Compra "
                            "FOR EACH ROW "
                            "BEGIN "
                            "DECLARE precio_videojuego DECIMAL(10, 2); "
                            "DECLARE saldo_actual DECIMAL(10, 2); "
                            "SET precio_videojuego = (SELECT Precio FROM Videojuego WHERE Titulo_Videojuego = NEW.Titulo_Videojuego); "
                            "SET saldo_actual = (SELECT Saldo FROM Usuario WHERE Nombre_Usuario = NEW.Nombre_Usuario); "
                            "IF saldo_actual >= precio_videojuego THEN "
                            "   UPDATE Usuario SET Saldo = Saldo - precio_videojuego WHERE Nombre_Usuario = NEW.Nombre_Usuario; "
                            "ELSE "
                            "   SIGNAL SQLSTATE '45000' "
                            "   SET MESSAGE_TEXT = 'Error: Saldo insuficiente para realizar la compra'; "
                            "END IF; "
                            "END;"
                        )



        
        except Exception as ex:
            logging.error("Error creating Compra table:", ex)
            
            
    def insert_videojuego(self, titulo_videojuego, precio, version, nombre_usuario, genero):
        try:
            self.db.execute(f"SELECT * FROM Videojuego WHERE Titulo_Videojuego = '{titulo_videojuego}'")
            if self.db.fetchone() is not None:
                return "El videojuego ya existe", False
            self.db.execute(f"INSERT INTO Videojuego(Titulo_Videojuego, Nombre_Usuario, Precio, Version, Genero) VALUES ('{titulo_videojuego}', '{nombre_usuario}', {precio}, '{version}', '{genero}')")
            self.db.commit()
            return "Juego creado correctamente", True
        except Exception as ex:
            logging.error("Error inserting videojuego: ", ex)
            self.db.rollback()
            return "Error inserting videojuego", False
        
    def delete_videojuego(self, cvideojuego,creador):
        try:
            #Comprobar si videojuego existe
            self.db.execute(f"SELECT * FROM Videojuego WHERE Titulo_Videojuego = '{cvideojuego}'")
            if self.db.fetchone() is None:
                return "El videojuego no existe", False
            self.db.execute(f"SELECT Nombre_Usuario FROM Videojuego WHERE Titulo_Videojuego = '{cvideojuego}'")
            escreador = self.db.fetchone()
            if escreador[0] != creador:
                return "No es el creador del videjuego", False
            self.db.execute(f"DELETE FROM Videojuego WHERE Titulo_Videojuego = '{cvideojuego}' AND Nombre_Usuario ='{creador}'")
            self.db.commit()
            return "Juego borrado correctamente", True
        except Exception as ex:
            logging.error("Error deleting videojuego: ", ex)
            self.db.rollback()
            return "Error deleting videojuego", False
        
    def update_version_videojuego(self, cvideojuego, version):
        try:
            #Comprobar si videojuego existe
            self.db.execute(f"SELECT * FROM Videojuego WHERE Titulo_Videojuego = '{cvideojuego}'")
            if self.db.fetchone() is None:
                return "El videojuego no existe", False
            self.db.execute(f"UPDATE Videojuego SET version = '{version}' WHERE Titulo_Videojuego = '{cvideojuego}'")
            self.db.commit()
            return "Version actulizada", True
        except Exception as ex:
            logging.error("Error updating version videojuego: ", ex)
            self.db.rollback()
            return "Error updating version videojuego", False
    
    def get_videojuego_por_genero(self, genero):
        try:
            self.db.execute(f"SELECT * FROM Videojuego WHERE genero = '{genero}'")
            return self.db.fetchall()
        except Exception as ex:
            logging.error("Error getting videojuego por genero: ", ex)
    
    def comprar_videojuego(self, cvideojuego, nombre_usuario):
        try:
            #Comprobar si videojuego existe
            self.db.execute(f"SELECT * FROM Videojuego WHERE Titulo_Videojuego = '{cvideojuego}'")
            if self.db.fetchone() is None:
                return "El videojuego no existe", False
            #Comprobar si el videojuego ya ha sido comprado
            self.db.execute(f"SELECT * FROM Compra WHERE Titulo_Videojuego = '{cvideojuego}' AND Nombre_Usuario = '{nombre_usuario}'")
            if self.db.fetchone() is not None:
                return "El videojuego ya ha sido comprado por el usuario", False
            self.db.execute(f"INSERT INTO Compra VALUES ('{cvideojuego}', '{nombre_usuario}', CURRENT_DATE)")
            self.db.commit()
            self.db.execute(f"SELECT Saldo FROM Usuario WHERE Nombre_Usuario = '{nombre_usuario}'")
            saldo_actualizado = self.db.fetchone()[0]
            return saldo_actualizado, True
        except Exception as ex:
            if "Saldo insuficiente" in str(ex):
                return "Saldo insuficiente", False
            logging.error("Error comprando videojuego: ", ex)
            self.db.rollback()
            return "Error comprando videojuego", False
        
    def add_saldo(self, cusuario, saldo):
        try:
            self.db.execute(f"UPDATE Usuario SET Saldo = Saldo + {saldo} WHERE Nombre_Usuario = '{cusuario}'")
            self.db.commit()
            self.db.execute(f"SELECT Saldo FROM Usuario WHERE Nombre_Usuario = '{cusuario}'")
            saldo_actualizado = self.db.fetchone()[0]
            return saldo_actualizado
        except Exception as ex:
            logging.error("Error adding saldo: ", ex)
            self.db.rollback()
            return False