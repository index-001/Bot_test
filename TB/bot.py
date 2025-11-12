from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests

URL_SHEET = "https://script.google.com/macros/s/AKfycbyDL2SOKAQafW9inwsxwyDq3TQW7CPXXFBxnmeSN6DSXeyGyFZaogTYSr7O7KO3LxgXgg/exec"

# Comando de inicio
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Envíame tu nombre, correo y mensaje separados por comas.")

# Captura de mensajes
async def recibir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        texto = update.message.text
        nombre, correo, mensaje = texto.split(",")
        data = {"nombre": nombre.strip(), "correo": correo.strip(), "mensaje": mensaje.strip()}
        
        r = requests.post(URL_SHEET, json=data)
        if r.text == "OK":
            await update.message.reply_text("✅ Datos enviados a Google Sheets correctamente.")
        else:
            await update.message.reply_text("⚠️ Error al enviar los datos.")
    except Exception as e:
        await update.message.reply_text("Formato incorrecto. Usa: Nombre, Correo, Mensaje")

# Crear el bot
app = ApplicationBuilder().token("8533267780:AAEG2DPjcpcyP0qEhgjU5lMITLVSJIBnrfY").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, recibir))

app.run_polling()
