# Proyecto-Blacklist

### Requerimientos del proyecto

- python 3.8.10

### Instrucciones para construir el proyecto

Para construir el proyecto es necesario utilizar un ambiente virtual de python, para realizarlo se debe instalar **venv** y crearlo con el siguiente comando:

```bashs
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

