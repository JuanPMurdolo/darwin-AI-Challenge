# darwin-AI-Challenge

# Bot de Seguimiento de Gastos en Telegram

Un sistema avanzado de bots para Telegram que permite a los usuarios registrar gastos mediante mensajes en lenguaje natural. El sistema utiliza IA para analizar y categorizar automáticamente los gastos.

## Arquitectura

El sistema está compuesto por dos microservicios:

### 1. Servicio Bot (Python)
- **Tecnologías**: FastAPI, LangChain, OpenAI, PostgreSQL
- **Propósito**: Procesa mensajes usando IA para extraer y categorizar gastos
- **Características**:
  - Procesamiento de lenguaje natural con LangChain + OpenAI
  - Categorización automática de gastos
  - Verificación de usuarios autorizados (whitelist)
  - Manejo concurrente de solicitudes

### 2. Servicio Conector (Node.js)
- **Tecnologías**: Node.js, Express, Telegram Bot API
- **Propósito**: Gestiona la interacción con Telegram y reenvía mensajes al Servicio Bot
- **Características**:
  - Gestión de webhooks/polling de Telegram
  - Enrutamiento de mensajes y respuestas
  - Manejo de errores y feedback al usuario

## Funcionalidades

✅ **Procesamiento de Lenguaje Natural**: Envía mensajes como "Pizza 20 pesos" o "Nafta $45"
✅ **Categorización Automática**: La IA categoriza los gastos en categorías predefinidas
✅ **Whitelist de Usuarios**: Solo usuarios autorizados pueden usar el bot
✅ **Procesamiento Concurrente**: Maneja múltiples usuarios simultáneamente
✅ **Manejo de Errores**: Gestión elegante de mensajes inválidos y errores
✅ **Despliegue Sencillo**: Listo para Vercel, Railway u otras plataformas

## Inicio Rápido

### Requisitos

- Python 3.11+
- Node.js LTS (18+)
- Base de datos PostgreSQL
- Clave API de OpenAI
- Token de Bot de Telegram

### 1. Configuración de la Base de Datos

```bash
# Configura PostgreSQL y ejecuta el script de inicialización
psql -d tu_base_de_datos -f scripts/01-create-database.sql
```

### 2. Servicio Bot

```bash
cd bot-service
pip install -r requirements.txt
cp .env.example .env
# Edita .env con tu configuración
python main.py
```

### 3. Servicio Conector

```bash
cd connector-service
npm install
cp .env.example .env
# Edita .env con tu configuración
npm start
```

## Configuración

### Variables de Entorno

**Servicio Bot (.env):**
```env
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/expense_bot
OPENAI_API_KEY=tu_clave_openai
PORT=8000
```

**Servicio Conector (.env):**
```env
TELEGRAM_BOT_TOKEN=tu_token_telegram
BOT_SERVICE_URL=http://localhost:8000
PORT=3000
```

### Agregar Usuarios Autorizados (Whitelist)

Agrega el ID de usuario de Telegram a la base de datos:

```sql
INSERT INTO users (telegram_id) VALUES ('123456789');
```

Para obtener el ID de Telegram de un usuario, puedes usar bots como @userinfobot.

## Ejemplos de Uso

Una vez que el bot está funcionando, los usuarios pueden enviar mensajes como:

- "Café 5 dólares" → Gasto de comida agregado ✅
- "Uber $15" → Gasto de transporte agregado ✅
- "Luz 120" → Gasto de servicios agregado ✅
- "Cine 25 pesos" → Gasto de entretenimiento agregado ✅

## Categorías

El bot categoriza automáticamente los gastos en:
- Vivienda
- Transporte
- Comida
- Servicios
- Seguros
- Salud
- Ahorro
- Deuda
- Educación
- Entretenimiento
- Otros

## Despliegue

### Vercel (Recomendado)

1. Sube el código a GitHub
2. Conecta el repositorio a Vercel
3. Configura las variables de entorno en el panel de Vercel
4. ¡Despliega!

### Railway

1. Conecta el repositorio de GitHub
2. Configura las variables de entorno
3. Despliega ambos servicios

### Supabase (Base de datos)

1. Crea un proyecto en Supabase
2. Ejecuta el script SQL en el editor de Supabase
3. Usa el string de conexión en tus variables de entorno

## Documentación de la API

### Servicio Bot

**POST /process-message**
```json
{
  "telegram_id": "123456789",
  "message": "Pizza 20 pesos"
}
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Gasto de comida agregado ✅",
  "category": "Comida"
}
```

### Endpoints de Salud

Ambos servicios proveen endpoints para verificar el estado:
- Servicio Bot: `GET /health`
- Servicio Conector: `GET /health`

## Desarrollo

### Ejecución en Desarrollo

**Terminal 1 (Servicio Bot):**
```bash
cd bot-service
python main.py
```

**Terminal 2 (Servicio Conector):**
```bash
cd connector-service
npm run dev
```

### Pruebas

Prueba el servicio bot directamente:
```bash
curl -X POST http://localhost:8000/process-message \
  -H "Content-Type: application/json" \
  -d '{"telegram_id": "123456789", "message": "Café 5 dólares"}'
```

## Buenas Prácticas Implementadas

- ✅ **Arquitectura de Microservicios**: Separación de responsabilidades
- ✅ **Configuración por Entorno**: Sin valores hardcodeados
- ✅ **Manejo de Errores**: Gestión integral de errores
- ✅ **Logging**: Registro estructurado en todos los servicios
- ✅ **Pool de Conexiones a BD**: Uso eficiente de la base de datos
- ✅ **Tipado Estricto**: Modelos Pydantic y soporte TypeScript
- ✅ **Apagado Elegante**: Limpieza adecuada al terminar
- ✅ **Endpoints de Salud**: Soporte para monitoreo y debugging

## Solución de Problemas

### Problemas Comunes

1. **El bot no responde**: Verifica que ambos servicios estén corriendo y puedan comunicarse
2. **Errores de conexión a la base de datos**: Revisa `DATABASE_URL` y la accesibilidad de la base
3. **Errores de OpenAI API**: Verifica la clave y los límites de uso
4. **Problemas con el webhook de Telegram**: Asegúrate de que el token es correcto y el bot está iniciado

Probado en Railway: https://railway.com/