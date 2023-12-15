class helpers:
    @staticmethod
    def check_init_tables(q, db):
        try:
            tables = q.get_tables()
            if len(tables) == 0:
                print("No tables found, creating tables...")
                q.create_tables()
                print("Tables created.")

                for i in range(1, 11):
                    q.insert_stock(100)
                db.commit()
        except Exception as ex:
            print("Error checking tables: ", ex)