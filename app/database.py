import mariadb
import json
class database:
    def __init__(self):
        self.id_user = ""
        self.password = ""
        self.host = ""
        self.port = 0
        self.database = ""

        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
                self.id_user = config["database_user"]
                self.password = config["database_password"]
                self.host = config["database_host"]
                self.port = config["database_port"]
                self.database = config["database_db"]

                self.connection = mariadb.connect(
                    user=self.id_user,
                    password=self.password,
                    host=self.host,
                    port=self.port,
                    database=self.database
                )

                self.cursor = self.connection.cursor()

        except mariadb.Error as ex:
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

    def savepoint(self, name):
        self.cursor.execute(f"SAVEPOINT {name}")

    def rollback_to_savepoint(self, name):
        self.cursor.execute(f"ROLLBACK TO {name}")
        
    def close(self):
        self.cursor.close()
        self.connection.close()
