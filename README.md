![Logo](img/swadit.png)

# Seminario 2 DDSI SWAD Interactive

Participantes:
- Alejandro Escobar Martínez
- Álvaro Ruiz Luzón
- Ismael Melchor Juan
- Luis Martínez Iáñez

### Instalación y ejecución

Para ejecutar el seminario se debe tener python y pip instalado e instalar las bibliotecas de python ejecutando

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


## Uso de la API

Los endpoints de la API serán los siguientes:

- /stock
    - `/`. Obtener todo el stock. GET
    - `/stock/<cproducto>`. Obtener stock dado un id de producto. GET
    - `/stock/`. Insertar nuevo stock. POST
    - `/stock/<cproducto>/update`. Actualizar el stock dado un id. POST
    - `/stock/<cproducto>/delete`. Eliminar stock dado un id. POST

- /pedido
    - `/`. Obtener todo los pedidos. GET
    - `/pedido/<cpedido>`. Obtener pedido dado un id de pedido. GET
    - `/pedido/`. Insertar nuevo pedido. POST
    - `/pedido/<cpedido>/update`. Actualizar el pedido dado un id de pedido. POST
    - `/pedido/<cpedido>/delete`. Eliminar pedido dado un id. POST

- /detalle_pedido
    - `/`. Obtener todo los detalles de pedido. GET
    - `/detalle_pedido/<cpedido>/<cproducto>`. Obtener stock dado un id de producto. GET
    - `/detalle_pedido/`. Insertar nuevo detalle de pedido. POST
    - `/detalle_pedido/update`. Actualizar los detalles de un pedido dado un cproducto y cpedido. POST
    - `/detalle_pedido/delete`. Eliminar los detalles de un pedido dado un cproducto y cpedido. POST