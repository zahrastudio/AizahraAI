# bot.py atau main_bot.py

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from modules.chat import tanya_ai  # pastikan modul chat.py sudah tersedia

# Handler untuk perintah /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalamualaikum, saya ZahraVerseAI siap membantu 🌙")

# Handler untuk pesan biasa
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    response = tanya_ai(user_input)
    await update.message.reply_text(response)

# Main function untuk menjalankan bot
def main():
#     import os  # FIXED: unknown import commented out
#     from dotenv import load_dotenv  # FIXED: unknown import commented out
    load_dotenv()

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot ZahraVerseAI sedang berjalan...")
    app.run_polling()

if __name__ == '__main__':
    main()
