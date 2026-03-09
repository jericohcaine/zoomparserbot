import os
import re
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def parse_zoom_link(url: str) -> dict | None:
    url = url.strip()

    # Formato estándar: https://xxx.zoom.us/j/ID?pwd=HASH.N
    m = re.search(r"zoom\.us/j/(\d+)\?pwd=([A-Za-z0-9_\-]+?)(?:\.\d+)?(?:[&#].*)?$", url)
    if m:
        return {"id": m.group(1), "pwd": m.group(2)}

    # Fallback genérico
    id_m  = re.search(r"/j/(\d+)", url)
    pwd_m = re.search(r"[?&]pwd=([A-Za-z0-9_\-]+)", url)
    if id_m or pwd_m:
        pwd = pwd_m.group(1).split(".")[0] if pwd_m else None
        return {"id": id_m.group(1) if id_m else None, "pwd": pwd}

    return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Mándame un link de Zoom y te saco el ID y la contraseña."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if "zoom.us" not in text:
        await update.message.reply_text("⚠️ Eso no parece un link de Zoom.")
        return

    result = parse_zoom_link(text)

    if not result:
        await update.message.reply_text("❌ No he podido extraer el ID ni la contraseña.")
        return

    lines = []
    if result["id"]:
        lines.append(f"`{result['id']}`")
    if result["pwd"]:
        lines.append(f"`{result['pwd']}`")

    if not lines:
        await update.message.reply_text("❌ Link reconocido pero sin ID ni contraseña.")
        return

    # Cada valor en su propio mensaje para facilitar copiar con un toque
    if result["id"]:
        await update.message.reply_text(
            f"🔢 *ID de reunión*\n`{result['id']}`",
            parse_mode="Markdown"
        )
    if result["pwd"]:
        await update.message.reply_text(
            f"🔑 *Contraseña*\n`{result['pwd']}`",
            parse_mode="Markdown"
        )


def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN no está definido como variable de entorno.")

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot arrancado...")
    app.run_polling()


if __name__ == "__main__":
    main()
