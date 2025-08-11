#!/bin/bash
echo "=== Setup Otomatis AizahraAI (Online & Offline) ==="

# === Konfigurasi ===
VENVDIR="venv"
BACKUP_VENV="venv_backup.zip"
LOCAL_WHL_DIR="offline_wheels"
PYTHON_PKGS=("moviepy" "gTTS" "pydub" "requests" "feedparser" "pyvis" "matplotlib" "networkx")

# === Fungsi cek koneksi internet ===
cek_internet() {
    wget -q --spider http://google.com
    return $?
}

# === Fungsi install pip packages dengan retry ===
install_pip_packages() {
    local retries=5
    for ((i=1; i<=retries; i++)); do
        echo "Percobaan $i instalasi paket pip..."
        pip install --upgrade pip setuptools wheel
        pip install "${PYTHON_PKGS[@]}" && return 0
        echo "⚠️ Instalasi pip gagal. Coba lagi..."
        sleep 3
    done
    return 1
}

# === Mulai proses ===
# 1. Hapus venv lama jika tidak ingin pakai
if [ -d "$VENVDIR" ]; then
    echo "[1/5] Menghapus virtual environment lama..."
    rm -rf "$VENVDIR"
fi

# 2. Buat venv baru
echo "[2/5] Membuat virtual environment baru..."
python -m venv "$VENVDIR"

# 3. Aktifkan venv
echo "[3/5] Mengaktifkan virtual environment..."
source "$VENVDIR/bin/activate"

# 4. Cek koneksi internet
if cek_internet; then
    echo "🌐 Internet tersedia. Instal paket online..."
    if install_pip_packages; then
        echo "✅ Semua paket berhasil diinstal online."
    else
        echo "❌ Instalasi online gagal, mencoba offline..."
    fi
else
    echo "📴 Tidak ada internet. Menggunakan mode offline..."
fi

# 5. Instal offline jika perlu
if ! python -c "import moviepy, gtts, pydub, requests, feedparser, pyvis, matplotlib, networkx" 2>/dev/null; then
    if [ -f "$BACKUP_VENV" ]; then
        echo "📦 Memulihkan venv dari backup..."
        unzip -o "$BACKUP_VENV" -d .
    elif [ -d "$LOCAL_WHL_DIR" ]; then
        echo "📦 Menginstal paket dari file .whl lokal..."
        pip install "$LOCAL_WHL_DIR"/*.whl
    else
        echo "⚠️ Tidak ada backup atau file .whl lokal. Instalasi gagal."
        exit 1
    fi
else
    echo "✅ Semua paket sudah lengkap."
fi

echo "🎯 Setup selesai. Sistem siap digunakan!"

