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
            print("Error creating tables: ", ex)
            self.db.rollback()
            return False
  
    def create_table_videojuego(self):
        try:
            self.db.execute("CREATE TABLE Videojuego ("
                            "Titulo_Videojuego VARCHAR(30),"
                            "Nombre_Usuario VARCHAR(20),"
                            "Genero VARCHAR(20),"
                            "Precio INTEGER,"
                            "Version INTEGER,"
                            "UNIQUE (Titulo_Videojuego),"
                            "FOREIGN KEY (Nombre_Usuario) REFERENCES Usuario(Nombre_Usuario))")
        
        except Exception as ex:
            print("Error creating Tienda table: ", ex)
            self.db.rollback()
 
    def create_table_compra(self):
        try:
            self.db.execute("CREATE TABLE Compra ("
                            "Titulo_Videojuego VARCHAR(30),"
                            "Nombre_Usuario VARCHAR(20),"
                            "Fecha_Transaccion DATETIME),"
                            "PRIMARY KEY (Titulo_Videojuego, Nombre_Usuario),"
                            "FOREIGN KEY (Titulo_Videojuego) REFERENCES Videojuego(Titulo_Videojuego),"
                            "FOREIGN KEY (Nombre_Usuario) REFERENCES Usuario(Nombre_Usuario))")
        
        except Exception as ex:
            print("Error creating Compra table:", ex)
            
            
    def insert_videojuego(self, titulo_videojuego, precio, version, nombre_usuario, genero):
        try:
            self.db.execute(f"INSERT INTO Videojuego VALUES ('{titulo}', '{nombre}', {precio}, {version}, {genero})")
            self.db.commit()
            return True
        except Exception as ex:
            print("Error inserting videojuego: ", ex)
            self.db.rollback()
            return False
        
    def delete_videojuego(self, cvideojuego):
        try:
            self.db.execute(f"DELETE FROM Videojuego WHERE cvideojuego = {cvideojuego}")
            self.db.commit()
            return True
        except Exception as ex:
            print("Error deleting videojuego: ", ex)
            self.db.rollback()
            return False
        
    def update_version_videojuego(self, cvideojuego, version):
        try:
            self.db.execute(f"UPDATE Videojuego SET version = {version} WHERE cvideojuego = {cvideojuego}")
            self.db.commit()
            return True
        except Exception as ex:
            print("Error updating version videojuego: ", ex)
            self.db.rollback()
            return False
    
    def get_videojuego_por_genero(self, genero):
        try:
            self.db.execute(f"SELECT * FROM Videojuego WHERE genero = '{genero}'")
            return self.db.fetchall()
        except Exception as ex:
            print("Error getting videojuego por genero: ", ex)
    
    def comprar_videojuego(self, cvideojuego, nombre_usuario):
        try:
            self.db.execute(f"INSERT INTO Compra VALUES ({cvideojuego}, {nombre_usuario}, CURRENT_DATE)")
            self.db.commit()
            return True
        except Exception as ex:
            print("Error comprando videojuego: ", ex)
            self.db.rollback()
            return False
        
    def add_saldo(self, cusuario, saldo):
        try:
            self.db.execute(f"UPDATE Usuario SET Saldo = Saldo + {saldo} WHERE cusuario = {cusuario}")
            self.db.commit()
            return True
        except Exception as ex:
            print("Error adding saldo: ", ex)
            self.db.rollback()
            return False