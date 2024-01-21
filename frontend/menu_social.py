from rich.console import Console
from rich.prompt import Prompt
import requests
from simple_term_menu import TerminalMenu

import global_var as gv

console = Console()

### Menu ###
def show_menu_social():
    while True:
      
        options = [
        "Mostrar perfil",
        "Modificar articulos adquiridos",
        "Modificar perfil",
        "Eliminar usuario",
        "Aceptar amigo",
        "Añadir amigo",
        "Borrar amigo",
        "Salir",
        ]
        
        menu_cursor_style = ("fg_green", "bold")
        menu_highlight_style = ("bg_black", "fg_green")
        terminal_menu = TerminalMenu(options, menu_cursor_style = menu_cursor_style, menu_highlight_style = menu_highlight_style)
        opcion_social = terminal_menu.show() 
    
        
        if opcion_social == 0:
            pass
        elif opcion_social == 1:
            pass
        elif opcion_social == 2:
            pass
        elif opcion_social == 3:
            pass
        elif opcion_social == 4:
            pass
        elif opcion_social == 5:
            pass
        elif opcion_social == 6:
            pass
        elif opcion_social == 7:
            break
        else:
            console.print("Opción no valida", style="bold red")