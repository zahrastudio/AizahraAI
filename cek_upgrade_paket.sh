#!/data/data/com.termux/files/usr/bin/bash

# File: cek_upgrade_paket.sh
# Fungsi: Cek & upgrade paket Python otomatis di Termux, logging ke file

# Aktifkan virtual environment
source /data/data/com.termux/files/home/AizahraAI/venv/bin/activate

# Tanggal sekarang untuk log
NOW=$(date +"%Y-%m-%d %H:%M:%S")

# Lokasi log file
LOGFILE="/data/data/com.termux/files/home/AizahraAI/upgrade_log.txt"

# Catat waktu mulai eksekusi ke log
echo "===== Script run at: $NOW =====" >> "$LOGFILE"

# Jalankan skrip Python cek & upgrade paket, output ke log dan juga terminal
python /data/data/com.termux/files/home/AizahraAI/cek_upgrade_paket.py | tee -a "$LOGFILE"

# Catat selesai ke log
echo "===== Script finished at: $(date +"%Y-%m-%d %H:%M:%S") =====" >> "$LOGFILE"
echo "" >> "$LOGFILE"  # baris kosong sebagai pemisah	

