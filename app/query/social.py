class social:
    def __init__(self, database):
        self.db = database
        self.db.connect()
        self.db.rollback()     

    def get_tables(self):
        try:
            self.db.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = DATABASE()")
            return self.db.fetchall()
        except Exception as ex:
            print("Error getting tables: ", ex)

    def delete_tables(self):
        try:
            self.db.execute("DROP TABLE Usuario")
            self.db.execute("DROP TABLE Perfil")
            self.db.execute("DROP TABLE Articulo")
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

    def create_table_perfil(self):
        try:
            self.db.execute("CREATE TABLE Perfil ("
                            "#Nombre_Usuario VARCHAR(20) PRIMARY KEY,"
                            "Email VARCHAR(20),"
                            "Fotografía BLOB,"
                            "Biografía VARCHAR(300),"
                            "Logros VARCHAR(300),"
                            "Artículos_adquiridos VARCHAR(20)")
        
        except Exception as ex:
            print("Error creating stock perfil: ", ex)
            self.db.rollback()


 UsuarioRegistrado-AñadirSaldo(#Nombre_Usuario, Saldo, Nombre, Contraseña, Artículos_adquiridos)
 
    def create_table_usuario(self):
        try:
            self.db.execute("CREATE TABLE Usuario ("
                            "#Nombre_Usuario VARCHAR(20) PRIMARY KEY,"
                            "Saldo INTEGER,"
                            "Fecha_pedido DATE)")
        
        except Exception as ex:
            print("Error creating usuario table:", ex)

    def create_table_articulo(self):
        try:
            self.db.execute("CREATE TABLE Articulo ("
                            "Cpedido INTEGER,"
                            "Cproducto INTEGER,"
                            "Cantidad INTEGER CHECK (Cantidad > 0),"
                            "PRIMARY KEY (Cpedido, Cproducto),"
                            "FOREIGN KEY (Cpedido) REFERENCES Pedido(Cpedido),"
                            "FOREIGN KEY (Cproducto) REFERENCES Stock(Cproducto))")
        except Exception as ex:
            print("Error creating articulo table: ", ex)


    def create_tables(self):
        try:
            self.create_table_perfil()
            self.create_table_usuario()
            self.create_table_articulo()
            self.db.commit()
            return True
        except Exception as ex:
            print("Error creating tables: ", ex)
            self.db.rollback()
            return False





    def insert_stock(self, cantidad):
        try:
            self.db.execute(f"INSERT INTO Stock(Cantidad) VALUES ({cantidad})")
            self.db.commit()
            return True
        except Exception as ex:
            print("Error inserting stock: ", ex)
            self.db.rollback()
            return False

    def get_stock(self):
        try:
            self.db.execute("SELECT * FROM Stock")
            return self.db.fetchall()
        except Exception as ex:
            print("Error getting stock: ", ex)

    def get_stock_by_id(self, cproducto):
        try:
            self.db.execute(f"SELECT * FROM Stock WHERE cproducto = {cproducto}")
            return self.db.fetchone()
        except Exception as ex:
            print("Error getting stock: ", ex)

    def update_stock(self, cproducto, cantidad):
        try:
            self.db.execute(f"UPDATE Stock SET cantidad = {cantidad} WHERE cproducto = {cproducto}")
            self.db.commit()
        except Exception as ex:
            print("Error updating stock: ", ex)
            self.db.rollback()

    def delete_stock(self, cproducto):
        try:
            self.db.execute(f"DELETE FROM Stock WHERE cproducto = {cproducto}")
            self.db.commit()
        except Exception as ex:
            print("Error deleting stock: ", ex)
            self.db.rollback()

    def get_cantidad_stock(self, cproducto):
        try:
            self.db.execute(f"SELECT cantidad FROM Stock WHERE cproducto = {cproducto}")
            return self.db.fetchone()
        except Exception as ex:
            print("Error getting cantidad stock: ", ex)





    def get_pedido(self):
        try:
            self.db.execute("SELECT * FROM Pedido")
            return self.db.fetchall()
        except Exception as ex:
            print("Error getting pedido: ", ex)

    def get_pedido_by_id(self, cpedido):
        try:
            self.db.execute(f"SELECT * FROM Pedido WHERE cpedido = {cpedido}")
            return self.db.fetchone()
        except Exception as ex:
            print("Error getting pedido: ", ex)

    def insert_pedido(self, ccliente, fecha_pedido):
        try:
            self.db.execute(f"INSERT INTO Pedido(Ccliente, Fecha_pedido) VALUES ({ccliente}, STR_TO_DATE('{fecha_pedido}', '%Y-%m-%d'))")
            self.db.commit()
            
        except Exception as ex:
            print("Error inserting pedido: ", ex)
            self.db.rollback()

    def delete_pedido(self, cpedido):
        try:
            self.db.execute(f"DELETE FROM Pedido WHERE cpedido = {cpedido}")
            self.db.commit()
        except Exception as ex:
            print("Error deleting pedido: ", ex)
            self.db.rollback()


    def update_pedido(self, cpedido, ccliente, fecha_pedido):
        try:
            self.db.execute(f"UPDATE Pedido SET ccliente = {ccliente}, fecha_pedido = STR_TO_DATE('{fecha_pedido}', '%Y-%m-%d') WHERE cpedido = {cpedido}")
            self.db.commit()
        except Exception as ex:
            print("Error updating pedido: ", ex)
            self.db.rollback()



    def get_detalle_pedido(self):
        try:
            self.db.execute("SELECT * FROM Detalle_Pedido")
            return self.db.fetchall()
        except Exception as ex:
            print("Error getting detalle: ", ex)

    def get_detalle_pedido_by_id(self, cpedido, cproducto):
        try:
            self.db.execute(f"SELECT * FROM Detalle_Pedido WHERE cpedido = {cpedido} AND cproducto = {cproducto}")
            return self.db.fetchone()
        except Exception as ex:
            print("Error getting detalle: ", ex)
            
    def delete_detalle_pedido(self, cpedido, cproducto):
        try:
            self.db.execute(f"DELETE FROM Detalle_Pedido WHERE cpedido = {cpedido} AND cproducto = {cproducto}")
            self.db.commit()
        except Exception as ex:
            print("Error deleting detalle pedido: ", ex)
            self.db.rollback()

    def insert_detalle_pedido(self, cpedido, cproducto, cantidad):
        try:
            self.db.execute(f"INSERT INTO Detalle_Pedido VALUES ({cpedido}, {cproducto}, {cantidad})")
            self.db.commit()
        except Exception as ex:
            print("Error inserting detalle pedido: ", ex)
            self.db.rollback()

     
