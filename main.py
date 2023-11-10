import query
import database
import random
import datetime
from tabulate import tabulate
from simple_term_menu import TerminalMenu

def main():
    options = ["Borrado y nueva creación de las tablas e inserción de 10 tuplas predefinidas en el código en la tabla Stock.", 
                "Dar de alta nuevo pedido", 
                "Mostrar contenido de las tablas de la BD",
                "Salir del programa"]
    terminal_menu = TerminalMenu(options)

    db = database.database()
    q = query.query(db)

    show_menu = True
    while True:
        if show_menu:
            menu_entry_index = terminal_menu.show()
            show_menu = False

        if menu_entry_index == 0:
            get_tables = q.get_tables()
            for table in get_tables:
                q.delete_table(table[0])
            q.create_table_stock()
            q.create_table_pedido()
            q.create_table_detalle_pedido()

            for i in range(10):
                q.insert_stock(i, random.randint(1, 100))
            show_menu = True
            
        elif menu_entry_index == 1:
            opciones_pedido = ["Añadir detalle de producto", 
                "Eliminar todos los detalles de producto", 
                "Cancelar pedido",
                "Finalizar pedido"
            ]
            menu_pedido = TerminalMenu(opciones_pedido)
            ccliente = input("Introduzca el código del cliente: ")
            cproducto = input("Introduzca el código del producto: ")

            q.insert_pedido(ccliente, cproducto, datetime.datetime.now().date())
            show_menu = True

        elif menu_entry_index == 2:
            stock = q.get_stock()
            pedido = q.get_pedido()
            detalle_pedido = q.get_detalle_pedido()
                        
            print("Tabla Stock:")
            print(tabulate(stock, headers=["Código", "Cantidad"], tablefmt="fancy_grid"))
            print("Tabla Pedido:")
            print(tabulate(pedido, headers=["Código", "Código cliente", "Código producto", "Fecha"], tablefmt="fancy_grid"))
            print("Tabla Detalle Pedido:")
            print(tabulate(detalle_pedido, headers=["Código pedido", "Código producto", "Cantidad"], tablefmt="fancy_grid"))
            print()
            show_menu = True
        
        elif menu_entry_index == 3:
            db.close()
            exit()
    

if __name__ == "__main__":
    main()