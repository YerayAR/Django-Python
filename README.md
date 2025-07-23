# Memory Game Web Application

## 📌 Resumen del Proyecto
Aplicación web de ejemplo desarrollada con **Django** que implementa un juego de memoria.
El objetivo es encontrar todas las parejas de cartas con el menor número de movimientos.
La lógica del juego se mantiene en la sesión del usuario, por lo que no es necesario una base de datos.

## 🔧 Requisitos Técnicos
- Python 3.11
- Django >= 3.2
- Docker y Docker Compose (opcional para un entorno aislado)

## 🚀 Instrucciones de Instalación
1. Clona el repositorio.
   ```bash
   git clone <repo-url>
   cd Memory-Game-Web-App
   ```
2. Crea un entorno virtual e instala dependencias.
   ```bash
   python -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```
3. Ejecuta la aplicación.
   ```bash
   python backend/manage.py runserver
   ```
   La aplicación estará disponible en `http://localhost:8000/`.

### Con Docker
```bash
docker-compose up --build
```

## 🧪 Ejemplos de Uso
- Para voltear una carta se realiza una petición `GET` a `/flip/<indice>/`.
- Las cartas y su estado se devuelven en formato JSON para actualizar el tablero en el navegador.

## 🗂️ Estructura del Proyecto
```text
.
├── backend/               -> Código backend de Django
│   ├── manage.py          -> Script de gestión
│   ├── config/            -> Configuración global (settings, urls, wsgi)
│   └── game/              -> Aplicación principal
│       ├── controllers/   -> Vistas de Django
│       ├── routes/        -> Definición de rutas
│       └── services/      -> Lógica del juego
├── frontend/              -> Archivos estáticos y plantillas
│   ├── static/            -> CSS y JavaScript
│   └── templates/         -> Plantillas HTML
├── Dockerfile             -> Imagen de desarrollo
├── docker-compose.yml     -> Orquestación opcional con Docker
└── requirements.txt       -> Dependencias de Python
```

## 👨‍💻 Contribución
Las aportaciones son bienvenidas mediante *pull requests* o creación de *issues*.

## 📄 Licencia
Proyecto disponible bajo la licencia MIT.

## 🧠 Consideraciones Finales
La lógica original del juego se ha mantenido intacta. La reestructuración solo
organiza el código para facilitar su mantenimiento y comprensión.
