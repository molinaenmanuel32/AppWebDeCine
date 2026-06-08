# 🎬 AppWebDeCine

Aplicación web de cine desarrollada con **Reflex (Python)**, integrada con una base de datos MySQL y la API de TMDB para la gestión y visualización de películas.

## Objetivo

Diseñar y desarrollar una página web funcional que permita gestionar películas, usuarios y reservas de asientos, integrando una API conectada a una base de datos y utilizando control de versiones con GitHub.

---

## Estructura del Proyecto

```text
AppWebDeCine/
├── requirements.txt
├── rxconfig.py
├── .env.example
├── cinemax/
│   ├── cinemax.py
│   ├── components/
│   ├── data/
│   │   └── movies.json
│   ├── pages/
│   ├── states/
│   └── utils/
├── scripts/
└── README.md
```

---

## Tecnologías Utilizadas

* Python
* Reflex
* MySQL
* TMDB API
* Git y GitHub

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/AppWebDeCine.git
cd AppWebDeCine
```

### 2. Crear un entorno virtual

```bash
python -m venv .venv
```

Activar el entorno:

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear un archivo `.env` basado en `.env.example`.

Ejemplo:

```env
DB_HOST=tu_host
DB_PORT=3306
DB_NAME=tu_base_de_datos
DB_USER=tu_usuario
DB_PASSWORD=tu_password
TMDB_API_KEY=tu_api_key
```

> Importante: No subas el archivo `.env` a GitHub.

### 5. Ejecutar la aplicación

```bash
reflex run
```

La aplicación estará disponible en:

```text
http://localhost:3000
```

---

## Funcionalidades

### Catálogo de Películas

* Visualización de películas disponibles.
* Búsqueda y filtrado por categorías.
* Información detallada de cada película.

### Usuarios

* Registro de usuarios.
* Inicio de sesión.
* Gestión de sesiones.

### Reservas

* Selección de asientos.
* Registro de reservas.
* Consulta de asientos ocupados.

### Integración con TMDB

* Obtención de imágenes y datos actualizados de películas.
* Uso de la API de TMDB para enriquecer el catálogo.

---

## Base de Datos

La aplicación utiliza MySQL para almacenar:

* Usuarios
* Películas
* Funciones
* Reservas

Si la base de datos no está disponible, la aplicación puede utilizar datos locales de respaldo desde:

```text
cinemax/data/movies.json
```

---

## Buenas Prácticas

Agregar al archivo `.gitignore`:

```text
.env
.venv/
__pycache__/
*.pyc
```

Nunca almacenar:

* Contraseñas
* API Keys
* Tokens
* Credenciales de bases de datos

directamente en el código fuente o en el repositorio.

---

## Autor

Proyecto académico desarrollado para la gestión de reservas y administración de películas en una plataforma web de cine.
