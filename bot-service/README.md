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
    - `MODEL_NAME` (Para usar Groq)
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
- `POST /api/expense/add`: Analiza un mensaje de Telegram y almacena el gasto
- `GET /api/expense/list`: Lista todos los gastos (Para uso de test no se pide login)
- `GET /api/expense/id`: Obtiene un gasto por ID
- `DELETE /api/expense/id`: Elimina un gasto
- `PUT /api/expense/id`: Actualiza un gasto
- `POST /api/analytics/`: Crea un pedido de calculo de gastos, con un id de usuario y un START-END Date
- `GET /api/analytics/id`: Usando la task ID puedes ver si el calculo ya fue tomado/updateado/terminado por Celery y si funciono deberias ver el calculo final
- `GET /api/analytics/sync`: Solo para testing

6. Testing:
```bash
./run_tests.sh
```

## Notas
- Para pruebas con Docker y PostgreSQL, asegúrate de tener los servicios levantados.
- Revisa el archivo `.env.example` para ejemplos de configuración.





