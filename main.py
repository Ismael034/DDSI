import database


def main():
    db = database.database()
    db.connect()

    db.execute("SELECT * FROM PRUEBA1")
    for row in db.fetchall():
        print(row)
    

if __name__ == "__main__":
    main()