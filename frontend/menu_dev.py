from rich.console import Console
from rich.prompt import Prompt
import requests
from simple_term_menu import TerminalMenu

import global_var as gv
from rich.table import Table

console = Console()

### Subir creacion ###
def subir_creacion():
    console.print("Subir Creación", style="bold magenta")
    titulo_creacion = Prompt.ask("Introduzca el titulo de la creación")
    tipo = Prompt.ask("Introduzca el tipo de la creación")
    fecha_subida = Prompt.ask("Introduzca la fecha")
    descripcion_corta = Prompt.ask("Introduzca la descripcion corta de la creación")
    descripcion_larga = Prompt.ask("Introduzca la descripcion larga de la creación")
    genero = Prompt.ask("Introduzca el genero de la creación")
    icono = Prompt.ask("Introduzca el icono de la creación")
    tamaño = Prompt.ask("Introduzca el tamaño de la creación")
    ruta_ejecutable = Prompt.ask("Introduzca la ruta del ejecutable de la creación")
    especificaciones = Prompt.ask("Introduzca las especificaciones de la creación")
    
    
    response = requests.post('http://127.0.0.1:5000/creacion', json={'titulo_creacion': titulo_creacion, 'tipo': tipo, 'nombre_usuario': gv.nombre_usuario, 'fecha_subida': fecha_subida, 'descripcion_corta': descripcion_corta, 'descripcion_larga': descripcion_larga, 'genero': genero, 'icono': icono, 'tamano': tamaño, 'ruta_ejecutable': ruta_ejecutable, 'especificaciones': especificaciones})
    
    if response.status_code == 200:
        console.print("Creación subida exitosamente", style="green")
    else:
        console.print(f"Error al subir creación: {response.text}", style="bold red")

### Borrar creacion ###
def borrar_creacion():
    console.print("Eliminar Creación", style="bold magenta")
    titulo_creacion = Prompt.ask("Introduzca el titulo de la creación")
    
    response = requests.post('http://127.0.0.1:5000/creacion/delete', json={'titulo_creacion': titulo_creacion, 'nombre_usuario': gv.nombre_usuario})
    
    if response.status_code == 200:
        console.print("Creación borrada exitosamente", style="green")
    else:
        console.print(f"Error al borrar creación: {response.text}", style="bold red")

### Consultar creacion por nombre ###
def consultar_creacion():
    console.print("Consular creación por nombre", style="bold magenta")
    titulo_creacion = Prompt.ask("Introduzca el nombre de la creacion")
    
    response = requests.get('http://127.0.0.1:5000/creacion/{}'.format(titulo_creacion))
    
    table = Table(title="Creación solicitada")
    table.add_column("Titulo Creación")
    table.add_column("Tipo")
    table.add_column("Creador")
    table.add_column("Numero Descargas")
    table.add_column("Fecha Subida")
    table.add_column("Activada (Mod)")

    data = response.json()
    for row in data:
        table.add_row(row[0], row[1], row[2], str(row[3]), str(row[4]), str(row[5]))
    
    if response.status_code == 200:
        console.print(table)
    else:
        console.print(f"Error al consultar la creación: {response.text}", style="bold red")
        
### Listar creaciones por tipo ###
def listar_creaciones_por_tipo():
    console.print("Listar creaciones por tipo", style="bold magenta")
    tipo = Prompt.ask("Introduzca el tipo de creacion a listar")
    
    response = requests.get('http://127.0.0.1:5000/creacion/tipo/{}'.format(tipo))
    
    if response.status_code == 200:
        console.print(response.json())
    else:
        console.print(f"Error al listar las creaciones: {response.text}", style="bold red")


### Activar mod ###
def activar_mod():
    console.print("Activación de Modificación", style="bold magenta")
    titulo_creacion = Prompt.ask("Introduzca el titulo de la modificación")
    
    response = requests.post('http://127.0.0.1:5000/creacion/{}/activar'.format(titulo_creacion))
    
    if response.status_code == 200:
        console.print("Modificación activada exitosamente", style="green")
    else:
        console.print(f"Error al activar la modificación: {response.text}", style="bold red")


### Menu ###
def show_menu_dev():
    while True:
        options = [
        "Consultar creación",
        "Listar creaciones",
        "Subir creación",
        "Borrar creación",
        "Activar modificación",
        "Salir",
        ]
        
        menu_cursor_style = ("fg_green", "bold")
        menu_highlight_style = ("bg_black", "fg_green") 
        terminal_menu = TerminalMenu(options, menu_cursor_style = menu_cursor_style, menu_highlight_style = menu_highlight_style)
        opcion_dev = terminal_menu.show() 
        
        if opcion_dev == 0:
            consultar_creacion()
        elif opcion_dev == 1:
            listar_creaciones_por_tipo()
        elif opcion_dev == 2:
            subir_creacion()
        elif opcion_dev == 3:
            borrar_creacion()
        elif opcion_dev == 4:
            activar_mod()    
        elif opcion_dev == 5:
            break      
        else:
            console.print("Opción no valida", style="bold red")
