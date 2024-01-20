from app.database import database
from app.query.query import query
import logging

class helpers:
    @staticmethod
    def check_init_tables():
        db = database()
        q = query(db)
        try:
            #q.delete_tables()
            tables = q.get_tables()
            if len(tables) == 0:
                logging.error("No tables found, creating tables...")
                q.create_tables()
                logging.error("Tables created.")
                db.commit()
        except Exception as ex:
            print("Error checking tables: ", ex)