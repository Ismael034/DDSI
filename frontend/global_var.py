nombre_usuario = 'test'
sesion_iniciada = False
from rich.console import Console
from rich.prompt import Prompt

console = Console()


def set_nombre_usuario(nuevo_nombre):
    global nombre_usuario
    nombre_usuario = nuevo_nombre
    sesion_iniciada = True

def cerrar_sesion():
    global nombre_usuario
    nombre_usuario = ''
    sesion_iniciada = False
    
    
def show_logo():
  logo = """ 
   ▄████████  ▄█     █▄     ▄████████ ████████▄          ▄██████▄     ▄████████   ▄▄▄▄███▄▄▄▄      ▄████████    ▄████████ 
  ███    ███ ███     ███   ███    ███ ███   ▀███        ███    ███   ███    ███ ▄██▀▀▀███▀▀▀██▄   ███    ███   ███    ███ 
  ███    █▀  ███     ███   ███    ███ ███    ███        ███    █▀    ███    ███ ███   ███   ███   ███    █▀    ███    █▀  
  ███        ███     ███   ███    ███ ███    ███       ▄███          ███    ███ ███   ███   ███  ▄███▄▄▄       ███        
▀███████████ ███     ███ ▀███████████ ███    ███      ▀▀███ ████▄  ▀███████████ ███   ███   ███ ▀▀███▀▀▀     ▀███████████ 
         ███ ███     ███   ███    ███ ███    ███        ███    ███   ███    ███ ███   ███   ███   ███    █▄           ███ 
   ▄█    ███ ███ ▄█▄ ███   ███    ███ ███   ▄███        ███    ███   ███    ███ ███   ███   ███   ███    ███    ▄█    ███ 
 ▄████████▀   ▀███▀███▀    ███    █▀  ████████▀         ████████▀    ███    █▀   ▀█   ███   █▀    ██████████  ▄████████▀  
                                                                                                                          
 """
  console.print(logo, style="bold green")
