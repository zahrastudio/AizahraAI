# modules/translate.py
from deep_translator import GoogleTranslator

def translate_teks(teks, target='id'):
    try:
        hasil = GoogleTranslator(source='auto', target=target).translate(teks)
        return hasil
    except Exception as e:
        return f"[❌ ERROR]: {e}"


