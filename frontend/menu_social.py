from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import requests
from simple_term_menu import TerminalMenu

import global_var as gv

console = Console()

def crear_usuario():
    console.print("Crear usuario", style="bold magenta")
    nombre_usuario = Prompt.ask("Ingresa el nombre de usuario")
    password = Prompt.ask("Ingresa la contraseña")
    nombre = Prompt.ask("Ingresa el nombre")
    email = Prompt.ask("Ingresa el email")


    response = requests.post('http://localhost:5000/user/', json={'nombre_usuario': nombre_usuario, 'password': password, 'nombre': nombre, 'email': email})
    
    if response.status_code == 200:
        console.print("Usuario creado exitosamente", style="green")
        gv.set_nombre_usuario(nombre_usuario)
        mostrar_perfil()
        return True
    else:
        console.print(f"Error al crear usuario", style="bold red")
        return False

def iniciar_sesion():
    console.print("Iniciar sesión", style="bold magenta")
    nombre_usuario = Prompt.ask("Ingresa el nombre de usuario")
    password = Prompt.ask("Ingresa la contraseña")

    response = requests.post('http://localhost:5000/user/login', json={'nombre_usuario': nombre_usuario, 'password': password})
    if response.status_code == 200:
        console.print("Sesión iniciada exitosamente", style="green")
        gv.set_nombre_usuario(nombre_usuario)
        mostrar_perfil()
        return True
    else:
        console.print(f"Error al iniciar sesión", style="bold red")

def mostrar_perfil():
    response = requests.get('http://localhost:5000/user/{}'.format(gv.nombre_usuario))
    if response.status_code == 200:
        table = Table(title="Perfil")
        table.add_column("Nombre de usuario")
        table.add_column("Foto de perfil")
        table.add_column("Biografia")
        table.add_column("Logros")
        table.add_row(response.json()[0], response.json()[1], response.json()[2], response.json()[3])
        console.print(table)
    else:
        console.print(f"Error al mostrar perfil: {response.text}", style="bold red")

def modificar_perfil():
    console.print("Modificar perfil", style="bold magenta")
    foto = Prompt.ask("Ingresa la foto de perfil")
    biografia = Prompt.ask("Ingresa la biografia")
    logros = Prompt.ask("Ingresa los logros")

    response = requests.post('http://localhost:5000/user/{}/update'.format(gv.nombre_usuario), json={'fotografia': foto, 'biografia': biografia, 'logros': logros})

    if response.status_code == 200:
        console.print("Perfil modificado exitosamente", style="green")
        mostrar_perfil()
    else:
        console.print(f"Error al modificar perfil", style="bold red")

def eliminar_usuario():
    response = requests.post('http://localhost:5000/user/{}/delete'.format(gv.nombre_usuario))
    if response.status_code == 200:
        console.print("Usuario eliminado exitosamente", style="green")
        cerrar_sesion()
    else:
        console.print(f"Error al eliminar usuario", style="bold red")

def get_amigos():
    response = requests.get('http://localhost:5000/user/{}/amigos'.format(gv.nombre_usuario))
    if response.status_code == 200:
        if response.json() is None:
            console.print("No tienes amigos :(", style="bold red")
        else:
            table = Table(title="Amigos")
            table.add_column("Nombre de usuario")
            table.add_column("Foto de perfil")
            table.add_column("Biografia")
            table.add_column("Logros")
            for amigo in response.json():
                table.add_row(amigo[0], amigo[1], amigo[2], amigo[3])
            console.print(table)
    else:
        console.print(f"Error al mostrar amigos", style="bold red")

def amigos():
    while True:
        options = [
        "Mostrar amigos",
        "Agregar amigo",
        "Eliminar amigo",
        "Volver al menú anterior",
        ]
        
        menu_cursor_style = ("fg_green", "bold")
        menu_highlight_style = ("bg_black", "fg_green")
        terminal_menu = TerminalMenu(options, menu_cursor_style = menu_cursor_style, menu_highlight_style = menu_highlight_style)
        opcion_amigos = terminal_menu.show() 
    
        
        if opcion_amigos == 0:
            get_amigos()
            pass
        elif opcion_amigos == 1:
            amigo = Prompt.ask("Ingresa el nombre del amigo")
            response = requests.post('http://localhost:5000/user/{}/amigos/add'.format(gv.nombre_usuario), json={'amigo': amigo})
            if response.status_code == 200:
                console.print("Amigo agregado exitosamente", style="green")
                get_amigos()
            else:
                console.print(f"Error al agregar amigo", style="bold red")
            pass
        elif opcion_amigos == 2:
            amigo = Prompt.ask("Ingresa el nombre del amigo")
            response = requests.post('http://localhost:5000/user/{}/amigos/delete'.format(gv.nombre_usuario), json={'amigo': amigo})
            if response.status_code == 200:
                console.print("Amigo eliminado exitosamente", style="green")
                get_amigos()
            else:
                console.print(f"Error al eliminar amigo", style="bold red")
            pass
        elif opcion_amigos == 3:
            break
        else:
            console.print("Opción no valida", style="bold red")

### Menu ###
def show_menu_social():
    while True:
      
        options = [
        "Mostrar perfil",
        "Modificar perfil",
        "Eliminar usuario",
        "Amigos",
        "Volver al menú principal",
        ]
        
        menu_cursor_style = ("fg_green", "bold")
        menu_highlight_style = ("bg_black", "fg_green")
        terminal_menu = TerminalMenu(options, menu_cursor_style = menu_cursor_style, menu_highlight_style = menu_highlight_style)
        opcion_social = terminal_menu.show() 
    
        
        if opcion_social == 0:
            mostrar_perfil()
            pass
        elif opcion_social == 1:
            modificar_perfil()
            pass
        elif opcion_social == 2:
            eliminar_usuario()
            pass
        elif opcion_social == 3:
            amigos()
            pass
        elif opcion_social == 4:
            break
        else:
            console.print("Opción no valida", style="bold red")

def show_menu_social_not_logged():
    while True:
      
        options = [
        "Crear usuario",
        "Iniciar sesión",
        "Volver al menú principal",
        ]
        
        menu_cursor_style = ("fg_green", "bold")
        menu_highlight_style = ("bg_black", "fg_green")
        terminal_menu = TerminalMenu(options, menu_cursor_style = menu_cursor_style, menu_highlight_style = menu_highlight_style)
        opcion_social = terminal_menu.show() 
    
        
        if opcion_social == 0:
            if crear_usuario():
                show_menu_social()
                break
            pass
        elif opcion_social == 1:
            if iniciar_sesion():
                show_menu_social()
                break
            pass
        elif opcion_social == 2:
            break
        else:
            console.print("Opción no valida", style="bold red")