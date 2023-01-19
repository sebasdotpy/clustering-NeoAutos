# Despliegue de aplicaciones en servidor (Linux)

Vamos a desplegar nuestra aplicación basada en Flask en nuestros servidores</br>

Flask es un framework que muchas personas aprenden como su _primer framework_ web ya que es simple, ligero y facil de aprender</br>

## Pasos a seguir

1. Crear o clonar nuestra aplicación dentro del servidor
2. Ejecutar Gunicorn WSGI en el servidor para servir la aplicación
3. Usar systemd para administrar Gunicorn
4. Ejecutar Nginx Webserver para aceptar y enrutar las peticiones al servidor de Gunicorn

## 1. Crear o clonar nuestra aplicación dentro del servidor

Si ya tienen su aplicación en un repositorio de Git, clona tu aplicación dentro del servidor.

* Instalar Python Virtualenv

```bash
sudo apt-get update
sudo apt-get install python3-venv
```

* Activar el entorno virtual en un nuevo directorio.

```bash
// Crear directorio
mkdir enviroments
cd enviroments

//Crear nuestro entorno virtual
python3 -m venv <nombre_del_entorno>

//Activar el entorno virtual
source venv/bin/activate

//Instalar nuestros requirements
pip install -r requirements.txt
```

* Verificamos que nuestra app esté funcionando ejecutando `python app.py`

## 2. Ejecutar Gunicorn WSGI server para _servir_ nuestra aplicación

Cuando nosotros _`corremos`_ Flask en realidad estamos ejecutando un servidor de desarrollo Werkzeug’s WSGI server que reenvia las solicitudes de nuestro servidor web.</br></br>
Dado que Werkzeug es solo para desarrollo, tenemos que usar Gunicorn, que es un servidor WSGI listo para producción, para atender nuestra aplicación.

1. Instalar Gunicorn usando `pip install gunicorn`
2. Ejecutar Gunicorn -`gunicorn -b 0.0.0.0:8000 app:app`. Para más codificaciones de este comando podemos visitar la [Documentacion de Gunicorn](https://gunicorn.org/)
3. Gunicorn está ejecutandose!. (Ctrl+C para salir de Gunicorn)

## 3. Usar systemd para administrar Gunicorn

Systemd es el boot manager por default de linux, lo usaremos para reiniciar nuestro servicio en caso de que el servidor se reinicie.

Vamos a crear un \<projectname>.service en la ruta `/etc/systemd/system` y especificaremos que pasará con gunicorn cuando se reinicie el servidor.

Añadiremos 3 partes a systemd Unit file - Unit, Service, Install

1. Unit - Esta sección es para la descripción de nuestro proyecto y algunas dependencias
2. Service - Para especificar el Usuario/Grupo que queremos que ejecute este servicio así como tambien información hacerca de como ejecutarlo
3. Install - Le dice a `systemd` a que momento durante el booteo deberá iniciarse este servicio

* Con esto dicho crearemos el archivo en la ruta

```bash
sudo nano /etc/systemd/system/dashapp.service
```

* Luego añadiremos esto al archivo

```text
[Unit]
Description=Gunicorn instance for a simple hello world app
After=network.target
[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/helloworld
ExecStart=/home/ubuntu/helloworld/venv/bin/gunicorn -b localhost:8000 app:app
Restart=always
[Install]
WantedBy=multi-user.target
```

* Despues activaremos el servicio

```bash
sudo systemctl daemon-reload
sudo systemctl start dashapp
sudo systemctl enable dashapp
```

* Finalmente verificaremos que la app se está ejecutando con `curl localhost:8000`

## 4. Ejecutar Nginx para aceptar las solicitudes al servidor

* Intalar Nginx - `sudo apt-get install nginx`
* Iniciar el servicio

```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

* Editar el archivo por default en los sitios disponibles

```bash
sudo nano /etc/nginx/sites-available/default
```

* Añadimos lo siguiente en la parte superior del archivo (debajo de los comentarios por defecto)

```text
upstream flaskhelloworld {
    server 127.0.0.1:8000;
}
```

* Añadimos un `proxi-pass` al proyecto en la locación `location/`

```text
# Some code above
location / {
    proxy_pass http://flaskhelloworld;
}
# some code below
```

* Reiniciamos Nginx

```text
sudo systemctl restart nginx
```

**TADA !!  Nuestra aplicación ya está lista para recibir usuarios**

---

# Referencias
[Step-by-step visual guide on deploying a Flask application on AWS EC2
](https://medium.com/techfront/step-by-step-visual-guide-on-deploying-a-flask-application-on-aws-ec2-8e3e8b82c4f7)

[Waitress](https://flask.palletsprojects.com/en/2.2.x/deploying/waitress/)

# **NOTA**

Para cambiar los permisos de ejecución de un fichero usamos el comando

```bash
sudo chmod [OPTIONS] nombre_del_fichero.extension

//siendo las opciones:
u -> user
g -> group
o -> others

r -> read
w -> write
x -> execute
```
