# ZoomBot

Bot de Telegram que extrae el ID de reunión y la contraseña de cualquier link de Zoom.

## Uso

Manda un link como este:
```
https://us06web.zoom.us/j/7200284335?pwd=PYYlsfXMpW0TMONdhfhm4eaGXI8OViJ.1
```

El bot responde con dos mensajes separados (fáciles de copiar con un toque):
```
🔢 ID de reunión
7200284335

🔑 Contraseña
PYYlsfXMpW0TMONdhfhm4eaGXI8OViJ
```

## Deploy en Railway

1. Sube esta carpeta a un repositorio de GitHub
2. En Railway: **New Project → Deploy from GitHub repo**
3. En **Variables**, añade:
   ```
   BOT_TOKEN = tu_token_de_botfather
   ```
4. Railway detecta el `Procfile` y arranca el worker automáticamente

## Local

```bash
pip install -r requirements.txt
BOT_TOKEN=tu_token python bot.py
```
