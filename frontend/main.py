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

    if gv.sesion_iniciada:
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
            if gv.sesion_iniciada:
                tienda.show_menu_tienda()
            else:
                tienda.show_menu_tienda_not_logged()
        elif opcion == 1:
            if gv.sesion_iniciada:
                biblioteca.show_menu_biblioteca()
            else:
                console.print("No has iniciado sesión", style="bold red")
        elif opcion == 2:
            if gv.sesion_iniciada:
                social.show_menu_social()
            else:
                social.show_menu_social_not_logged()
        elif opcion == 3:
            if gv.sesion_iniciada:
                dev.show_menu_dev()
            else:
                console.print("No has iniciado sesión", style="bold red")
        elif opcion == 4:
            break
        

if __name__ == "__main__":
    main()
