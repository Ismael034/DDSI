from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import requests
from simple_term_menu import TerminalMenu

import global_var as gv

console = Console()

### Publicar videojuego ###
def publicar_videojuego():
    console.print("Publicar videojuego", style="bold magenta")
    titulo_videojuego = Prompt.ask("Ingresa el titulo del videojuego")
    precio = Prompt.ask("Ingresa el precio del videojuego")
    version = Prompt.ask("Ingresa la version del videojuego")
    descripcion_corta = Prompt.ask("Ingresa la descripcion corta del videojuego")
    descripcion_larga = Prompt.ask("Ingresa la descripcion larga del videojuego")
    genero = Prompt.ask("Ingresa el genero del videojuego")
    icono = Prompt.ask("Ingresa el icono del videojuego")
    tamaño = Prompt.ask("Ingresa el tamaño del videojuego")
    ruta_ejecutable = Prompt.ask("Ingresa la ruta del ejecutable del videojuego")
    especificaciones = Prompt.ask("Ingresa las especificaciones del videojuego")
    
    response = requests.post('http://127.0.0.1:5000/tienda/', json={'titulo_videojuego': titulo_videojuego, 'precio': precio, 'version': version, 'nombre_usuario': gv.nombre_usuario, 'descripcion_corta': descripcion_corta, 'descripcion_larga': descripcion_larga, 'genero': genero, 'icono': icono, 'tamaño': tamaño, 'ruta_ejecutable': ruta_ejecutable, 'especificaciones': especificaciones})
    
    if response.status_code == 200 and response.json()[1] != False:
        console.print("Videojuego creado exitosamente", style="green")
    else:
        console.print(f"Error al publicar videojuego: {response.json()[0]}", style="bold red")
        

### Eliminar videojuego ###
def eliminar_videojuego():
    console.print("Eliminar videojuego", style="bold magenta")
    cvideojuego = Prompt.ask("Ingresa el titulo del videojuego")
    
    response = requests.delete('http://127.0.0.1:5000/tienda/{}'.format(cvideojuego))
    
    if response.status_code == 200 and response.json()[1] != False:
        console.print("Videojuego borrado exitosamente", style="green")
    else:
        console.print(f"Error al borrar videojuego: {response.json()[0]}", style="bold red")
        
        
### Actualizar version de un videojuego ###
def actualizar_version_videojuego():
    console.print("Actualizar version de un videojuego", style="bold magenta")
    cvideojuego = Prompt.ask("Ingresa el titulo del videojuego")
    version = Prompt.ask("Ingresa la version del videojuego")
    
    response = requests.post('http://127.0.0.1:5000/tienda/update-version/{}'.format(cvideojuego), json={'version': version})
    
    if response.status_code == 200 and response.json()[1] != False:
        console.print("Version de juego actualizado", style="green")
    else:
        console.print(f"Error al borrar videojuego: {response.json()[0]}", style="bold red")
        
### Mostrar videojuegos por genero ###
def mostrar_videojuegos_por_genero():
    console.print("Mostrar videojuegos por genero", style="bold magenta")
    genero = Prompt.ask("Ingresa el genero del videojuego")
    
    response = requests.get('http://127.0.0.1:5000/tienda/{}'.format(genero))

    table = Table(title="Videojuegos por genero")
    table.add_column("Titulo")
    table.add_column("Creador")
    table.add_column("Genero")
    table.add_column("Precio")
    table.add_column("Version")
    table.add_column("Tamaño")
    table.add_column("Descripcion Corta")
    table.add_column("Descripcion Larga")
    table.add_column("Icono")
    table.add_column("Especificaciones")
    data = response.json()
    for row in data:
        table.add_row(row[0], row[1], row[2], str(row[3]), row[4], row[5], row[6], row[7], row[8], row[9])
    
    if response.status_code == 200:
        console.print(table)
    else:
        console.print(f"Error al mostrar videojuegos: {response.text}", style="bold red")
        
def comprar_videojuego():
    console.print("Comprar videojuego", style="bold magenta")
    cvideojuego = Prompt.ask("Ingresa el titulo del videojuego")
    
    response = requests.post('http://127.0.0.1:5000/tienda/comprar/{}'.format(cvideojuego), json={'nombre_usuario': gv.nombre_usuario})
    
    if response.status_code == 200:
        console.print('Saldo total: ' + str(response.json()))
    else:
        console.print(f"Error al comprar videojuego: {response.text}", style="bold red")
        
def add_saldo():
    console.print("Añadir saldo a tu cuenta", style="bold magenta")
    saldo = Prompt.ask("Ingresa el saldo a añadir")
    
    response = requests.post('http://127.0.0.1:5000/tienda/add-saldo/{}'.format(gv.nombre_usuario), json={'saldo': saldo})
    
    if response.status_code == 200:
        console.print('Saldo total: ' + str(response.json()))
    else:
        console.print(f"Error al comprar videojuego: {response.text}", style="bold red")
    
  
  
### Menu ###
def show_menu_tienda():
    while True:
        options = [
        "Publicar videojuego",
        "Eliminar videojuego",
        "Actualizar version de un videojuego",
        "Mostrar videojuegos por genero",
        "Comprar videojuegos",
        "Añadir saldo a tu cuenta",
        "Volver al Menú Principal",
        ]
        
        menu_cursor_style = ("fg_green", "bold")
        menu_highlight_style = ("bg_black", "fg_green")
        
        terminal_menu = TerminalMenu(options, menu_cursor_style = menu_cursor_style, menu_highlight_style = menu_highlight_style)  
        opcion_tienda = terminal_menu.show()
        
        if opcion_tienda == 0:
            # Lógica para Publicar Videojuego
            publicar_videojuego()
        elif opcion_tienda == 1:
            # Lógica para Eliminar Videojuego
            eliminar_videojuego()
            
        elif opcion_tienda == 2:
            # Logica para Actualizar version de un videojuego
            actualizar_version_videojuego()
            
        elif opcion_tienda == 3:
            # Lógica para Mostrar videojuegos por genero
            mostrar_videojuegos_por_genero()
            
        elif opcion_tienda == 4:
            # Lógica para Comprar videojuegos
            comprar_videojuego()
        elif opcion_tienda == 5:
            # Lógica para Añadir saldo a tu cuenta
            add_saldo()
        elif opcion_tienda == 6:
            break
        
        
### Menu ###
def show_menu_tienda_not_logged():
    while True:
        options = [
        "Mostrar videojuegos por genero",
        "Volver al Menú Principal",
        ]
        
        menu_cursor_style = ("fg_green", "bold")
        menu_highlight_style = ("bg_black", "fg_green")
        
        terminal_menu = TerminalMenu(options, menu_cursor_style = menu_cursor_style, menu_highlight_style = menu_highlight_style)  
        opcion_tienda = terminal_menu.show()
        
        if opcion_tienda == 0:
            mostrar_videojuegos_por_genero()
        elif opcion_tienda == 1:
            break