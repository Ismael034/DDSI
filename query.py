class query:
    def __init__(self, database):
        self.db = database
        self.db.connect()
        

    def get_tables(self):
        try:
            self.db.execute("SELECT table_name FROM user_tables")
            return self.db.fetchall()
        except Exception as ex:
            print("Error getting tables: ", ex)

    def delete_tables(self):
        try:
            self.db.execute("DROP TABLE Stock")
            self.db.execute("DROP TABLE Pedido")
            self.db.execute("DROP TABLE Detalle_Pedido")
            self.db.commit()
        
        except Exception as ex:
            print("Error deleting table: ", ex)
            self.db.rollback()

    def delete_table(self, name):
        try:
            self.db.execute(f"DROP TABLE {name}")
        
        except Exception as ex:
            print("Error deleting table: ", ex)

    def create_table_stock(self):
        try:
            self.db.execute("CREATE TABLE Stock ("
                            "Cproducto INTEGER PRIMARY KEY,"
                            "Cantidad INTEGER)")

            self.db.commit()
        
        except Exception as ex:
            print("Error creating stock table: ", ex)

    def create_table_pedido(self):
        try:
            self.db.execute("CREATE TABLE Pedido ("
                            "Cpedido INTEGER PRIMARY KEY,"
                            "Ccliente INTEGER,"
                            "Fecha_pedido DATE)")
        
        except Exception as ex:
            print("Error creating pedido table:", ex)

    def create_table_detalle_pedido(self):
        try:
            self.db.execute("CREATE TABLE Detalle_Pedido ("
                            "Cpedido INTEGER REFERENCES Pedido(Cpedido),"
                            "Cproducto INTEGER REFERENCES Stock(Cproducto),"
                            "Cantidad INTEGER,"
                            "CONSTRAINT clave_primaria PRIMARY KEY (Cpedido,Cproducto))")
        
        except Exception as ex:
            print("Error creating detalle table: ", ex)


    def create_tables(self):
        try:
            self.create_table_stock()
            self.create_table_pedido()
            self.create_table_detalle_pedido()
            self.db.commit()
        except Exception as ex:
            print("Error creating tables: ", ex)
            self.db.rollback()

    def insert_stock(self, cproducto, cantidad):
        try:
            self.db.execute(f"INSERT INTO Stock VALUES ({cproducto}, {cantidad})")
            self.db.commit()
        except Exception as ex:
            print("Error inserting stock: ", ex)
            self.db.rollback()

    def insert_pedido(self, cpedido, ccliente, fecha_pedido):
        try:
            self.db.execute(f"INSERT INTO Pedido VALUES ({cpedido}, {ccliente}, TO_DATE('{fecha_pedido}', 'YYYY-MM-DD'))")
            self.db.commit()
        except Exception as ex:
            print("Error inserting pedido: ", ex)
            self.db.rollback()

    def get_stock(self):
        try:
            self.db.execute("SELECT * FROM Stock")
            return self.db.fetchall()
        except Exception as ex:
            print("Error getting stock: ", ex)

    def get_pedido(self):
        try:
            self.db.execute("SELECT * FROM Pedido")
            return self.db.fetchall()
        except Exception as ex:
            print("Error getting pedido: ", ex)

    def get_detalle_pedido(self):
        try:
            self.db.execute("SELECT * FROM Detalle_Pedido")
            return self.db.fetchall()
        except Exception as ex:
            print("Error getting detalle: ", ex)

    