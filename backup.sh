#!/data/data/com.termux/files/usr/bin/bash

# Nama file backup
ZIP_NAME="AizahraAI_backup.zip"

# Buat backup zip dari folder AizahraAI
zip -r "$ZIP_NAME" ~/AizahraAI

# Jika zip berhasil dibuat, pindahkan ke folder Download
if [ -f "$ZIP_NAME" ]; then
  mv "$ZIP_NAME" ~/storage/shared/Download/
  echo "✅ Backup selesai. File disimpan di: ~/storage/shared/Download/$ZIP_NAME"
else
  echo "❌ Gagal membuat backup. File tidak ditemukan."
fi



