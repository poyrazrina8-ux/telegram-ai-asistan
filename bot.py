
import os
import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from google import genai

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

client = genai.Client(api_key=GEMINI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Merhaba! Ben kişisel yapay zekâ asistanınım. 🤖\n"
        "Bana mesaj yazabilirsin.\n"
        "/yardim komutuyla komutları görebilirsin."
    )

async def yardim(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Kullanabileceğin komutlar:\n"
        "/start - Asistanı başlat\n"
        "/yardim - Yardım\n\n"
        "Normal mesaj yazarak benimle sohbet edebilirsin."
    )

async def sohbet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mesaj = update.message.text
    try:
        cevap = await asyncio.to_thread(
            client.models.generate_content,
            model="gemini-2.5-flash",
            contents=mesaj,
        )
        metin = cevap.text or "Şu an cevap oluşturamadım."
        await update.message.reply_text(metin[:4000])
    except Exception:
        await update.message.reply_text(
            "Şu an bir hata oluştu. Biraz sonra tekrar dene."
        )

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("yardim", yardim))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, sohbet)
    )
    app.run_polling()

if __name__ == "__main__":
    main()
