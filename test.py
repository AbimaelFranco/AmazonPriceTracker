from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    filters,
)
from telegram.error import NetworkError, TelegramError
from decouple import config
from get_image import get_image
from get_title import get_product_title
import logging

# Configurar logging para controlar los errores en consola
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Token desde .env
TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Envíame el link de Amazon con /track <url> <minutos>")

# /track
async def track(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Mensaje recibido:", update.message.text)
    
    args = context.args
    if not args or len(args) != 2:
        await update.message.reply_text("Formato incorrecto. Usa /track <url> <minutos>")
        return

    url, time = args
    # await update.message.reply_text(f"Ok, empezaré a monitorear {url} cada {minutos} minutos.")

    # Obtener imagen del producto
    imagen_url = get_image(url)
    title = get_product_title(url)


    if not imagen_url or not title:
        await update.message.reply_text("No se pudo obtener la imagen o el título del producto.")
        await update.message.reply_text(f"URL: {url}\nMonitoreando cada {time} minutos")
        return

    caption = f"*Nombre del producto*: {title}\n*Tiempo de monitoreo*: {time} minutos"

    await update.message.reply_photo(photo=imagen_url, caption=caption, parse_mode='Markdown')
    # await update.message.reply_text(f"Producto: {title}\nURL: {url}\nMonitoreando cada {time} minutos...")

    # if imagen_url:
    #     await update.message.reply_photo(photo=imagen_url, caption="Esta es la imagen del producto que vas a seguir.")
    # else:
    #     await update.message.reply_text("No se pudo obtener la imagen del producto.")

# Manejo de errores global
async def manejar_errores(update: object, context: ContextTypes.DEFAULT_TYPE):
    error = context.error
    if isinstance(error, NetworkError):
        print("Error de red: probablemente se perdió la conexión con Telegram.")
    elif isinstance(error, TelegramError):
        print("Error de Telegram:", error)
    else:
        print("Error inesperado:", error)

# Función principal
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Handlers de comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("track", track))

    # Manejador global de errores
    app.add_error_handler(manejar_errores)

    # Iniciar el bot
    app.run_polling()

if __name__ == '__main__':
    main()
