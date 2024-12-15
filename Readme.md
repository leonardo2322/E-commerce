# **Django E-comerce app**

Este proyecto es una aplicación web desarrollada con Django que permite a los usuarios crear, listar y eliminar Productos. Es una aplicacion sencilla con perfil y creacion de productos para superusuarios, proyecto de aprendizaje.

---

## **Características**

- **Gestión de usuarios:**
  - Registro y autenticación de usuarios.
- **Creación de Productos categorias siendo superusuario:**
  - puedes insertar variedad de categorias por su nombre productos con imagenes
- **historial de compra para usuarios normales**
  - el usuario que se registre podra comprar los productos disponibles y tendra un historial de compra

---

## **Requisitos Previos**

Antes de ejecutar este proyecto, asegúrate de tener instalado lo siguiente:

- Python l3.12.5
- Django 5.1.3
- Docker (opcional, para ejecutar con contenedores)
- Git (opcional, para clonar el repositorio)

---

## **Instalación y Ejecución**

#### 1. **Crea un entorno virtual **

```terminal
- python -m venv env
- source env/bin/activate # En Windows: env\Scripts\activate
```

#### 2.**Clona este repositorio**

```bash o windows
https://github.com/leonardo2322/E-commerce.git

cd .\E-commerce\Turing\

```

#### 3. **con el entorno activo ejecuta en la terminal**

```terminal shell o bash
- pip install -r requirements.txt
```

#### 5. **Ejecuta el servidor local**

```terminal shell o bash
python manage.py runserver
```

#### 6. **si te falla por alguna razon por la secret key**

```terminal shell o bash
bien se debes crear el .env donde iran claves sensibles del contenedor para la base de datos y tambien la clave secreta
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### **Con Docker**

```terminal o shell
ejecuta este comando

- docker-compose build

 para construir y preparar las imagenes docker

- docker-compose up

este comando levantaria los contenedores y ya puedes localmente en localhost:8000 acceder a la pagina

- comando completo windows
- docker-compose build; docker-compose up
este ejecutara todo de una agrega -d si no quieres los logs

    linux
- docker-compose build && docker-compose up

```
