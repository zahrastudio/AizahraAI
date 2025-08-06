from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from modules.quran import ambil_quran
from modules.hadits import cari_hadits
from modules.doa import ambil_doa

TOKEN = "7904385831:AAHr0eoauFQoDf67xx8Rh0O1jrPI3SzTLt4"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalamualaikum, saya ZahraVerseAI siap membantu 🌙")

async def handle_quran(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        surah, ayat = context.args
        hasil = ambil_quran(surah, ayat)
        teks = f"📖 Quran {surah}:{ayat}\n{hasil['arab']}\n\nLatin: {hasil['latin']}\nArti: {hasil['translation']}"
    except:
        teks = "Gunakan format: /quran <surah> <ayat>"
    await update.message.reply_text(teks)

async def handle_hadits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tema = ' '.join(context.args) or 'niat'
    hasil = cari_hadits(tema)
    if hasil:
        h = hasil[0]
        teks = f"📜 Hadits {tema}\n{h['arab']}\n\nLatin: {h['latin']}\nArti: {h.get('terjemah') or h.get('arti')}\nSumber: {h['sumber']}"
    else:
        teks = "Hadits tidak ditemukan."
    await update.message.reply_text(teks)

async def handle_doa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    hasil = ambil_doa()
    teks = f"🤲 Doa: {hasil['doa']}\n{hasil['arab']}\n\nArti: {hasil['arti']}"
    await update.message.reply_text(teks)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quran", handle_quran))
    app.add_handler(CommandHandler("hadits", handle_hadits))
    app.add_handler(CommandHandler("doa", handle_doa))
    print("✅ ZahraVerseAI Telegram Bot aktif...")
    app.run_polling()

if __name__ == "__main__":
    main()
