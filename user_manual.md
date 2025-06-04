# Manual de Usuario – API de Pagos Casa Benetti

## ¿Qué es esta API?
La API de Pagos Casa Benetti permite gestionar usuarios y transacciones de pago de forma segura y sencilla. Está pensada para ser consumida por aplicaciones web, móviles o integraciones de terceros.

---

## ¿Cómo empezar?

### 1. Registro de usuario
- Endpoint: `POST /users/`
- Body (JSON):
  ```json
  {
    "email": "usuario@correo.com",
    "password": "tu_contraseña_segura"
  }
  ```
- Respuesta exitosa: 201 Created

### 2. Login y obtención de token JWT
- Endpoint: `POST /login/`
- Body (form-data):
  - username: tu email
  - password: tu contraseña
- Respuesta exitosa:
  ```json
  {
    "access_token": "<token>",
    "token_type": "bearer"
  }
  ```

### 3. Usar el token para endpoints protegidos
- Copia el `access_token`.
- En cada petición protegida, agrega el header:
  ```
  Authorization: Bearer <access_token>
  ```

---

## Ejemplos de uso

### Crear transacción
- Endpoint: `POST /transactions/`
- Body (JSON):
  ```json
  {
    "user_id": 1,
    "amount": 100.0,
    "status": "pending"
  }
  ```
- Header: Authorization con tu token.

### Consultar historial
- Endpoint: `GET /users/1/transactions/`
- Header: Authorization con tu token.

### Autorizar transacción
- Endpoint: `POST /transactions/authorize/`
- Body (JSON): igual que crear transacción.
- Header: Authorization con tu token.

---

## Errores comunes
- 401 Unauthorized: Token inválido o no enviado.
- 400 Bad Request: Datos inválidos o usuario ya existe.
- 422 Unprocessable Entity: Faltan campos o formato incorrecto.

---

## Documentación interactiva
Puedes probar todos los endpoints y ver ejemplos en:
- [http://localhost:8000/docs](http://localhost:8000/docs) (local)
- [https://casa-benetti-api.onrender.com/docs](https://casa-benetti-api.onrender.com/docs) (producción)

---

## 🔑 Cómo usar la autenticación en Swagger UI

1. Haz login en `/custom-login/` desde la interfaz `/docs` (solo username y password, nunca client_id ni client_secret).
2. Copia el valor de `access_token` que recibes en la respuesta.
3. Haz clic en el botón "Authorize" (ícono de candado arriba a la derecha).
4. Pega el token así:
   ```
   Bearer <tu_access_token>
   ```
   (incluye la palabra Bearer y un espacio antes del token)
5. Haz clic en "Authorize" y luego en "Close".
6. Ahora puedes probar cualquier endpoint protegido directamente desde la interfaz gráfica.

---

## ¿Cómo usar la API?

1. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```
2. Ejecuta el servidor:
   ```
   uvicorn app.main:app --reload
   ```
3. Accede a la documentación interactiva en http://127.0.0.1:8000/docs

### Estructura de respuesta
Todas las respuestas tienen el formato:
```
{
  "DATA": ...,
  "STATUS": true/false,
  "CODIGO": 200/201/400/401/404/500
}
```

### Endpoints principales
- `/custom-login` (POST): Solo requiere username y password. No se solicita client_id ni client_secret.
- `/me`: Devuelve los datos del usuario autenticado.

---

## 🧪 Pruebas automáticas y base de datos limpia

- Cada vez que ejecutas los tests (`python -m pytest`), la base de datos `test.db` se elimina automáticamente antes de cada prueba.
- Esto asegura que cada test corre en un entorno limpio y sin datos residuales.
- No necesitas borrar manualmente el archivo ni preocuparte por errores de permisos (salvo que otro proceso esté usando la base de datos fuera de los tests).

---

¿Dudas? Consulta el README o contacta al desarrollador.
