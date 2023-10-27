import pyodbc


try:
    with open("connection.txt", "r") as f:
        id_user = f.readline().strip()
        password = f.readline().strip()
        database = f.readline().strip()

        connection = pyodbc.connect(
            'Driver={Devart ODBC Driver for Oracle};'
            'Direct=True;'
            'Host=oracle0.ugr.es;'
            'Service Name=practbd.oracle0.ugr.es;'
            f'User ID={id_user};'
            f'Password={password};')

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM mis_sesiones")

        for row in cursor:
            print(row)

        cursor.close()
        connection.close()


except pyodbc.Error as ex:
    print("Error:", ex)