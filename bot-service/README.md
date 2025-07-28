# Bot Service

Servicio Python que analiza y categoriza gastos desde mensajes de Telegram usando LangChain y OpenAI.

## Características
- Clasificación de mensajes
- Categorización de gastos
- Lista blanca de usuarios
- Manejo asíncrono y concurrente de requests
- Integración con PostgreSQL

## Configuración del entorno

1. Instala Python 3.11+
2. Crea un archivo `.env` con las siguientes variables:
    - `OPENAI_API_KEY=tu_clave`
    - `DATABASE_URL=postgresql+asyncpg://usuario:contraseña@localhost:5432/expenses_db`
    - `TELEGRAM_BOT_TOKEN=tu_token` (si usas integración Telegram)
    - `MODEL_NAME` (Para usar Groq)s
    - `GROQ_API_KEY` (API Key de Groq)
    - `REDIS_URL = redis://redis:6379/0`
    - `CELERY_BROKER_URL = redis://redis:6379/0`
    - `CELERY_RESULT_BACKEND = redis://redis:6379/0`

3. Instala dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecuta el servidor:
```bash
docker-compose up --build
```

5. Endpoints principales:
- `POST /expense/add`: Analiza un mensaje de Telegram y almacena el gasto
- `GET /expense/list`: Lista todos los gastos
- `GET /expense/id`: Obtiene un gasto por ID
- `DELETE /expense/id`: Elimina un gasto
- `PUT /expense/id`: Actualiza un gasto

6. Testing:
```bash
./run_tests.sh
```

## Notas
- Para desarrollo local puedes usar SQLite: `DATABASE_URL=sqlite+aiosqlite:///./test.db`
- Para pruebas con Docker y PostgreSQL, asegúrate de tener los servicios levantados.
- Revisa el archivo `.env.example` para ejemplos de configuración.





