![Logo](img/swadit.png)

# Práctica 3 DDSI SWAD Interactive

Participantes:
- Alejandro Escobar Martínez
- Álvaro Ruiz Luzón
- Ismael Melchor Juan
- Luis Martínez Iáñez

### Instalación y ejecución

Para ejecutar la práctica se debe tener python y pip instalado e instalar las bibliotecas de python ejecutando

```
pip3 install -r requirements.txt
```

Será necesario instalar algunas dependencias adicionales y docker

```
sudo apt install libmariadb3 libmariadb-dev docker docker-compose

sudo dnf install libmariadb3 libmariadb-devel docker docker-compose
```

Se deberá modificar el fichero `config.json` y el fichero `docker-compose.yml` con los datos para la conexión a la base de datos

Una vez los datos sean correctos, iniciar el contenedor de docker ejecutando

```
sudo docker-compose up -d

Una vez ejecutado, podremos acceder a la API desde el puerto 5000
```


## Cloudbeaver

Para poder acceder a la base de datos de una manera sencilla, se incluye en el archivo `docker-compose.yml` un gestor de base de datos. Para acceder, ir al navegador a la url [http://127.0.0.1:8080/#/](http://127.0.0.1:8080/#/). Al iniciar la primera conexión con la base de datos, seleccionar `MariaDB` como sistema gestor y introducir los siguientes datos en los campos:

- Host: `mariadb`
- Port: `3306`
- Database: `swad`
- User name: `root`
- Password: `acanas23`
