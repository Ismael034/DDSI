# Seminario 1 DDSI SWAD Interactive

Participantes:
- Alejandro Escobar Martínez
- Álvaro Ruiz Luzón
- Ismael Melchor Juan
- Luis Martínez Iáñez

### Instalación y ejecución

Para ejecutar el seminario se debe de instalar previamente el [driver odbc de Devart](https://www.devart.com/odbc/oracle/). Tener python y pip instalado e instalar las bibliotecas de python ejecutando

```
pip3 install -r requirements.txt
sudo apt install libmariadb3 libmariadb-dev
```

Se deberá modificar el fichero `config.json` y el fichero `docker-compose.yml` con los datos para la conexión a la base de datos

Una vez los datos sean correctos, iniciar el contenedor de docker ejecutando

```
sudo docker-compose up -d
```

y ejecutar el programa con

```
python3 swad_it.py
```
