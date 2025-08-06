#!/data/data/com.termux/files/usr/bin/bash

echo "🔄 Menghapus file script lama..."
rm -f main.py karakter.py
rm -rf modules/

echo "🗂 Membuat ulang struktur folder..."
mkdir modules
touch main.py karakter.py modules/quran.py modules/hadits.py modules/doa.py

echo "✅ Struktur bot AizahraAI telah direset."
echo "Silakan edit ulang: main.py, karakter.py, dan modules/*"

