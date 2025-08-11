#!/data/data/com.termux/files/usr/bin/bash
# File: run_cek_upgrade_paket.sh
# Fungsi: Menjalankan cek_upgrade_paket.py di virtual environment Termux dan simpan log

# Path ke virtual environment dan skrip Python kamu
VENV_PATH="/data/data/com.termux/files/home/AizahraAI/venv"
SCRIPT_PATH="/data/data/com.termux/files/home/AizahraAI/cek_upgrade_paket.py"
LOGFILE="/data/data/com.termux/files/home/AizahraAI/cron_upgrade_log.txt"

# Aktifkan virtual environment
source "$VENV_PATH/bin/activate"

# Tanggal & waktu sekarang untuk log
NOW=$(date +"%Y-%m-%d %H:%M:%S")
echo "===== Script run at: $NOW =====" >> "$LOGFILE"

# Jalankan skrip Python
python "$SCRIPT_PATH" >> "$LOGFILE" 2>&1

echo "===== Script finished at: $(date +"%Y-%m-%d %H:%M:%S") =====" >> "$LOGFILE"
echo "" >> "$LOGFILE"  # spasi sebagai pemisah

# Nonaktifkan virtual environment (opsional)
deactivate


