# Manual Técnico – API de Pagos Casa Benetti

## Estructura del proyecto

- `app/` – Código fuente principal
  - `main.py` – Entrypoint FastAPI, rutas y dependencias
  - `models.py` – Modelos SQLAlchemy (User, Transaction)
  - `schemas.py` – Esquemas Pydantic (validación y serialización)
  - `crud.py` – Lógica de acceso a datos
  - `database.py` – Configuración de la base de datos
  - `tests/` – Pruebas automáticas con pytest
- `requirements.txt` – Dependencias
- `README.md` – Guía de uso y despliegue
- `user_manual.md` – Manual de usuario
- `tech_manual.md` – Manual técnico (este archivo)

---

## Tecnologías principales
- Python 3.12+
- FastAPI
- SQLAlchemy
- Pydantic v2
- PostgreSQL (Render) / SQLite (local)
- JWT (python-jose)
- Bcrypt (hash de contraseñas)
- Pytest (pruebas)

---

## Instalación y configuración

1. Instala dependencias:
   ```powershell
   pip install -r requirements.txt
   ```
2. (Opcional) Crea y configura la base de datos localmente (SQLite por defecto).
3. Para producción, define la variable de entorno `DATABASE_URL` (PostgreSQL).

---

## Ejecución local
```powershell
python -m uvicorn app.main:app --reload
```

---

## Pruebas automáticas
```powershell
python -m pytest
```

---

## Seguridad y buenas prácticas
- Contraseñas hasheadas con bcrypt.
- JWT para autenticación y protección de endpoints.
- Validaciones robustas con Pydantic v2.
- Fechas timezone-aware (`datetime.now(timezone.utc)`).
- Pruebas limpias y cobertura de errores comunes.

---

## Despliegue en Render
1. Haz clic en “Deploy to Render” en el README.
2. Crea una base de datos PostgreSQL y copia la Internal Database URL.
3. Agrega la variable de entorno `DATABASE_URL` en tu servicio web.
4. Render instalará dependencias y desplegará la API automáticamente.

---

## Extensión y mantenimiento
- Para agregar endpoints, crea el esquema en `schemas.py`, la función en `crud.py` y la ruta en `main.py`.
- Usa validaciones con `@field_validator` y `ConfigDict`.
- Agrega pruebas en `app/tests/test_api.py`.
- Mantén las dependencias actualizadas.

---

## Recomendaciones avanzadas
- Implementa rate limiting (`slowapi`) para endpoints sensibles.
- Usa logs estructurados (`logging` o `loguru`).
- Considera refresh tokens y roles de usuario si el proyecto crece.
- Usa un archivo `.env` para variables sensibles (con `python-dotenv`).

---

## Instalación y dependencias

Antes de ejecutar la API, asegúrate de instalar las dependencias con:

```
pip install -r requirements.txt
```

## Estructura de respuesta estándar

Todas las respuestas de la API siguen el formato:

```
{
  "DATA": ...,
  "STATUS": true/false,
  "CODIGO": 200/201/400/401/404/500
}
```

## Endpoints principales

- `/login` (POST y GET): Solo requiere username y password. No se solicita client_id ni client_secret.
- `/me`: Devuelve los datos del usuario autenticado.

## Ejecución

```
uvicorn app.main:app --reload
```

La documentación interactiva está disponible en `/docs`.

---

## 🧪 Pruebas automáticas y base de datos limpia

- El archivo `app/tests/test_api.py` elimina automáticamente `test.db` antes de cada test usando un fixture de pytest.
- Esto garantiza que cada prueba se ejecuta en un entorno limpio y reproducible.
- No es necesario borrar manualmente la base de datos antes de correr los tests.

---

¿Dudas técnicas? Consulta el código fuente o abre un issue en el repositorio.
