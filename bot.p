import os import logging from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup from telegram.ext import (ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler, CallbackContext, ContextTypes)

Konfigurasi logging

logging.basicConfig( format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO ) logger = logging.getLogger(name)

Fungsi /start

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: keyboard = [ [InlineKeyboardButton("Menu Utama", callback_data='menu')] ] reply_markup = InlineKeyboardMarkup(keyboard) await update.message.reply_text('Selamat datang di AizahraAI!', reply_markup=reply_markup)

Fungsi callback dari tombol menu

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: query = update.callback_query await query.answer() data = query.data

if data == 'menu':
    keyboard = [
        [InlineKeyboardButton("Tentang", callback_data='about')],
        [InlineKeyboardButton("Bantuan", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Silakan pilih menu:", reply_markup=reply_markup)

elif data == 'about':
    await query.edit_message_text(text="AizahraAI adalah bot yang membantu eksplorasi spiritual dan kemanusiaan.")

elif data == 'help':
    await query.edit_message_text(text="Ketik /start untuk memulai, atau gunakan menu di bawah ini untuk navigasi.")

Fungsi fallback pesan teks

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: await update.message.reply_text(f"Anda mengirim: {update.message.text}")

Fungsi error handler

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None: logger.warning(f'Update {update} menyebabkan error {context.error}')

Fungsi utama

def main() -> None: TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") if not TOKEN: raise ValueError("TOKEN Telegram belum diatur di environment variable TELEGRAM_BOT_TOKEN")

application = ApplicationBuilder().token(TOKEN).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

application.add_error_handler(error_handler)

application.run_polling()

if name == 'main': main()



