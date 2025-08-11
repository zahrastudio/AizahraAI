# import os  # FIXED: unknown import commented out
# from dotenv import load_dotenv  # FIXED: unknown import commented out
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from modules import chat, tts, audio

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN tidak ditemukan di .env")

# Bersihkan folder audio/ saat start
audio.cleanup_audio_folder()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Kirim /chat <pertanyaan> untuk mulai.")

async def chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Format: /chat <pertanyaan>")
        return

    prompt = " ".join(context.args)
    await update.message.reply_text("⏳ Tunggu sebentar...")

    try:
        # Dapatkan jawaban dari GPT
        answer = chat.chat_ai(prompt)

        # Konversi ke voice .ogg
        ogg_path = tts.text_to_speech_ogg(answer)

        # Kirim voice bulat
        with open(ogg_path, "rb") as voice_file:
            await update.message.reply_voice(voice=voice_file, caption=answer)

    except Exception as e:
        await update.message.reply_text(f"❌ Terjadi kesalahan: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("chat", chat_command))

    print("🤖 Bot berjalan...")
    app.run_polling()
