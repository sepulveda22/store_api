# Store API - FastAPI

## Requisitos
- Python 3.8+
- pip

## Instalación

1. Clona el repositorio:
   ```bash
   git clone <URL_DEL_REPO>
   cd store_api
   ```

2. Crea un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   # Activa el entorno virtual:
   # En Windows:
   venv\Scripts\activate
   # En Linux/Mac:
   source venv/bin/activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura tu archivo `config.json` con tus variables necesarias (ejemplo: secret_key, datos de conexión a base de datos).

5. Ejecuta el servidor:
   ```bash
   uvicorn main:app --reload
   ```

## Documentación

Accede a la documentación interactiva en:
- http://localhost:8000/docs
- http://localhost:8000/redoc

## Estructura del proyecto
- `main.py`: Punto de entrada de la API
- `models/`: Modelos de la base de datos
- `schemas/`: Esquemas Pydantic
- `routes/`: Rutas/endpoints
- `utils/`: Utilidades y seguridad
- `database.py`: Configuración de la base de datos

## Pruebas
(Agrega aquí instrucciones si implementas tests)

---

Recuerda no subir archivos sensibles como `config.json` al repositorio público.
