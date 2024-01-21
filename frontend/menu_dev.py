from rich.console import Console
from rich.prompt import Prompt
import requests
from simple_term_menu import TerminalMenu

import global_var as gv

console = Console()



### Menu ###
def show_menu_dev():
    while True:
        options = [
        "Consultar creacion",
        "Listar creaciones",
        "Subir creacion",
        "Borrar creacion",
        "Salir",
        ]
        
        menu_cursor_style = ("fg_green", "bold")
        menu_highlight_style = ("bg_black", "fg_green") 
        terminal_menu = TerminalMenu(options, menu_cursor_style = menu_cursor_style, menu_highlight_style = menu_highlight_style)
        opcion_dev = terminal_menu.show() 
        
        if opcion_dev == 0:
            pass
        elif opcion_dev == 1:
            pass
        elif opcion_dev == 2:
            pass
        elif opcion_dev == 3:
            pass
        elif opcion_dev == 4:
            break
        else:
            console.print("Opción no valida", style="bold red")