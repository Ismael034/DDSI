from rich.console import Console
from rich.prompt import Prompt
import requests
import menu_tienda as tienda
import menu_biblioteca as biblioteca
import menu_social as social
import menu_dev as dev
from simple_term_menu import TerminalMenu

import global_var as gv

console = Console()

### Peticiones ###

### Menu ###
def main():
    gv.show_logo()
    console.print("usuario: {}".format(gv.nombre_usuario), style="bold magenta")
    while True:
        options = [
        "Tienda",
        "Biblioteca",
        "Social",
        "Dev",
        "Salir",
        ]
        
        menu_cursor_style = ("fg_green", "bold")
        menu_highlight_style = ("bg_black", "fg_green")
        terminal_menu = TerminalMenu(options, menu_cursor_style = menu_cursor_style, menu_highlight_style = menu_highlight_style)
        opcion = terminal_menu.show()
        
        
        
        if opcion == 0:
            tienda.show_menu_tienda()
        elif opcion == 1:
            biblioteca.show_menu_biblioteca()
        elif opcion == 2:
            social.show_menu_social()
        elif opcion == 3:
            dev.show_menu_dev()
        elif opcion == 4:
            break
        

if __name__ == "__main__":
    main()