from app.api.routes.articulo.articulo import articulo
from app.api.routes.tienda.tienda import tienda
from app.api.routes.social.social import social
from app.api.routes.dev.dev import dev

class query:
    def __init__(self, database):
        self.db = database
        self.db.connect()
        self.db.rollback()     

    def create_tables(self):
        try:
            social.create_tables(self.db)
            articulo.create_tables(self.db)
            tienda.create_tables(self.db)
            dev.create_tables(self.db)
        
        except Exception as ex:
            print("Error creating tables: ", ex)
            self.db.rollback()
