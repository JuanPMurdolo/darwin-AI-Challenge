# Frontend Bot Service

Aplicación web (Next.js) para visualizar y gestionar gastos categorizados por el bot.

## Configuración del entorno

1. Instala Node.js 18+
2. Crea un archivo `.env.local` con las siguientes variables:
    - `NEXT_PUBLIC_API_URL=http://localhost:8001` (URL del backend Bot Service)

3. Instala dependencias:
```bash
npm install
```

4. Ejecuta el frontend:
```bash
npm run dev
```

## Notas
- El frontend consume los endpoints del Bot Service.
- Revisa el archivo `.env.local.example` para ejemplos de configuración.
- Personaliza los estilos en `tailwind.config.js` y los componentes en `app/components/`.
