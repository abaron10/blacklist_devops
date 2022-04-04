# Proyecto-Grupo11-202120

### Requerimientos del proyecto

- python 3.8.10
- ffmpeg 4.2.4-1ubuntu0.1
- redis 5.0.7

### Instrucciones para construir el proyecto

Para construir el proyecto es necesario utilizar un ambiente virtual de python, para realizarlo se debe instalar **venv** y crearlo con el siguiente comando:

```bash
  $ python3 -m venv env
```

Luego se activa el ambiente con el siguiente comando:

```bash
  $ source env/bin/activate
```

Instalar dependencias del proyecto:

```bash
  $ cd application
  $ pip install -r ./requirements.txt
```

### Ejecutar servidor

#### Con flask directamente

```bash
  $ cd application
  $ FLASK_APP=app/app flask run
```

#### Con Gunicorn

```bash
  $ cd application
  $ gunicorn --bind 0.0.0.0:8080 wsgi:app
```

### Ejecutar cola de mensajes

Con **redis** corriendo ejecutar el siguiente comando:

```bash
  $ cd application
  $ celery -A app.tareas.tareas worker
```

## Despliegue basico AWS
1. En la infraestructura creada encender las
![image](https://user-images.githubusercontent.com/64280930/140665348-a19ed371-3b26-4bc7-8b72-fe637e718e15.png)
2. Acceder al nodo bastión ssh -i ssh_<llave>.pem ubuntu@<ec2_ip>
3. Dentro del nodo bastion acceder al nodo web mediante ssh -i ssh_<llave_nodo_web>.pem ubuntu@<ec2_ip_web>
4. Acceder a la aplicación /application
5. Ejecutar
  ```bash
  $ gunicorn --bind 0.0.0.0:8080 wsgi:app
```
6. Salir del nodo web y acceder desde el nodo bastion al nodo de cola de mensajeria mediante ssh -i ssh_<llave_nodo_cola>.pem ubuntu@<ec2_ip_cola>
7. Acceder a la aplicación /application
```bash
  $ celery -A app.tareas.tareas worker
```
## Escalamiento de la capa web AWS
1. Balanceador de carga:
  Para poder distribuir la carga entre las diferentes EC2 es necesario configurar un balanceador como se ve en la figura
<p align="center">
<img width=750 src="https://user-images.githubusercontent.com/64280930/142772398-5208d950-7014-44fa-97aa-6a5f81b87d8d.png">
</p>
2. S3
  Sistema de almacenamiento de archivos externo para guardar las grabaciones
  <p align="center">
<img width=750 src="https://user-images.githubusercontent.com/64280930/142772654-7889f1bc-b691-4585-a244-c1994d4a17b8.png">
</p>
3. Ruta del balanceador:
  Es balanceador de carga distribuye las peticiones por el puerto 5000.
  http://plantillas-1-525534123.us-east-1.elb.amazonaws.com:5000
  

