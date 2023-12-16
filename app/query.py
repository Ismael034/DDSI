class query:
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
            self.db.execute("DROP TABLE Detalle_Pedido")
            self.db.execute("DROP TABLE Stock")
            self.db.execute("DROP TABLE Pedido")
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

    def create_table_stock(self):
        try:
            self.db.execute("CREATE TABLE Stock ("
                            "Cproducto INTEGER PRIMARY KEY AUTO_INCREMENT,"
                            "Cantidad INTEGER)")
        
        except Exception as ex:
            print("Error creating stock table: ", ex)
            self.db.rollback()

    def create_table_pedido(self):
        try:
            self.db.execute("CREATE TABLE Pedido ("
                            "Cpedido INTEGER PRIMARY KEY AUTO_INCREMENT,"
                            "Ccliente INTEGER,"
                            "Fecha_pedido DATE)")
        
        except Exception as ex:
            print("Error creating pedido table:", ex)

    def create_table_detalle_pedido(self):
        try:
            self.db.execute("CREATE TABLE Detalle_Pedido ("
                            "Cpedido INTEGER,"
                            "Cproducto INTEGER,"
                            "Cantidad INTEGER CHECK (Cantidad > 0),"
                            "PRIMARY KEY (Cpedido, Cproducto),"
                            "FOREIGN KEY (Cpedido) REFERENCES Pedido(Cpedido),"
                            "FOREIGN KEY (Cproducto) REFERENCES Stock(Cproducto))")
        except Exception as ex:
            print("Error creating detalle table: ", ex)


    def create_tables(self):
        try:
            self.create_table_stock()
            self.create_table_pedido()
            self.create_table_detalle_pedido()
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

    def insert_pedido(self, ccliente, fecha_pedido):
        try:
            self.db.execute(f"INSERT INTO Pedido(Ccliente, Fecha_pedido) VALUES ({ccliente}, STR_TO_DATE('{fecha_pedido}', '%Y-%m-%d'))")
        except Exception as ex:
            print("Error inserting pedido: ", ex)
            self.db.rollback()

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
        except Exception as ex:
            print("Error updating stock: ", ex)

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

    def get_detalle_pedido(self):
        try:
            self.db.execute("SELECT * FROM Detalle_Pedido")
            return self.db.fetchall()
        except Exception as ex:
            print("Error getting detalle: ", ex)

    def get_detalle_pedido_by_id(self, cpedido):
        try:
            self.db.execute(f"SELECT * FROM Detalle_Pedido WHERE cpedido = {cpedido}")
            return self.db.fetchall()
        except Exception as ex:
            print("Error getting detalle: ", ex)
            
    def delete_detalle_pedido(self, cpedido):
        try:
            self.db.execute(f"DELETE FROM Detalle_Pedido WHERE cpedido = {cpedido}")
        except Exception as ex:
            print("Error deleting detalle: ", ex)
            self.db.rollback()

    def insert_detalle_pedido(self, cpedido, cproducto, cantidad, savepoint):
        try:
            self.db.execute(f"INSERT INTO Detalle_Pedido VALUES ({cpedido}, {cproducto}, {cantidad})")
        except Exception as ex:
            print("Error inserting detalle pedido: ", ex)
            self.db.rollback_to_savepoint(savepoint)

     