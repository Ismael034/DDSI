from app.query.articulo import articulo
from app.query.tienda import tienda
from app.query.social import social
from app.query.dev import dev
import logging

class query:
    def __init__(self, database):
        self.db = database
        self.db.connect()
        self.db.rollback()     

    def create_tables(self):
        try:
            social(self.db).create_tables()
            articulo(self.db).create_tables()
            tienda(self.db).create_tables()
            dev(self.db).create_tables()
        
        except Exception as ex:
            logging.error("Error creating tables: ", ex)
            self.db.rollback()

    def get_tables(self):
        try:
            self.db.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = DATABASE()")
            return self.db.fetchall()
        except Exception as ex:
            print("Error getting tables: ", ex)

    def delete_tables(self):
        try:
            self.db.execute("DROP TABLE IF EXISTS Listar_Creacion")
            self.db.execute("DROP TABLE IF EXISTS Consultar_Creacion")
            self.db.execute("DROP TABLE IF EXISTS Creacion")

            self.db.execute("DROP TABLE IF EXISTS Compra")
            self.db.execute("DROP TABLE IF EXISTS Videojuego")

            self.db.execute("DROP TABLE IF EXISTS Valoracion")
            self.db.execute("DROP TABLE IF EXISTS Articulo_obtenido")
            self.db.execute("DROP TABLE IF EXISTS Articulo")

            self.db.execute("DROP TABLE IF EXISTS Amistad")
            self.db.execute("DROP TABLE IF EXISTS Perfil")
            self.db.execute("DROP TABLE IF EXISTS Usuario")
            
            self.db.execute(f"DROP TRIGGER IF EXISTS actualizar_saldo")
            self.db.execute(f"DROP TRIGGER IF EXISTS crear_perfil")
            self.db.execute(f"DROP TRIGGER IF EXISTS anadir_articulo_usuario")
            
            self.db.commit()
        except Exception as ex:
            logging.error("Error deleting tables: ", ex)
            self.db.rollback()
