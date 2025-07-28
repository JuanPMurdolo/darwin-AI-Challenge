# Connector Service

Servicio Node.js que conecta el bot de Telegram con el backend y otros servicios externos.

## Configuración del entorno

1. Instala Node.js 18+
2. Crea un archivo `.env` con las siguientes variables:
    - `TELEGRAM_BOT_TOKEN=tu_token`
    - `API_URL=http://localhost:8001` (URL del backend Bot Service)
    - `TELEGRAM_BOT_SERVICE`

3. Instala dependencias:
```bash
npm install
```

4. Ejecuta el servicio:
```bash
npm start
```

## Notas
- El servicio se conecta con el bot de Telegram y reenvía los mensajes al backend.
- Revisa el archivo `.env.example` para ejemplos de configuración.
