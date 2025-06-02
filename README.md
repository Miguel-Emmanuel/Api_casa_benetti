# API de Pagos Casa Benetti

Proyecto FastAPI para gestión de usuarios y transacciones de pago.

## Instalación

1. Clona el repositorio o descarga los archivos.
2. Instala las dependencias:

```powershell
pip install -r requirements.txt
```

3. Configura la base de datos MySQL ejecutando el script:

```powershell
mysql -u root -p < pagos_benetti_setup.sql
```

4. Actualiza la cadena de conexión en `app/database.py` si cambiaste usuario, contraseña o base de datos.

## Ejecución

Inicia el servidor con:

```powershell
python -m uvicorn app.main:app --reload
```

Abre tu navegador en [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) para ver y probar la API.

## Pruebas

Ejecuta las pruebas unitarias con:

```powershell
python -m pytest
```

## Endpoints principales

- **Registrar usuario:** `POST /users/`
- **Iniciar transacción:** `POST /transactions/`
- **Consultar historial:** `GET /users/{user_id}/transactions/`
- **Autorizar transacción:** `POST /transactions/authorize/`

## Buenas prácticas
- Código modular y limpio.
- Validaciones y manejo de errores.
- Uso de Pydantic y SQLAlchemy.
- Pruebas unitarias automáticas.

## Despliegue automático (CI/CD)

Puedes usar GitHub Actions para CI/CD. Ejemplo de workflow en `.github/workflows/python-app.yml`:

```yaml
name: Python application

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python -m pytest
```

Guarda este archivo en `.github/workflows/python-app.yml` para activar CI/CD en GitHub.

---

¿Dudas? Consulta la documentación en `/docs` o abre un issue.
