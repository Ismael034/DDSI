import query
import database
import random
import datetime
from tabulate import tabulate
from simple_term_menu import TerminalMenu


def print_tables(q):
    stock = q.get_stock()
    pedido = q.get_pedido()
    detalle_pedido = q.get_detalle_pedido()
                
    print("Tabla Stock:")
    print(tabulate(stock, headers=["Código pedido", "Cantidad"], tablefmt="fancy_grid"))
    print("Tabla Pedido:")
    print(tabulate(pedido, headers=["Código pedido", "Código cliente", "Fecha pedido"], tablefmt="fancy_grid"))
    print("Tabla Detalle Pedido:")
    print(tabulate(detalle_pedido, headers=["Código pedido", "Código producto", "Cantidad"], tablefmt="fancy_grid"))
    print()

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
            tables_deleted = True
            get_tables = q.get_tables()
            for table in get_tables:
                if not q.delete_table(table[0]):
                    tables_deleted = False
                    break

            if q.create_tables() and tables_deleted:
                for i in range(10):
                    if not q.insert_stock(i, random.randint(1, 100)):
                        break

                db.commit()
            show_menu = True
            
        elif menu_entry_index == 1:
            opciones_pedido = ["Añadir detalle de producto", 
                "Eliminar todos los detalles de pedido", 
                "Cancelar pedido",
                "Finalizar pedido"
            ]
            while True:
                try:
                    cpedido = int(input("Introduzca el código del pedido: "))
                    ccliente = int(input("Introduzca el código del cliente: "))
                    break
                except ValueError:
                    print("Error: Introduzca un número entero")

            q.insert_pedido(cpedido, ccliente, datetime.datetime.now().date())

            pedido_savepoint = "pedido_insertado"
            db.savepoint(pedido_savepoint)

            show_sub_menu = True
            menu_pedido = TerminalMenu(opciones_pedido)
            while True:
                if show_sub_menu:
                    menu_pedido_index = menu_pedido.show()
                    show_sub_menu = False

                if menu_pedido_index == 0:
                    try:
                        cantidad = int(input("Introduzca la cantidad: "))
                        cproducto = int(input("Introduzca el código del producto: "))
                    except ValueError:
                        print("Error: Introduzca un número entero")
                        print()
                        show_sub_menu = True
                        continue
                    

                    cantidad_stock = q.get_cantidad_stock(cproducto)

                    try:
                        stock_resultante = cantidad_stock[0] - cantidad
                    except TypeError:
                        print("Error: No existe el producto")
                        print()
                    
                    if stock_resultante < 0:
                        print("Error: No hay suficiente stock")
                        print()
                    else:
                        q.insert_detalle_pedido(cpedido, cproducto, cantidad, pedido_savepoint)
                        q.update_stock(cproducto, stock_resultante, pedido_savepoint)

                    show_sub_menu = True
                    print_tables(q)
                elif menu_pedido_index == 1:
                    print("Eliminando detalles de pedido...")
                    q.delete_detalle_pedido(cpedido)
                    print_tables(q)
                    show_sub_menu = True

                elif menu_pedido_index == 2:
                    db.rollback()
                    print("Pedido cancelado")
                    print_tables(q)
                    break
                
                elif menu_pedido_index == 3:
                    db.commit()
                    print("Pedido finalizado")
                    break
                
            show_menu = True

        elif menu_entry_index == 2:
            print_tables(q)
            show_menu = True
        
        elif menu_entry_index == 3:
            db.close()
            exit()
    

if __name__ == "__main__":
    main()