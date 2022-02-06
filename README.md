# API COMERCIO

La siguiente es una API creada con el fin de simular una plicacion de comercio. El objetivo de esta aplicacion es el ofrecer un servicio en donde clientes puedan registrar sus productos para que los usuarios puedan visualizarlos y comprarlos, ademas todo esto mediado por un actor intermedio el cual se encarga de mantener los servicios y brindar soporte tanto a clientes como usuarios.

Esta aplicacion se encuentra construida bajo el framework Django, utiliza una base de datos relacional PostgreSQL y una base de datos en memoria Redis, todo esto contenido bajo Docker.

## REQUISITOS
* Python 3.10
* Docker
* PostgreSQL
* Redis

## INSTALACIÓN
Para correr el proyecto en local es necesario ubicarse en la carpeta raiz del proyecto y ejecutar el comando
```console
docker-compose up
```
Para poder crear un superusuario se debe ejecutar el siguiente comando en una nueva terminal sobre la carpeta raiz
```console
docker-compose exec commerce-api python3 manage.py createsuperuser
```

## FUNCIONAMIENTO

La aplicacion tiene la siguiente arquitectura a manera general

<p align="center">
  <img src="https://user-images.githubusercontent.com/78517969/152666876-7ffa46b0-2858-4fad-890f-e817536d0100.png" width=600 alt="Model" />
</p>

## API

