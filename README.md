# 🚀 API de Pagos Casa Benetti

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Miguel-Emmanuel/Api_casa_benetti)
https://api-casa-benetti.onrender.com/
¡Bienvenido a la API REST para la gestión de usuarios y transacciones de pago de Casa Benetti! 

---

## 🔐 Autenticación y autorización (JWT)

- **Registro de usuario (`/users/`) y login (`/login/`)**: públicos.
- **Todos los endpoints de transacciones, historial y validación**: protegidos, requieren autenticación JWT.
- **¿Cómo usar?**
  1. Regístrate con `/users/` (POST).
  2. Haz login en `/login/` (POST, usa `username` y `password` en el body tipo form-data).
  3. Copia el `access_token` de la respuesta.
  4. Haz clic en "Authorize" en la interfaz `/docs` e ingresa: `Bearer <access_token>`.
  5. Ahora puedes acceder a todos los endpoints protegidos.

---

## 🔧 Variables de entorno (.env)

La API utiliza variables de entorno para mayor seguridad y flexibilidad. Puedes definirlas en un archivo `.env` en la raíz del proyecto:

```
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/db
SECRET_KEY=clave_secreta_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=1440
```

- En Render, configura estas variables en el panel de configuración del servicio web.
- Localmente, basta con el archivo `.env`.

---

## 🛡️ Seguridad avanzada y buenas prácticas

- **Rate limiting:** El endpoint `/login/` está protegido contra ataques de fuerza bruta (5 intentos por minuto por IP).
- **Refresh tokens:** Soporte para renovar el token de acceso sin reingresar credenciales.
- **Roles:** El modelo de usuario soporta roles (por defecto `user`).
- **Logs estructurados:** Todos los eventos importantes y errores se registran en `logs/api.log`.
- **Handler global de errores:** Todas las excepciones inesperadas devuelven un error JSON uniforme y quedan registradas.
- **Validación de acceso:** Los usuarios solo pueden consultar sus propias transacciones (salvo que sean admin).
- **Campos validados:** Límites de tamaño y validaciones estrictas en todos los modelos.

---

## 🛠️ Buenas prácticas
- Código modular y limpio.
- Validaciones y manejo de errores.
- Uso de Pydantic y SQLAlchemy.
- Pruebas unitarias automáticas.
- CI/CD con GitHub Actions (`.github/workflows/python-app.yml`).

---

## 📦 Instalación rápida

1. Clona el repositorio o descarga los archivos.
2. Instala las dependencias:
   ```powershell
   pip install -r requirements.txt
   ```
3. (Opcional) Configura la base de datos localmente:
   - Por defecto, la API usará SQLite si no encuentra la variable `DATABASE_URL`.
   - Para producción en Render, la base de datos PostgreSQL se configura automáticamente.

---

## Instalación y ejecución del proyecto

### Requisitos previos
- Python 3.10 o superior
- pip (gestor de paquetes de Python)

### Instalación de dependencias

```bash
pip install -r requirements.txt
```

### Ejecución del servidor

```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en http://127.0.0.1:8000

### Documentación interactiva

- Swagger UI: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc

### Notas importantes
- No es necesario ni se solicita client_id ni client_secret en ningún endpoint.
- Todas las respuestas siguen la estructura:
  ```json
  {
    "DATA": ...,
    "STATUS": true/false,
    "CODIGO": 200/201/400/401/404/500
  }
  ```
- El endpoint `/login` acepta POST (body) y GET (query params) solo con username y password.
- El endpoint `/me` devuelve los datos del usuario autenticado.

---

## ▶️ Ejecución local

```powershell
python -m uvicorn app.main:app --reload
```

Abre tu navegador en [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) para ver y probar la API con Swagger UI.

---

## ✨ Endpoints principales

- **Registrar usuario:** `POST /users/` (público)
- **Login:** `POST /login/` (público, retorna JWT)
- **Iniciar transacción:** `POST /transactions/` (protegido)
- **Consultar historial:** `GET /users/{user_id}/transactions/` (protegido)
- **Autorizar transacción:** `POST /transactions/authorize/` (protegido)
- **Obtener usuario autenticado:** `GET /users/me/` (protegido)

Explora y prueba todos los endpoints en `/docs`.

---

## 📚 Ejemplo de uso de refresh token

```json
POST /refresh-token/
{
  "refresh_token": "<tu_refresh_token>"
}
```
Respuesta:
```json
{
  "access_token": "nuevo_token",
  "token_type": "bearer"
}
```

---

## 🧪 Pruebas automáticas y base de datos limpia

Para asegurar que cada test se ejecuta en un entorno limpio, el archivo `test_api.py` elimina automáticamente el archivo `test.db` antes de cada prueba usando un fixture de pytest. Así, no necesitas borrar la base de datos manualmente.

### Ejecución de tests

```powershell
python -m pytest
```

Esto ejecutará todos los tests y recreará la base de datos desde cero en cada uno.

> **Nota:** Si usas Windows y ves errores de permisos, asegúrate de que ningún proceso esté usando `test.db` fuera de los tests.

---

## 🌐 Despliegue en Render

1. Haz clic en el botón “Deploy to Render” arriba ☝️
2. Crea una base de datos PostgreSQL en Render y copia la Internal Database URL.
3. En tu Web Service, agrega la variable de entorno:
   - **DATABASE_URL** = pega aquí la Internal Database URL
4. Render instalará dependencias y desplegará tu API automáticamente.

---

## 🌍 API en Producción
Accede a la API desplegada aquí (si ya la publicaste):
https://casa-benetti-api.onrender.com

Prueba los endpoints en la documentación interactiva:
https://casa-benetti-api.onrender.com/docs

---

## 🆘 ¿Dudas o problemas?
- Consulta los logs en Render si algo falla.
- Abre un issue en este repo si necesitas ayuda.
- ¡Tu API estará online en minutos! 🚀

---

> Desarrollado con ❤️ por Miguel Emmanuel
