from rich.console import Console
from rich.prompt import Prompt
import requests
from simple_term_menu import TerminalMenu
from rich.table import Table
import json


import global_var as gv

console = Console()

### Menu ###
def show_menu_biblioteca():
    while True:
        options = [
        "Consultar articulo obtenido",
        "Mostrar articulos obtenidos",
        "Valorar artículo",
        "Salir",
        ]
        
        
        menu_cursor_style = ("fg_green", "bold")
        menu_highlight_style = ("bg_black", "fg_green")
        terminal_menu = TerminalMenu(options, menu_cursor_style = menu_cursor_style, menu_highlight_style = menu_highlight_style)
        opcion_biblioteca = terminal_menu.show() 
        

        if opcion_biblioteca == 0:

            titulo = Prompt.ask("Nombre del artículo")

            response = requests.get('http://127.0.0.1:5000/articulo_obtenido/{}/1/{}'.format(gv.nombre_usuario,titulo))
            data = response.json()
            table = Table(title="Artículo")
            table.add_column("Titulo")
            table.add_column("Ultima vez jugado")
            table.add_column("ESTADISTICAS")
            for row in data:
                table.add_row(row[0],row[1],row[2])
            
            if response.status_code == 200:
                console.print(table)
            else:
                console.print(f"Error al consultar artículo: {response.text}", style="bold red")
            while True:
                opt = ["Ejecutar","Atrás"]
                menu = TerminalMenu(opt)
                eje = menu.show()
                if eje == 0:
                    response = requests.post('http://127.0.0.1:5000/articulo_obtenido/{}/{}/exe'.format(gv.nombre_usuario,titulo), json={'nombre_usuario': gv.nombre_usuario, 'titulo': titulo})
                    response = requests.get('http://127.0.0.1:5000/articulo_obtenido/{}/1/{}'.format(gv.nombre_usuario,titulo))
                    data = response.json()
                    table = Table(title="Artículo")
                    table.add_column("Titulo")
                    table.add_column("Ultima vez jugado")
                    table.add_column("ESTADISTICAS")
                    for row in data:
                        table.add_row(row[0],row[1],row[2])

                    if response.status_code == 200:
                        console.print(table)
                    else:
                        console.print(f"Error al consultar artículo: {response.text}", style="bold red")
                elif eje >= 1:
                    break
            pass
        elif opcion_biblioteca == 1:

            n = Prompt.ask("Número de artículos a mostrar")
            response = requests.get('http://127.0.0.1:5000/articulo_obtenido/{}/{}'.format(gv.nombre_usuario,n))
            data = response.json()
            table = Table(title="Artículos")
            table.add_column("Titulo")
            table.add_column("Ultima vez jugado")
            for row in data:
                table.add_row(row[0],row[1])

            console.print(table)
            pass
        elif opcion_biblioteca == 2:
            console.print("Elige el artículo a valorar:\n")

            n = 9999
            response = requests.get('http://127.0.0.1:5000/articulo_obtenido/{}/{}'.format(gv.nombre_usuario,n))
            data = response.json()
            articulos = []
            for row in data:
                tit = row[0]
                articulos.append(tit)
            eleccion_titulo = TerminalMenu(articulos)
            titulo_elegido = articulos[eleccion_titulo.show()]
            while True:
                p = Prompt.ask("Qué puntuación del 1 al 5 le das ")
                if int(p) > 0 and int(p) <= 5:
                    break
            
            com = Prompt.ask("Añade un comentario adicional [opcional]")
            response = requests.post('http://127.0.0.1:5000/valoracion/',json={'titulo':titulo_elegido,'nombre_usuario':gv.nombre_usuario,'puntuacion':int(p),'comentario':com})
            
            console.print(f"Articulo: {titulo_elegido}\n - Puntuacion: {p}\n - Comentario: {com}\n")

            if response.status_code == 200:
                console.print("Valoración enviada :D")
            else:
                console.print(f"Ha habido un error al valorar por parte de {gv.nombre_usuario}")
                console.print(response.json())
            pass
        elif opcion_biblioteca == 3:
            break
        else:
            console.print("Opción no valida", style="bold red")