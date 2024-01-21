from rich.console import Console
from rich.prompt import Prompt
import requests
from simple_term_menu import TerminalMenu

import global_var as gv

console = Console()

### Menu ###
def show_menu_biblioteca():
    while True:
        options = [
        "Consultar articulo",
        "Mostrar articulos obtenidos",
        "Consultar articulo obtenido",
        "Activar modificacion",
        "Salir",
        ]
        
        
        menu_cursor_style = ("fg_green", "bold")
        menu_highlight_style = ("bg_black", "fg_green")
        terminal_menu = TerminalMenu(options, menu_cursor_style = menu_cursor_style, menu_highlight_style = menu_highlight_style)
        opcion_biblioteca = terminal_menu.show() 
        
        if opcion_biblioteca == 0:
            pass
        elif opcion_biblioteca == 1:
            pass
        elif opcion_biblioteca == 2:
            pass
        elif opcion_biblioteca == 3:
            pass
        elif opcion_biblioteca == 4:
            break
        else:
            console.print("Opción no valida", style="bold red")