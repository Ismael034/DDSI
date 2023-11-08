import pyodbc

class database:
    def __init__(self):
        self.id_user = ""
        self.password = ""
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            with open("connection.txt", "r") as f:
                self.id_user = f.readline().strip()
                self.password = f.readline().strip()

                self.connection = pyodbc.connect(
                    'Driver={Devart ODBC Driver for Oracle};'
                    'Direct=True;'
                    'Host=oracle0.ugr.es;'
                    'Service Name=practbd.oracle0.ugr.es;'
                    f'User ID={self.id_user};'
                    f'Password={self.password};')

                self.cursor = self.connection.cursor()

        except pyodbc.Error as ex:
            print("Error: ", ex)
            exit()

    def disconnect(self):
        self.cursor.close()
        self.connection.close()

    def execute(self, query):
        self.cursor.execute(query)

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close(self):
        self.cursor.close()
        self.connection.close()
        